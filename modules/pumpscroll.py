import asyncio
from .account import Account
import aiohttp
from fake_useragent import UserAgent
from loguru import logger
from config import PUMPSCROLL_ABI, PUMPSCROLL_CONTRACT, ZERO_ADDRESS
import random
from utils.helpers import retry
from utils.gas_checker import check_gas


class PumpScroll(Account):
    def __init__(self, wallet_info, chain="scroll") -> None:
        super().__init__(wallet_info, chain)

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://scrollpump.xyz",
            "priority": 'u=1, i',
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referrer": "https://scrollpump.xyz/",
            "user-agent": UserAgent(browsers=["chrome"], os=["macos"]).chrome
        }

    async def get_data(self):
        url = "https://api.scrollpump.xyz/api/Airdrop/GetSign"

        data = {'address': self.address}

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url=url,
                headers=self.headers,
                proxy=self.proxy,
                params=data
            )

        if response.status not in [200, 201]:
            raise ValueError('Failed parse supported chains')

        data = await response.json()
        if data["success"]:
            return data["data"]
        else:
            return False

    @retry
    @check_gas
    async def claim_pump(self, refs=None):
        logger.info(f"[{self.account_id}][{self.address}] Start claim ScrollPump tokens")

        contract = self.get_contract(PUMPSCROLL_CONTRACT, PUMPSCROLL_ABI)
        address = self.w3.to_checksum_address(self.address)

        claimed = await contract.functions.claimed(address).call()
        if claimed:
            logger.warning(f"[{self.account_id}][{self.address}] Already claimed PumpScroll tokens")
            return

        claim_data = await self.get_data()
        if not claim_data:
            return logger.info(f"[{self.account_id}][{self.address}] Not eligible")

        tx_data = await self.get_tx_data()
        amount = int(claim_data['amount'])
        signature = claim_data['sign']
        if refs and refs[0]:
            ref = self.w3.to_checksum_address(random.choice(refs))
        else:
            ref = ZERO_ADDRESS

        transaction = await contract.functions.claim(
            amount,
            signature,
            ref
        ).build_transaction(tx_data)

        await self.send_tx(transaction)
