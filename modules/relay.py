import asyncio
from .transfer import Transfer
import aiohttp
from fake_useragent import UserAgent
from config import RPC, ZERO_ADDRESS
from loguru import logger


class Relay(Transfer):
    def __init__(self, wallet_info, from_chains=None) -> None:
        super().__init__(wallet_info, from_chains)

        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referrer": "https://www.relay.link/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "User-Agent": UserAgent(browsers=["chrome"], os=["macos"]).chrome
        }

    async def get_chains(self):
        url = "https://api.relay.link/chains"

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url=url,
                headers=self.headers,
                proxy=self.proxy
            )

        if response.status not in [200, 201]:
            raise ValueError('Failed parse supported chains')

        data = await response.json()
        supported_chains = []
        for chains in data['chains']:
            supported_chains.append(chains['id'])

        return supported_chains

    async def get_bridge_config(self, from_chain, to_chain):
        url = "https://api.relay.link/config"

        params = {
            'originChainId': RPC[from_chain]['chain_id'],
            'destinationChainId': RPC[to_chain]['chain_id'],
            'user': ZERO_ADDRESS,
            'currency': ZERO_ADDRESS,
        }

        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url=url,
                headers=self.headers,
                params=params,
                proxy=self.proxy
            )

            if response.status not in [200, 201]:
                raise ValueError('Failed parse supported chains')

            return await response.json()

    async def get_bridge_data(self, from_chain, to_chain, amount_in_wei):
        url = f"https://api.relay.link/execute/call"

        payload = {
            "user": self.address,
            "originChainId": RPC[from_chain]['chain_id'],
            "destinationChainId": RPC[to_chain]['chain_id'],
            "txs": [
                {
                    "to": self.address,
                    "value": amount_in_wei,
                    "data": "0x"
                }
            ],

            "source": "relay.link"
        }

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=url,
                headers=self.headers,
                json=payload,
                proxy=self.proxy
            )

            if response.status not in [200, 201]:
                raise ValueError('Failed parse bridge data')

            return await response.json()

    async def bridge_logic(self, source_chain, destination_chain, amount_wei, amount, balance):
        logger.info(
            f"[{self.account_id}][{self.address}] Bridge {self.chain} –> {destination_chain} | {amount} ETH"
        )

        chain_ids = await self.get_chains()
        if RPC[source_chain]['chain_id'] not in chain_ids or RPC[destination_chain]['chain_id'] not in chain_ids:
            raise ValueError(f'Bridge from {source_chain} to {destination_chain} does not supported')

        bridge_config = await self.get_bridge_config(source_chain, destination_chain)
        bridge_data = await self.get_bridge_data(source_chain, destination_chain, amount_wei)

        if bridge_config['enabled']:
            max_amount = float(bridge_config['solver']['capacityPerRequest'])

            if amount <= max_amount:

                tx_data = await self.get_tx_data(amount_wei)

                tx_data['to'] = self.w3.to_checksum_address(bridge_data["steps"][0]['items'][0]['data']['to'])
                tx_data['data'] = bridge_data["steps"][0]['items'][0]['data']['data']

                await self.send_tx(tx_data)
