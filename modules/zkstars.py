import random

from loguru import logger
from config import ZKSTARS_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class ZkStars(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

    @retry
    @check_gas
    async def mint(self, contracts: list, min_mint: int, max_mint: int, mint_all: bool, sleep_from: int, sleep_to: int):
        quantity_mint = random.randint(min_mint, max_mint)

        contracts = contracts if mint_all is True else random.sample(contracts, quantity_mint)

        logger.info(f"[{self.account_id}][{self.address}] Mint {quantity_mint} ZkStars NFT")

        for _, contract in enumerate(contracts, start=1):
            mint_contract = self.get_contract(self.w3.to_checksum_address(contract), ZKSTARS_ABI)

            mint_price = await mint_contract.functions.getPrice().call()
            nft_id = await mint_contract.functions.name().call()

            logger.info(f"[{self.account_id}][{self.address}] Mint #{nft_id} NFT")

            tx_data = await self.get_tx_data()
            tx_data.update({"value": mint_price})

            transaction = await mint_contract.functions.safeMint(
                self.w3.to_checksum_address("0xE022adf1735642DBf8684C05f53Fe0D8339F5663")
            ).build_transaction(tx_data)

            await self.send_tx(transaction)

            if _ != len(contracts):
                await sleep(sleep_from, sleep_to, message="Sleep between next mint")
