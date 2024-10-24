import asyncio
from .account import Account
from typing import List
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.middleware import async_geth_poa_middleware
import random
from config import RPC, ERC20_ABI
from loguru import logger
from utils.helpers import retry, sleep
from utils.gas_checker import check_gas


class Transfer(Account):
    def __init__(self, wallet_info, from_chains=None):
        chain = 'scroll' if not from_chains or 'scroll' in from_chains else 'ethereum'
        super().__init__(wallet_info=wallet_info, chain=chain)

    async def find_chains_with_max_balance(self, chains: List[str], min_required_amount):
        source_chains = []
        for chain in chains:
            w3 = AsyncWeb3(AsyncHTTPProvider(random.choice(RPC[chain]["rpc"]),
                                             request_kwargs=self.request_kwargs),
                           middlewares=[async_geth_poa_middleware]
                           )
            balance_wei = await w3.eth.get_balance(w3.to_checksum_address(self.address))
            balance = w3.from_wei(balance_wei, 'ether')
            if balance >= min_required_amount:
                source_chains.append((chain, balance))

        source_chains = [chain for chain, _ in sorted(source_chains, key=lambda x: x[1], reverse=True)]
        return source_chains

    def change_settings(self, source_chain):
        self.chain = source_chain
        self.w3 = AsyncWeb3(AsyncHTTPProvider(random.choice(RPC[self.chain]["rpc"]),
                                              request_kwargs=self.request_kwargs),
                            middlewares=[async_geth_poa_middleware],
                            )
        self.explorer = RPC[self.chain]["explorer"]
        self.token = RPC[self.chain]["token"]

    async def check_balance_on_destination(self, check: bool, dst_chain: str, amount_to_check: float):
        if not check:
            return True
        dst_balance = await self.check_native_balance(dst_chain)
        if dst_balance >= amount_to_check:
            return False
        return True

    async def calculate_transfer_amount(self, min_amount, max_amount, decimal, all_amount,
                                        min_percent, max_percent, save_funds):
        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        if all_amount:
            save_funds_wei = self.w3.to_wei(random.uniform(*save_funds), 'ether')
            save_funds = self.w3.from_wei(save_funds_wei, 'ether')
            amount -= save_funds
            amount_wei -= save_funds_wei

        return amount_wei, amount, balance

    async def bridge_logic(self, source_chain, destination_chain, amount_wei, amount, balance):
        logger.info(f'[{self.account_id}][{self.address}] Start transfer {amount} ETH from {source_chain} to OKX')

        if not self.okx_address:
            logger.error(f'[{self.account_id}][{self.address}] OKX address is not specified for wallet')
            raise ValueError('OKX address is not specified for wallet')

        tx_data = await self.get_tx_data(amount_wei)

        tx_data.update({"to": self.w3.to_checksum_address(self.okx_address)})
        await self.send_tx(tx_data)

    @retry
    @check_gas
    async def transfer_eth(
            self,
            from_chains: List[str],
            min_amount: float, max_amount: float, decimal: int,
            all_amount: bool, min_percent: int, max_percent: int,
            save_funds: List[float], check_balance_on_dest: bool, check_amount: float,
            min_required_amount: float, destination_chains: List[str] = None,
            bridge_from_all_chains: bool = False, sleep_between_transfers=None,
            wait_unlimited_time=False, sleep_between_attempts=(120, 300)):

        if not destination_chains:
            destination_chains = ["scroll"]
        destination_chain = random.choice(destination_chains)
        need_bridge = await self.check_balance_on_destination(check_balance_on_dest, destination_chain, check_amount)
        if not need_bridge:
            logger.info(
                f"[{self.account_id}][{self.address}] Skip bridge. Balance in {destination_chain.capitalize()} "
                f"is greater than {check_amount}"
            )
            return

        # wait unlimited time handle
        while True:
            source_chains = await self.find_chains_with_max_balance(from_chains, min_required_amount)
            if not source_chains:
                if wait_unlimited_time:
                    logger.info(f'[{self.account_id}][{self.address}] Waiting money for bridge '
                                f'[{self.__class__.__name__}]')
                    await sleep(*sleep_between_attempts, message="Sleep before next attempt")
                    continue
                else:
                    logger.warning(f'[{self.account_id}][{self.address}] No chains with required balance. Skip module')
                    return
            break

        for source_chain in source_chains:
            self.change_settings(source_chain)

            amount_wei, amount, balance = await self.calculate_transfer_amount(min_amount=min_amount,
                                                                               max_amount=max_amount,
                                                                               decimal=decimal,
                                                                               all_amount=all_amount,
                                                                               min_percent=min_percent,
                                                                               max_percent=max_percent,
                                                                               save_funds=save_funds)

            if amount <= 0:
                logger.error(f"[{self.account_id}][{self.address}] Save_funds is greater than amount")
                raise ValueError('Save_funds is greater than amount')

            await self.bridge_logic(source_chain, destination_chain, amount_wei, amount, balance)
            if not bridge_from_all_chains:
                break
            await sleep(*sleep_between_transfers,
                        message=f"[{self.account_id}][{self.address}] Sleep before next transfer")


    @retry
    @check_gas
    async def transfer_erc20(self, token_contract, chain):
        self.change_settings(chain)
        contract = self.get_contract(self.w3.to_checksum_address(token_contract), ERC20_ABI)

        balance = await contract.functions.balanceOf(self.address).call()
        if balance > 0:
            tx_data = await self.get_tx_data()
            transaction = await contract.functions.transfer(
                self.okx_address,
                balance).build_transaction(tx_data)
            await self.send_tx(transaction)
        else:
            logger.warning(f'[{self.account_id}][{self.address}] No balance of token')
