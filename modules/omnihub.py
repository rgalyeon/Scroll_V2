from loguru import logger
from config import OMNIHUB_CONTRACT, OMNIHUB_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
import string
import random


class OmniHub(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

        self.contract = self.get_contract(OMNIHUB_CONTRACT, OMNIHUB_ABI)

    @retry
    @check_gas
    async def deploy(self) -> None:
        logger.info(f"[{self.account_id}][{self.address}] Deploy NFT on OmniHub")

        characters = string.ascii_letters

        name_length = random.randint(5, 12)
        ticker_length = random.randint(3, 5)
        name = ''.join(random.choice(characters) for _ in range(name_length))
        ticker = ''.join(random.choice(characters) for _ in range(ticker_length)).upper()
        supply = random.randint(100, 2000)

        value = 0.0001
        tx_data = await self.get_tx_data(self.w3.to_wei(value, 'ether'))

        transaction = await self.contract.functions.deploy(
            name, ticker, 0, supply
        ).build_transaction(tx_data)

        await self.send_tx(transaction)
