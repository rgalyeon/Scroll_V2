import random

from loguru import logger
from config import ROCKETSAM_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class RocketSam(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")
        self.current_contract = None

    async def router(self, contracts,
                     min_amount,
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

        await self.deposit(contracts, amount_wei, amount, balance)
        if make_withdraw:
            await sleep(sleep_from, sleep_to, message=f"[{self.account_id}][{self.address}] Sleep before withdrawal")
            await self.withdraw([self.current_contract], sleep_from, sleep_to)

    async def get_deposit_amount(self, contract: str):
        contract = self.get_contract(self.w3.to_checksum_address(contract), ROCKETSAM_ABI)
        amount = await contract.functions.balances(self.address).call()
        return amount

    @retry
    @check_gas
    async def deposit(self, contracts: list, amount_wei, amount, balance):

        logger.info(f"[{self.account_id}][{self.address}] Deposit to RocketSam")

        contract = self.get_contract(self.w3.to_checksum_address(random.choice(contracts)), ROCKETSAM_ABI)
        self.current_contract = contract.address

        fee = await contract.functions.estimateProtocolFee(amount_wei).call()

        tx_data = await self.get_tx_data(amount_wei + fee)

        transaction = await contract.functions.depositWithReferrer(
            self.w3.to_checksum_address("0xE022adf1735642DBf8684C05f53Fe0D8339F5663"),
            amount_wei
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def withdraw(self, contracts: list, sleep_from, sleep_to):
        for _, contract in enumerate(contracts, start=1):
            amount = await self.get_deposit_amount(contract)

            if amount > 0:
                logger.info(
                    f"[{self.account_id}][{self.address}] Make withdraw from RocketSam | " +
                    f"{self.w3.from_wei(amount, 'ether')} ETH"
                )

                contract = self.get_contract(self.w3.to_checksum_address(contract), ROCKETSAM_ABI)

                tx_data = await self.get_tx_data()

                transaction = await contract.functions.withdraw().build_transaction(tx_data)

                signed_txn = await self.sign(transaction)

                txn_hash = await self.send_raw_transaction(signed_txn)

                await self.wait_until_tx_finished(txn_hash.hex())

                if _ != len(contracts):
                    await sleep(sleep_from, sleep_to, message="Sleep between next withdrawal")
            else:
                logger.error(f"[{self.account_id}][{self.address}] Deposit not found")
