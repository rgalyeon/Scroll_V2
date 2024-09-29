import aiohttp
from loguru import logger
from .transfer import Transfer
from config import RPC


class Nitro(Transfer):
    def __init__(self, wallet_info, from_chains) -> None:
        super().__init__(wallet_info, from_chains=from_chains)

    async def get_quote(self, amount: int, destination_chain: str):
        url = "https://api-beta.pathfinder.routerprotocol.com/api/v2/quote"

        params = {
            "fromTokenAddress": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            "toTokenAddress": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            "amount": amount,
            "fromTokenChainId": str(RPC[self.chain]["chain_id"]),
            "toTokenChainId": str(RPC[destination_chain]["chain_id"]),
            "partnerId": 1
        }

        async with aiohttp.ClientSession() as session:
            response = await session.get(url=url, params=params, proxy=self.proxy)

            transaction_data = await response.json()

            return transaction_data

    async def build_transaction(self, params: dict):
        url = "https://api-beta.pathfinder.routerprotocol.com/api/v2/transaction"

        async with aiohttp.ClientSession() as session:
            response = await session.post(url=url, json=params, proxy=self.proxy)

            transaction_data = await response.json()

            return transaction_data

    async def bridge_logic(self, source_chain: str, destination_chain: str, amount_wei, amount, balance):

        logger.info(
            f"[{self.account_id}][{self.address}] Start bridge Nitro – {source_chain.capitalize()} -> " +
            f"{destination_chain.capitalize()} | {amount} ETH"
        )

        quote = await self.get_quote(amount_wei, destination_chain)
        quote.update({"senderAddress": self.address, "receiverAddress": self.address})

        transaction_data = await self.build_transaction(quote)

        tx_data = await self.get_tx_data()
        tx_data.update(
            {
                "from": self.w3.to_checksum_address(transaction_data["txn"]["from"]),
                "to": self.w3.to_checksum_address(transaction_data["txn"]["to"]),
                "value": int(transaction_data["txn"]["value"], 16),
                "data": transaction_data["txn"]["data"],
            }
        )

        await self.send_tx(tx_data)
