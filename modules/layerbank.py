from loguru import logger
from config import LAYERBANK_CONTRACT, LAYERBANK_WETH_CONTRACT, LAYERBANK_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account
import random


class LayerBank(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

        self.contract = self.get_contract(LAYERBANK_CONTRACT, LAYERBANK_ABI)

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
            await sleep(sleep_from, sleep_to, message=f"[{self.account_id}][{self.address}] Sleep before withdrawal")
            await self.withdraw(0, 0, 6, True, 100, 100, 0)

    async def get_deposit_amount(self):
        weth_contract = self.get_contract(LAYERBANK_WETH_CONTRACT)

        amount = await weth_contract.functions.balanceOf(self.address).call()

        return amount

    @retry
    @check_gas
    async def deposit(self, amount_wei, amount, balance) -> None:

        logger.info(f"[{self.account_id}][{self.address}] Make deposit on LayerBank | {amount} ETH")

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await self.contract.functions.supply(
            self.w3.to_checksum_address(LAYERBANK_WETH_CONTRACT),
            amount_wei,
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

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

        if amount_wei > 0:
            logger.info(
                f"[{self.account_id}][{self.address}] Make withdraw from LayerBank | " +
                f"{self.w3.from_wei(amount_wei, 'ether')} ETH"
            )

            await self.approve(amount_wei, LAYERBANK_WETH_CONTRACT, LAYERBANK_CONTRACT)

            tx_data = await self.get_tx_data()

            transaction = await self.contract.functions.redeemUnderlying(
                self.w3.to_checksum_address(LAYERBANK_WETH_CONTRACT),
                amount_wei,
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Deposit not found")
