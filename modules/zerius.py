import random
from typing import List

from loguru import logger

from config import ZERIUS_CONTRACT, ZERIUS_ABI, ZERO_ADDRESS
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class Zerius(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

        self.contract = self.get_contract(ZERIUS_CONTRACT, ZERIUS_ABI)

        self.chain_ids = {
            "arbitrum": 110,
            "optimism": 111,
            "polygon": 109,
            "bsc": 102,
            "avalanche": 106,
        }

    async def get_nft_id(self, txn_hash: str):
        receipts = await self.w3.eth.get_transaction_receipt(txn_hash)

        nft_id = int(receipts["logs"][0]["topics"][-1].hex(), 0)

        return nft_id

    async def get_estimate_fee(self, chain: str, nft_id: int):
        fee = await self.contract.functions.estimateSendFee(
            self.chain_ids[chain],
            self.address,
            nft_id,
            False,
            "0x"
        ).call()

        return int(fee[0] * 1.2)

    @retry
    @check_gas
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Zerius NFT")

        mint_fee = await self.contract.functions.mintFee().call()

        tx_data = await self.get_tx_data(mint_fee)

        transaction = await self.contract.functions.mint().build_transaction(tx_data)

        # TODO need fix

        signed_txn = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())

        return txn_hash.hex()

    @retry
    @check_gas
    async def bridge(self, chain: List, mint_nft, sleep_from: int, sleep_to: int):
        chain_id = random.choice(chain)

        nft_id = await self.get_nft_id(mint_nft)

        await sleep(sleep_from, sleep_to)

        l0_fee = await self.get_estimate_fee(chain_id, nft_id)

        base_bridge_fee = await self.contract.functions.bridgeFee().call()

        tx_data = await self.get_tx_data(l0_fee + base_bridge_fee)

        transaction = await self.contract.functions.sendFrom(
            self.address,
            self.chain_ids[chain_id],
            self.address,
            nft_id,
            ZERO_ADDRESS,
            ZERO_ADDRESS,
            "0x0001000000000000000000000000000000000000000000000000000000000003d090"
        ).build_transaction(tx_data)

        await self.send_tx(transaction)

    async def mint_and_bridge(self, chain, sleep_from, sleep_to):
        mint_nft = await self.mint()

        await self.bridge(chain, mint_nft, sleep_from, sleep_to)
