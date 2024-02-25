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
            if balance == 0:
                tx_data = await self.get_tx_data()
                if method == 'mint':
                    transaction = await contract.functions.mint().build_transaction(tx_data)
                elif method == 'mintRandomTo':
                    transaction = await contract.functions.mintRandomTo(self.address, 1).build_transaction(tx_data)
                else:
                    raise ValueError('Unknown mint method')
                signed_txn = await self.sign(transaction)
                txn_hash = await self.send_raw_transaction(signed_txn)
                await self.wait_until_tx_finished(txn_hash.hex())
                break
            nfts.remove(contr)
        else:
            logger.info(f"[{self.account_id}][{self.address}] All nfts minted. Skip module")
