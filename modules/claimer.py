import random
from hashlib import sha256

from loguru import logger
from aiohttp import ClientSession
from config import CLAIMER_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from fake_useragent import UserAgent
import json


class Claimer(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")


        self.headers = {
            'accept': 'text/x-component',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'text/plain;charset=UTF-8',
            'next-action': '2ab5dbb719cdef833b891dc475986d28393ae963',
            'origin': 'https://claim.scroll.io',
            'priority': 'u=1, i',
            'referer': 'https://claim.scroll.io/?step=4',
            'user-agent': UserAgent().chrome,
        }

        self.contract = self.get_contract('0xE8bE8eB940c0ca3BD19D911CD3bEBc97Bea0ED62', CLAIMER_ABI)

    async def get_claim_data(self):
        data = f'["{self.address}"]'

        url = 'https://claim.scroll.io/?step=4'
        async with ClientSession() as session:
            async with session.post(url, headers=self.headers, proxy=self.proxy, data=data) as response:
                response = await response.text()

        json_objects = response.splitlines()
        json_object = json_objects[1]
        data = json.loads(json_object[2:])
        return data

    @retry
    @check_gas
    async def claim(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Claim")

        claim_data = await self.get_claim_data()
        if not claim_data:
            logger.warning(f'[{self.account_id}][{self.address}] | Not eligible')
            return

        amount = int(claim_data['amount'])
        claim_status = claim_data['claim_status']
        if not claim_status == 'UNCLAIMED':
            logger.warning(f'[{self.account_id}][{self.address}] | Already claimed')
            return

        proof = claim_data['proof']

        tx_data = await self.get_tx_data()

        transaction = await self.contract.functions.claim(
            self.address,
            amount,
            proof
        ).build_transaction(tx_data)

        await self.send_tx(transaction)



