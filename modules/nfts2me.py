import random

from loguru import logger
from config import NFTS2ME_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Minter(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

    @retry
    @check_gas
    async def mint_nft(self, contracts):

        logger.info(f"[{self.account_id}][{self.address}] Mint NFT on NFTS2ME")
        nfts = contracts.copy()

        while len(nfts):
            contr, method = random.choice(contracts)
            contract = self.get_contract(contr, NFTS2ME_ABI)
            balance = await contract.functions.balanceOf(self.address).call()
            mint_price = await contract.functions.mintPrice().call()
            if balance == 0:
                tx_data = await self.get_tx_data(value=mint_price)
                if method == 'mint':
                    transaction = await contract.functions.mint().build_transaction(tx_data)
                elif method == 'mintRandomTo':
                    transaction = await contract.functions.mintRandomTo(self.address, 1).build_transaction(tx_data)
                else:
                    raise ValueError('Unknown mint method')
                await self.send_tx(transaction)
                break
            nfts.remove((contr, method))
        else:
            logger.info(f"[{self.account_id}][{self.address}] All nfts minted. Skip module")
