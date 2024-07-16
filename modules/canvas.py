import aiohttp
from loguru import logger
from config import CANVAS_CONTRACT, CANVAS_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry, badges_checker
from .account import Account
import string
import random
from fake_useragent import UserAgent


class Canvas(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="scroll")

        ua = UserAgent().getRandom

        self.headers = {
            "Referer": "https://scroll.io/",
            "Sec-Ch-Ua": "",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": ua["os"],
            "User-Agent": ua['useragent']
        }

    @staticmethod
    async def generate_random_nickname(name, contract):
        characters = string.ascii_letters + string.digits + "_"

        if not name:
            length = random.randint(10, 15)
            name = ''.join(random.choice(characters) for _ in range(length))

        while True:
            username_used = await contract.functions.isUsernameUsed(name).call()

            if not username_used:
                return name

            length = random.randint(10, 15)
            name = ''.join(random.choice(characters) for _ in range(length))

    @badges_checker
    @retry
    @check_gas
    async def mint_eth_badge(self):
        badge_address = "0x3dacAd961e5e2de850F5E027c70b56b5Afa5DfeD"
        link = f"https://canvas.scroll.cat/badge/claim?badge={badge_address}&recipient={self.address}"

        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=self.headers, proxy=self.proxy) as response:
                response_data = await response.json()

        if response_data['message'] == 'success':
            tx_data = await self.get_tx_data()
            tx_data['to'] = "0x39fb5E85C7713657c2D9E869E974FF1e0B06F20C"
            tx_data['data'] = response_data['tx']['data']

            signed_txn = await self.sign(tx_data)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Error on mint")
            return

    @badges_checker
    @retry
    @check_gas
    async def mint_main_badge(self, ref_code=""):
        contract = self.get_contract(CANVAS_CONTRACT, CANVAS_ABI)
        name = None

        if str.isalpha(self.account_id) and 4 <= len(self.account_id) <= 15:
            name = self.account_id

        name = await self.generate_random_nickname(name, contract)

        value = 0.0005 if ref_code else 0.001

        badge = "0x3dacAd961e5e2de850F5E027c70b56b5Afa5DfeD"
        check_link = f"https://canvas.scroll.cat/badge/check?badge={badge}&recipient={self.address}"
        sig_link = f"https://canvas.scroll.cat/code/{ref_code}/sig/{self.address}"

        minted = await contract.functions.isProfileMinted(self.address).call()
        if minted:
            logger.info(f"[{self.account_id}][{self.address}] Already minted")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(check_link, headers=self.headers, proxy=self.proxy) as response:
                response_data = await response.json()

        if response_data["message"] != "success" or response_data["eligibility"] is not True:
            logger.error(f"[{self.account_id}][{self.address}] Address not eligible for mint")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(sig_link, headers=self.headers, proxy=self.proxy) as response:
                response_data = await response.json()

        sig = response_data["signature"]

        tx_data = await self.get_tx_data(self.w3.to_wei(value, "ether"))
        transaction = await contract.functions.mint(
            name,
            sig
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())
