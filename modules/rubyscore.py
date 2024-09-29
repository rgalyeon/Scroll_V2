from loguru import logger
from config import RUBYSCORE_CONTRACT, RUBYSCORE_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Rubyscore(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

        self.contract = self.get_contract(RUBYSCORE_CONTRACT, RUBYSCORE_ABI)

    @retry
    @check_gas
    async def vote(self):
        logger.info(f"[{self.account_id}][{self.address}] Start vote on Rubyscore")

        tx_data = await self.get_tx_data()
        transaction = await self.contract.functions.vote().build_transaction(tx_data)
        await self.send_tx(transaction)
