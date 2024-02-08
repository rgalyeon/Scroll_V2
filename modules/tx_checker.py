import asyncio
import random

from eth_typing import ChecksumAddress
from loguru import logger
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.middleware import async_geth_poa_middleware
from eth_account import Account as EthereumAccount
from tabulate import tabulate
from utils.password_handler import get_wallet_data

from config import RPC


async def get_nonce(address: ChecksumAddress):
    web3 = AsyncWeb3(
        AsyncHTTPProvider(random.choice(RPC["scroll"]["rpc"])),
        middlewares=[async_geth_poa_middleware],
    )

    nonce = await web3.eth.get_transaction_count(address)

    return nonce


async def check_tx():
    tasks = []

    logger.info("Start transaction checker")

    accounts = [data['private_key'] for _, data in get_wallet_data().items()]
    for _id, pk in enumerate(accounts, start=1):
        account = EthereumAccount.from_key(pk)

        tasks.append(asyncio.create_task(get_nonce(account.address), name=account.address))

    await asyncio.gather(*tasks)

    table = [[k, i.get_name(), i.result()] for k, i in enumerate(tasks, start=1)]

    headers = ["#", "Address", "Nonce"]

    print(tabulate(table, headers, tablefmt="github"))
