import json

import aiohttp
from loguru import logger
from config import CANVAS_CONTRACT, CANVAS_ABI
from config import (ETH_BADGE, AMBIENT_SWAPOOOR, AMBIENT_PROVIDOOR, AMBIENT_FILLOOR,
                    AMBIENT_YEET, ZEBRA_BADGE, SCROLLY_BADGE, PENCIL_S_BADGE, PENCIL_P_BADGE,
                    SCROLLER_AGENT_BADGE, PASSPORT_XYZ_BADGE, SYMBIOSIS_PROFESSIONAL, TRUSTA_MEDIA_BADGE,
                    SYMBIOSIS_WHALE, SYMBIOSIS_SWAPPER, SYMBIOSIS_BEGINNER, XHS_BADGE, SCROLL_BOOSTER,
                    OMNIHUB_BADGE, TRUSTA_POH_BADGE, RETRO_BRIDGE_BADGE, SYMBIOSIS_PRO_SWAPPER,
                    SMILECOBRA_BADGE, SCROLL_EXPLORER, SYMBIOSIS_BRIDGE_1, SYMBIOSIS_BRIDGE_2,
                    SYMBIOSIS_BRIDGE_3, SYMBIOSIS_BRIDGE_4, SYMBIOSIS_BRIDGE_5, SYMBIOSIS_BRIDGE_6,
                    SYMBIOSIS_BRIDGE_7, SYMBIOSIS_BRIDGE_8, SYMBIOSIS_BRIDGE_9, SYMBIOSIS_BRIDGE_10)
from utils.gas_checker import check_gas
from utils.helpers import retry, badges_checker, sleep
from .account import Account
import string
import random
from fake_useragent import UserAgent
from eth_abi import decode, encode


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

        if not name or any(char.isdigit() for char in name):
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
    async def mint_main_badge(self, ref_codes=""):
        logger.info(f"[{self.account_id}][{self.address}] Mint Canvas Main Badge")

        contract = self.get_contract(CANVAS_CONTRACT, CANVAS_ABI)
        name = None

        str_name = str(self.account_id)
        if str.isalpha(str_name) and 4 <= len(str_name) <= 15:
            name = str_name

        name = await self.generate_random_nickname(name, contract)

        value = 0.0005 if ref_codes else 0.001

        ref_code = random.choice(ref_codes)
        badge = "0x3dacAd961e5e2de850F5E027c70b56b5Afa5DfeD"
        check_link = f"https://canvas.scroll.cat/badge/check?badge={badge}&recipient={self.address}"
        sig_link = f"https://canvas.scroll.cat/code/{ref_code}/sig/{self.address}"

        profile = await contract.functions.getProfile(self.address).call()
        minted = await contract.functions.isProfileMinted(profile).call()
        if minted:
            logger.info(f"[{self.account_id}][{self.address}] Already minted")
            return False

        async with aiohttp.ClientSession() as session:
            async with session.get(check_link, headers=self.headers, proxy=self.proxy) as response:
                response_data = await response.json()

        if response_data["message"] != "success" or response_data["eligibility"] is not True:
            logger.error(f"[{self.account_id}][{self.address}] Address not eligible for mint")
            return False

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

        return True

    async def mint_all_badges(self, sleep_from, sleep_to, random_badge, ref_codes=""):
        logger.info(f"[{self.account_id}][{self.address}] Start mint All badges")

        badges = [
            ETH_BADGE, AMBIENT_SWAPOOOR, AMBIENT_PROVIDOOR, AMBIENT_FILLOOR,
            AMBIENT_YEET, ZEBRA_BADGE, SCROLLY_BADGE, PENCIL_S_BADGE, PENCIL_P_BADGE,
            SCROLLER_AGENT_BADGE, PASSPORT_XYZ_BADGE, SYMBIOSIS_PROFESSIONAL, TRUSTA_MEDIA_BADGE,
            SYMBIOSIS_WHALE, SYMBIOSIS_SWAPPER, SYMBIOSIS_BEGINNER, XHS_BADGE, SCROLL_BOOSTER,
            OMNIHUB_BADGE, TRUSTA_POH_BADGE, RETRO_BRIDGE_BADGE, SYMBIOSIS_PRO_SWAPPER,
            SMILECOBRA_BADGE, SCROLL_EXPLORER, SYMBIOSIS_BRIDGE_1, SYMBIOSIS_BRIDGE_2,
            SYMBIOSIS_BRIDGE_3, SYMBIOSIS_BRIDGE_4, SYMBIOSIS_BRIDGE_5, SYMBIOSIS_BRIDGE_6,
            SYMBIOSIS_BRIDGE_7, SYMBIOSIS_BRIDGE_8, SYMBIOSIS_BRIDGE_9, SYMBIOSIS_BRIDGE_10,
            ("", "Origin")
        ]

        if random_badge:
            random.shuffle(badges)

        badges.insert(0, ("", "Main"))

        for badge in badges:

            if badge[1] == "Origin":
                minted = await self.mint_scroll_origin_badge()
            elif badge[1] == "Main":
                minted = await self.mint_main_badge(ref_codes)
            else:
                minted = await self.mint_badge(badge)
            if minted:
                await sleep(sleep_from, sleep_to, "Sleep before next mint")

    @badges_checker
    @retry
    @check_gas
    async def mint_scroll_origin_badge(self):
        logger.info(f"[{self.account_id}][{self.address}] Start mint Scroll Origin badge")

        tx_data = await self.get_tx_data()

        data = await self.w3.eth.call({
            "to": "0x74670A3998d9d6622E32D0847fF5977c37E0eC91",
            "data": f"0x2f745c59000000000000000000000000{self.address[2::].lower()}0000000000000000000000000000000000000000000000000000000000000000"
        })

        amount = decode(["uint256"], data)[0]
        if amount <= 0:
            logger.warning(f"[{self.account_id}][{self.address}] Not eligible")
            return False

        token_id = decode(["uint256"], data)[0]
        tx_data["to"] = "0xC47300428b6AD2c7D03BB76D05A176058b47E6B0"
        tx_data["data"] = "0xf17325e7" + encode(
            ["(bytes32,(address,uint64,bool,bytes32,bytes,uint256))"],
            [(bytes.fromhex("d57de4f41c3d3cc855eadef68f98c0d4edd22d57161d96b7c06d2f4336cc3b49"),
             (self.address, 0, False,
              bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"),
              bytes.fromhex(f"0000000000000000000000002dbce60ebeaafb77e5472308f432f78ac3ae07d90000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000004000000000000000000000000074670a3998d9d6622e32d0847ff5977c37e0ec910000000000000000000000{hex(token_id)[2::].rjust(42, '0')}"), 0))]).hex()

        signed_txn = await self.sign(tx_data)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())
        return True

    @retry
    @check_gas
    async def mint_badge(self, badge_data):

        url, name = badge_data

        badge = url.split("=")[1]
        logger.info(f"[{self.account_id}][{self.address}] Start mint {name} badge")

        contract = self.get_contract(badge, CANVAS_ABI)
        has_badge = await contract.functions.hasBadge(self.address).call()
        if has_badge:
            logger.warning(f"[{self.account_id}][{self.address}] Badge {name} already minted")
            return False

        check_link = f"{url}&recipient={self.address}"

        async with aiohttp.ClientSession() as session:
            async with session.get(check_link, headers=self.headers, proxy=self.proxy) as response:
                try:
                    response_data = json.loads(await response.text())
                except json.JSONDecodeError:
                    logger.error(f"[{self.account_id}][{self.address}] Bad response from website")
                    return False

        if not response_data['eligibility']:
            logger.error(f"[{self.account_id}][{self.address}] Not eligible for mint")
            return False

        link = check_link.replace('check', 'claim')

        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=self.headers, proxy=self.proxy) as response:
                try:
                    response_data = json.loads(await response.text())
                except json.JSONDecodeError:
                    logger.error(f"[{self.account_id}][{self.address}] Bad response from website")
                    return False

        if response_data['message'] == 'success':
            tx_data = await self.get_tx_data()
            tx_data['to'] = self.w3.to_checksum_address(response_data['tx']['to'])
            tx_data['data'] = response_data['tx']['data']

            signed_txn = await self.sign(tx_data)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
            return True
        else:
            if 'message' in response_data:
                logger.error(f"[{self.account_id}][{self.address}] Error on mint: {response_data['message']}")
            else:
                logger.error(f"[{self.account_id}][{self.address}] Bad response: {response_data}")
            return False
