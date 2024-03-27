from loguru import logger
from config import AMBIENT_CONTRACT, AMBIENT_ABI, SCROLL_TOKENS, ZERO_ADDRESS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from eth_abi import abi


class Ambient(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

        self.contract = self.get_contract(AMBIENT_CONTRACT, AMBIENT_ABI)

    async def get_min_amount_out(self, from_token_name, to_token_name, from_token_amount, slippage):
        if from_token_name in {'ETH', 'USDC'} and to_token_name in {'USDC', 'ETH'}:
            abi_ = [{"inputs": [], "name": "latestAnswer", "outputs":
                    [{"internalType": "int256", "name": "", "type": "int256"}],
                    "stateMutability": "view", "type": "function"}]
            w3 = self.get_w3('ethereum')
            contract = w3.eth.contract(address=w3.to_checksum_address('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419'),
                                       abi=abi_)
            eth_price = await contract.functions.latestAnswer().call() / 10 ** 8

            prices = {'ETH': eth_price, 'USDC': 1}
            amount_in_usd = prices[from_token_name] * float(from_token_amount)
            min_amount_out = (amount_in_usd / prices[to_token_name])

            decimals = 18 if to_token_name == 'ETH' else (await self.get_balance(SCROLL_TOKENS[to_token_name]))[
                'decimal']

            min_amount_out_in_wei = self.w3.to_wei(min_amount_out, 'ether' if decimals == 18 else 'mwei')

            return int(min_amount_out_in_wei - (min_amount_out_in_wei / 100 * slippage))
        else:
            raise ValueError('Supported only ETH and USDC')

    @retry
    @check_gas
    async def swap(
            self,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: float,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        from_token_address = self.w3.to_checksum_address(SCROLL_TOKENS[from_token])
        to_token_address = self.w3.to_checksum_address(SCROLL_TOKENS[to_token])

        amount_wei, amount, balance = await self.get_amount(
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(
            f"[{self.account_id}][{self.address}] Swap on Ambient – {from_token} -> {to_token} | {amount} {from_token}"
        )

        max_sqrt_price = 21267430153580247136652501917186561137
        min_sqrt_price = 65537
        pool_idx = 420
        reserve_flags = 0
        tip = 0

        min_amount_out = await self.get_min_amount_out(from_token, to_token, amount, slippage)

        if from_token != 'ETH':
            await self.approve(amount_wei, from_token_address, self.w3.to_checksum_address(AMBIENT_CONTRACT))

        encode_data = abi.encode(
            ['address', 'address', 'uint16', 'bool', 'bool', 'uint256', 'uint8', 'uint256', 'uint256', 'uint8'], [
                ZERO_ADDRESS,
                to_token_address if from_token == 'ETH' else from_token_address,
                pool_idx,
                True if from_token == 'ETH' else False,
                True if from_token == 'ETH' else False,
                amount_wei,
                tip,
                max_sqrt_price if from_token == 'ETH' else min_sqrt_price,
                min_amount_out,
                reserve_flags
            ]
        )

        tx_data = await self.get_tx_data(value=amount_wei if from_token == 'ETH' else 0)
        transaction = await self.contract.functions.userCmd(
            1,
            encode_data
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())
