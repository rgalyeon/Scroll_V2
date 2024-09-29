from loguru import logger
from config import AAVE_CONTRACT, AAVE_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from utils.sleeping import sleep
import random


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
                     max_percent,
                     required_amount_for_withdraw):

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
            await sleep(sleep_from, sleep_to, message=f"[{self.account_id}][{self.address}] Sleep before withdrawal")
            await self.withdraw(0, 0, 6, True, 100, 100, 0)

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

        await self.send_tx(transaction)

    async def get_deposit_amount(self):
        aave_weth_contract = self.get_contract(self.aave_weth_contract)

        amount = await aave_weth_contract.functions.balanceOf(self.address).call()

        return amount

    @retry
    @check_gas
    async def withdraw(self, min_amount, max_amount, decimal, all_amount, min_percent, max_percent,
                       min_required_amount) -> None:
        balance = await self.get_deposit_amount()
        random_amount = round(random.uniform(min_amount, max_amount), decimal)
        random_percent = random.randint(min_percent, max_percent)
        percent = 1 if random_percent == 100 else random_percent / 100
        amount_wei = int(balance * percent) if all_amount else self.w3.to_wei(random_amount, "ether")
        amount = self.w3.from_wei(int(balance * percent), "ether") if all_amount else random_amount

        if not all_amount and amount_wei > balance:
            amount_wei = balance
            amount = self.w3.from_wei(amount_wei, 'ether')

        if amount < min_required_amount:
            logger.info(f"[{self.account_id}][{self.address}] Amount < min required amount. Skip module")
            return

        if amount > 0:
            logger.info(
                f"[{self.account_id}][{self.address}] Make withdraw from Aave | " +
                f"{self.w3.from_wei(amount_wei, 'ether')} ETH"
            )

            await self.approve(amount, self.aave_weth_contract, AAVE_CONTRACT)

            tx_data = await self.get_tx_data()

            transaction = await self.contract.functions.withdrawETH(
                self.w3.to_checksum_address("0x11fCfe756c05AD438e312a7fd934381537D3cFfe"),
                amount_wei,
                self.address
            ).build_transaction(tx_data)

            await self.send_tx(transaction)
        else:
            logger.warning(f"[{self.account_id}][{self.address}] Deposit not found. Skip module")
