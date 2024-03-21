from loguru import logger
from config import AAVE_CONTRACT, AAVE_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from utils.sleeping import sleep


class Aave(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

        self.contract = self.get_contract(AAVE_CONTRACT, AAVE_ABI)
        self.aave_weth_contract = "0xf301805be1df81102c957f6d4ce29d2b8c056b2a"

    async def router(self, min_amount,
                     max_amount,
                     decimal,
                     sleep_from,
                     sleep_to,
                     make_withdraw,
                     all_amount,
                     min_percent,
                     max_percent):

        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        await self.deposit(amount_wei, amount, balance)
        if make_withdraw:
            await sleep(sleep_from, sleep_to)
            await self.withdraw()

    @retry
    @check_gas
    async def deposit(self, amount_wei, amount, balance):

        logger.info(f"[{self.account_id}][{self.address}] Make deposit on AAVE | {amount} ETH")

        undefined = "0x11fCfe756c05AD438e312a7fd934381537D3cFfe"
        tx_data = await self.get_tx_data(amount_wei)
        transaction = await self.contract.functions.depositETH(
            self.w3.to_checksum_address(undefined),
            self.w3.to_checksum_address(self.address),
            0
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

    async def get_deposit_amount(self):
        aave_weth_contract = self.get_contract(self.aave_weth_contract)

        amount = await aave_weth_contract.functions.balanceOf(self.address).call()

        return amount

    @retry
    @check_gas
    async def withdraw(self):
        amount = await self.get_deposit_amount()
        balance = self.w3.from_wei(amount, 'ether')

        if amount > 0:
            logger.info(
                f"[{self.account_id}][{self.address}] Make withdraw {balance} ETH from Aave"
            )

            await self.approve(amount, self.aave_weth_contract, AAVE_CONTRACT)

            tx_data = await self.get_tx_data()

            transaction = await self.contract.functions.withdrawETH(
                self.w3.to_checksum_address("0x11fCfe756c05AD438e312a7fd934381537D3cFfe"),
                amount,
                self.address
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.warning(f"[{self.account_id}][{self.address}] Deposit not found. Skip module")
