import asyncio

import aiohttp

from loguru import logger
from config import OWLTO_CHECKIN_CONTRACT, OWLTO_CHECKIN_ABI, RPC
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
import time


class Owlto(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info, chain="scroll")

        self.contract = self.get_contract(OWLTO_CHECKIN_CONTRACT, OWLTO_CHECKIN_ABI)

    @retry
    @check_gas
    async def check_in(self, ref: str):
        logger.info(f"[{self.account_id}][{self.address}] Start Owlto Check-in")

        date = time.strftime("%Y%m%d")

        if ref != "":
            ref = f"https://owlto.finance/?ref={ref}"
        else:
            ref = "https://owlto.finance"

        tx_data = await self.get_tx_data()
        transaction = await self.contract.functions.checkIn(int(date)).build_transaction(tx_data)
        await self.send_tx(transaction)

        headers = {
            "authority": "owlto.finance",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "dnt": "1",
            "referer": ref,
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "MOCK_USER_AGENT",
        }

        params = {
            "hash": txn_hash.hex(),
            "chainId": str(RPC[self.chain]["chain_id"]),
            "userAddress": self.address,
        }

        n_attempt = 3
        while n_attempt:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://owlto.finance/api/lottery/maker/sign/in", params=params,
                                           headers=headers, proxy=self.proxy) as response:
                        response_data = await response.json()
                        if response_data['message'] == 'success':
                            logger.success(f"[{self.account_id}][{self.address}] Successfully check-in on site")
                            break
                        elif response_data['message'] == "Repeat check-in":
                            logger.warning(f"[{self.account_id}][{self.address}] {response_data['message']}")
                            break
                        else:
                            logger.error(f"[{self.account_id}][{self.address}] {response_data['message']}")
                await asyncio.sleep(20)
            except Exception as e:
                logger.error(f'[{self.account_id}][{self.address}] Error in button check-in: {e}')
                if n_attempt - 1:
                    logger.info(f'[{self.account_id}][{self.address}] Retry owlto site check-in')
            n_attempt -= 1
