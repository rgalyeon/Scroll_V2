import os
import time
import json
import base64
import random
import asyncio

from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector
from datetime import datetime, timezone
from utils.sleeping import sleep
from utils.stark_signature import pedersen_hash, sign, EC_ORDER, private_to_stark_key
from utils.eth_coder import decrypt_with_private_key, get_public_key, encrypt_with_public_key
from eth_account.messages import encode_defunct
from loguru import logger
from .transfer import Transfer

REGISTER_DATA = {
    "types": {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"}
        ],
        "rhino.fi": [
            {"type": "string", "name": "action"},
            {"type": "string", "name": "onlySignOn"}
        ]
    },
    "domain": {
        "name": "rhino.fi",
        "version": "1.0.0"
    },
    "primaryType": "rhino.fi",
    "message": {
        "action": "Access your rhino.fi account",
        "onlySignOn": "app.rhino.fi"
    }
}


class RhinoFi(Transfer):
    def __init__(self, wallet_info):
        super().__init__(wallet_info)

        self.nonce, self.signature = None, None
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.session = ClientSession(connector=ProxyConnector.from_url(f"{self.proxy}", verify_ssl=False)
                                     if self.proxy else TCPConnector(verify_ssl=False))

    def get_authentication_data(self):
        date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S")
        nonce = f"{time.time():.3f}"

        text = (f"To protect your rhino.fi privacy we ask you to sign in with your wallet to see your data.\n"
                f"Signing in on {date} GMT. For your safety, only sign this message on rhino.fi!")

        nonse_str = f"v3-{nonce}"
        text_hex = "0x" + text.encode('utf-8').hex()
        text_encoded = encode_defunct(hexstr=text_hex)
        signature = self.w3.eth.account.sign_message(text_encoded,
                                                     private_key=self.private_key).signature

        return nonse_str, self.w3.to_hex(signature)

    async def make_request(self, method: str = 'GET', url: str = None, headers: dict = None, params: dict = None,
                           data: str = None, json: dict = None):
        def get_user_agent():
            random_version = f"{random.uniform(520, 540):.2f}"
            return (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random_version} (KHTML, like Gecko)'
                    f' Chrome/119.0.0.0 Safari/{random_version} Edg/119.0.0.0')

        if headers is None:
            headers = {}
        headers.update({'User-Agent': get_user_agent()})
        async with self.session.request(method=method, url=url, headers=headers, data=data, json=json,
                                        params=params) as response:
            data = await response.json()
            if response.status in [200, 201]:
                return data
            raise ValueError(f"Bad request to {self.__class__.__name__} API: {response.status}")

    def make_headers(self):
        data_to_headers = f'{{"signature":"{self.signature}","nonce":"{self.nonce}"}}'

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "utf-8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://app.rhino.fi",
            "Referer": "https://app.rhino.fi/",
            "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Authorization": f"EcRecover {base64.b64encode(data_to_headers.encode('utf-8')).decode('utf-8')}"
        }

        return headers

    async def get_user_config(self):

        url = "https://api.rhino.fi/v1/trading/r/getUserConf"

        data = {
            'nonce': self.nonce,
            'signature': self.signature
        }

        while True:
            try:
                data = await self.make_request(method='POST', url=url, headers=self.headers, json=data)
                return data
            except:
                import traceback

                traceback.print_exc()
                logger.warning(f"[{self.account_id}][{self.address}] Get bad API data")
                await asyncio.sleep(5)

    async def get_vault_id(self):

        url = "https://api.rhino.fi/v1/trading/r/getVaultId"

        data = {
            'nonce': self.nonce,
            'signature': self.signature,
            'token': 'ETH'
        }

        return await self.make_request(method='POST', url=url, headers=self.headers, json=data)

    @staticmethod
    def create_stark_key(dtk_private_key):
        stark_key = private_to_stark_key(int(f"0x{dtk_private_key}", 16) % EC_ORDER)

        return f"0{hex(stark_key)[2:]}"

    def create_dtk(self):
        dtk = os.urandom(32).hex()

        sing_data = self.w3.eth.account.sign_typed_data(self.private_key,
                                                        full_message=REGISTER_DATA).signature

        encryption_key = self.w3.keccak(f"{sing_data.hex()}".encode('utf-8'))

        public_key = get_public_key(encryption_key).hex()

        encrypted_message = encrypt_with_public_key(public_key, json.dumps({"data": dtk}))

        return dtk, encrypted_message

    async def reg_new_acc(self):

        url = 'https://api.rhino.fi/v1/trading/w/register'

        dtk, encrypted_trading_key = self.create_dtk()
        stark_public_key_x = self.create_stark_key(dtk)

        data = {
            "encryptedTradingKey": {
                "dtk": encrypted_trading_key,
                "dtkVersion": "v3"
            },
            "meta":
                {
                    "walletType": "metamask",
                    "campaign": None,
                    "referer": None,
                    "platform": "DESKTOP",
                },
            "nonce": self.nonce,
            "signature": self.signature,
            "starkKey": stark_public_key_x,
        }

        return await self.make_request(method='POST', url=url, headers=self.headers, json=data)

    async def recover_trading_key(self):

        url = 'https://api.rhino.fi/v1/trading/r/recoverTradingKey'

        data = {
            "nonce": self.nonce,
            "signature": self.signature,
            "meta": {
                "ethAddress": self.address,
            }
        }

        return await self.make_request(method='POST', url=url, headers=self.headers, json=data)

    async def recover_dtk(self):
        encrypted_trading_key = (await self.recover_trading_key())['encryptedTradingKey']
        sing_data = self.w3.eth.account.sign_typed_data(self.private_key,
                                                        full_message=REGISTER_DATA).signature
        encryption_private_key = self.w3.keccak(f"{sing_data.hex()}".encode('utf-8')).hex()

        dtk = decrypt_with_private_key(encryption_private_key, encrypted_trading_key)

        return json.loads(dtk)['data']

    async def get_vault_id_and_stark_key(self, deversifi_address):

        url = "https://api.rhino.fi/v1/trading/r/vaultIdAndStarkKey"

        headers = self.make_headers()

        params = {
            "token": 'ETH',
            "targetEthAddress": deversifi_address,
        }

        return await self.make_request(method="GET", url=url, headers=headers, params=params)

    async def get_user_balance(self):

        data = {
            "nonce": self.nonce,
            "signature": self.signature,
            "token": "ETH",
            "fields": [
                "balance",
                "available",
                "updatedAt"
            ]
        }

        url = "https://api.rhino.fi/v1/trading/r/getBalance"

        response = await self.make_request(method="POST", url=url, headers=self.headers, json=data)
        if response:
            return response[0]['available']
        return 0

    async def get_stark_signature(self, amount_in_wei, expiration_timestamp, tx_nonce, receiver_public_key,
                                  receiver_vault_id, sender_vault_id, token_address):

        packed_message = 1  # instruction_type
        packed_message = (packed_message << 31) + int(sender_vault_id)
        packed_message = (packed_message << 31) + int(receiver_vault_id)
        packed_message = (packed_message << 63) + int(amount_in_wei)
        packed_message = (packed_message << 63) + 0
        packed_message = (packed_message << 31) + int(tx_nonce)
        packed_message = (packed_message << 22) + int(expiration_timestamp)

        msg_hash = pedersen_hash(pedersen_hash(int(token_address, 16), int(receiver_public_key, 16)),
                                 int(packed_message))

        stark_dtk_private_key = int(await self.recover_dtk(), 16) % EC_ORDER

        tx_signature = sign(msg_hash=msg_hash, priv_key=stark_dtk_private_key)
        return hex(tx_signature[0]), hex(tx_signature[1])

    async def deposit_to_rhino(self, amount, source_chain_info, chain_from_name: str):
        logger.info(f"[{self.account_id}][{self.address}] Deposit {amount} ETH from {chain_from_name.capitalize()} "
                    f"to Rhino")

        if source_chain_info['enabled']:
            source_chain_address = source_chain_info['contractAddress']
            amount_in_wei = int(amount * 10 ** 18)

            tx_data = await self.get_tx_data(value=amount_in_wei)
            tx_data.update({
                'data': "0xdb6b5246",
                'to': self.w3.to_checksum_address(source_chain_address)
            })

            signed_tx = await self.sign(tx_data)
            tx_hash = await self.send_raw_transaction(signed_tx)

            await self.wait_until_tx_finished(tx_hash.hex())

    async def withdraw_from_rhino(self, rhino_user_config, amount, chain_to_name, dst_address):

        while True:
            await asyncio.sleep(4)
            if int(amount * 10 ** 8) <= int(await self.get_user_balance()):
                logger.info(f"[{self.account_id}][{self.address}] Funds have been received to Rhino")
                break
            logger.info(f"[{self.account_id}][{self.address}] Wait a little, while the funds come into Rhino")
            await asyncio.sleep(1)
            await sleep(90, 120)

        logger.info(f"[{self.account_id}][{self.address}] Withdraw {amount} ETH from Rhino "
                    f"to {chain_to_name.capitalize()}")

        url = "https://api.rhino.fi/v1/trading/bridgedWithdrawals"

        deversifi_address = rhino_user_config["DVF"]['deversifiAddress']
        receiver_vault_id, receiver_public_key = (await self.get_vault_id_and_stark_key(deversifi_address)).values()

        sender_public_key = rhino_user_config['starkKeyHex']
        sender_vault_id = await self.get_vault_id()
        token_address = rhino_user_config['tokenRegistry']['ETH']['starkTokenId']

        expiration_timestamp = int(time.time() / 3600) + 4320
        payload_nonce = random.randint(1, 2 ** 53 - 1)
        tx_nonce = random.randint(1, 2 ** 31 - 1)
        amount_in_wei = int(amount * 10 ** 8)

        r_signature, s_signature = await self.get_stark_signature(amount_in_wei, expiration_timestamp, tx_nonce,
                                                                  receiver_public_key, receiver_vault_id,
                                                                  sender_vault_id, token_address)

        headers = self.make_headers()

        payload = {
            "chain": chain_to_name.upper(),
            "token": "ETH",
            "amount": f"{amount_in_wei}",
            "tx": {
                "amount": amount_in_wei,
                "senderPublicKey": sender_public_key,
                "receiverPublicKey": receiver_public_key,
                "receiverVaultId": receiver_vault_id,
                "senderVaultId": sender_vault_id,
                "signature": {
                    "r": r_signature,
                    "s": s_signature
                },
                "token": token_address,
                "type": "TransferRequest",
                "nonce": tx_nonce,
                "expirationTimestamp": expiration_timestamp
            },
            "nonce": payload_nonce,
            "recipientEthAddress": dst_address,
            "isBridge": False,
        }

        await self.make_request(method='POST', url=url, headers=headers, json=payload)
        await sleep(60, 120)

    async def get_token_balance(self) -> [float, int, str]:

        amount_in_wei = await self.w3.eth.get_balance(self.address)
        return amount_in_wei, amount_in_wei / 10 ** 18

    @staticmethod
    def round_amount(min_amount: float, max_amount: float) -> float:
        decimals = max(len(str(min_amount)) - 1, len(str(max_amount)) - 1)
        return round(random.uniform(min_amount, max_amount), decimals + 2)

    async def bridge_logic(self, source_chain, destination_chain, amount_wei, amount, balance):
        try:

            self.nonce, self.signature = self.get_authentication_data()

            rhino_user_config = await self.get_user_config()

            if not rhino_user_config['isRegistered']:
                await asyncio.sleep(1)

                logger.info(f"[{self.account_id}][{self.address}] Make registration on Rhino")
                await self.reg_new_acc()

                await asyncio.sleep(1)

                logger.success(f"[{self.account_id}][{self.address}] Successfully registered on Rhino")
                rhino_user_config = await self.get_user_config()
            else:
                await asyncio.sleep(1)

                logger.info(f"[{self.account_id}][{self.address}]Already registered on Rhino")

            await asyncio.sleep(1)

            _, balance = await self.get_token_balance()

            if amount < balance:

                source_chain_info = rhino_user_config['DVF']['bridgeConfigPerChain'][self.chain.upper()]

                await asyncio.sleep(1)

                await self.deposit_to_rhino(amount, source_chain_info, self.chain)

                await asyncio.sleep(1)

                dst_address = self.address

                await self.withdraw_from_rhino(rhino_user_config, amount, destination_chain, dst_address)

                logger.success(f"[{self.account_id}][{self.address}] Successfully bridged {amount} "
                               f"from {self.chain} to {destination_chain}")
                return True
            else:
                logger.info(f"[{self.account_id}][{self.address}] Insufficient balance in {self.chain}")
        except Exception as error:
            raise ValueError(f"Rhino error: {error}")
        finally:
            await self.session.close()

    async def withdraw_all(self, dst_chain):
        rhino_user_config = await self.get_user_config()
        amount = int(await self.get_user_balance()) / (10 ** 8)
        await self.withdraw_from_rhino(rhino_user_config, amount, dst_chain, self.address)
