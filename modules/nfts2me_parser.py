import asyncio
import json
import random

import aiohttp
from utils.scrollscan_api import make_api_url
from utils.helpers import retry
from config import NFTS2ME_CREATOR_CONTRACT, RPC
import pandas as pd
from web3 import AsyncWeb3
from web3.middleware import async_geth_poa_middleware
from config import NFTS2ME_MAIN_ABI, NFTS2ME_CONTRACTS_PATH
from loguru import logger


def get_contract_instance(w3, contract_address: str, abi: list):
    return w3.eth.contract(address=contract_address, abi=abi)


async def check_mint_price(contract):
    return await contract.functions.mintPrice().call()


async def check_max_per_address(contract):
    return await contract.functions.maxPerAddress().call()


async def check_total_supply(contract):
    return await contract.functions.totalSupply().call()


async def get_contract_address_from_transaction(w3, tx_hash):
    try:
        receipt = await w3.eth.get_transaction_receipt(tx_hash)
        # print(receipt)
        return receipt['logs'][0]['address'] if receipt['logs'] else None
    except Exception as e:
        print(f"Error getting contract address: {e}")
        return None


async def fetch_json(session, url):
    try:
        async with session.post(url) as response:
            return await response.json()
    except Exception as e:
        print(f"Error fetching JSON: {e}")
        return None


async def get_collections_tx():
    async with aiohttp.ClientSession() as session:
        url = make_api_url(module='account',
                           action='txlist',
                           address=NFTS2ME_CREATOR_CONTRACT, **{'sort': 'desc', 'page': 1})
        response_json = await fetch_json(session, url)

    if response_json is None:
        return []

    tx_df = pd.DataFrame(response_json['result']).sort_values(by='timeStamp', ascending=False)
    collections = tx_df[tx_df['methodId'] == '0x638860eb']['hash'].reset_index(drop=True)
    return collections


async def parse_nfts2me_contracts(mint_price, min_total_supply, n_contracts):
    w3 = AsyncWeb3(
        AsyncWeb3.AsyncHTTPProvider(random.choice(RPC["scroll"]["rpc"])),
        middlewares=[async_geth_poa_middleware]
    )

    collections_tx = await get_collections_tx()

    semaphore = asyncio.Semaphore(5)
    # Создаём асинхронные задачи для каждого хеша
    tasks = [process_contract_with_semaphore(w3, tx_hash, semaphore, mint_price, min_total_supply) for tx_hash in
             collections_tx[:n_contracts + 100]]
    contracts = await asyncio.gather(*tasks)

    # Фильтруем None и возвращаем результаты
    return [contract for contract in contracts if contract]


def update_contracts(contracts):
    with open(NFTS2ME_CONTRACTS_PATH, 'w') as file:
        json.dump(contracts, file)


@retry
async def find_and_update_nfts2me_contracts(mint_price, min_total_supply, search_limit):
    logger.info(f'Starting a search for collections with parameters: mint_price: {mint_price}, min_total_supply {min_total_supply}')
    contracts = await parse_nfts2me_contracts(mint_price, min_total_supply, search_limit)
    logger.success(f'Search is complete. {len(contracts)} contracts found.')
    logger.info(f'Saving results')
    update_contracts(contracts)
    logger.success(f'Contracts saved')


async def process_contract_with_semaphore(w3, tx_hash, semaphore, mint_price, min_total_supply):
    async with semaphore:
        return await process_contract(w3, tx_hash, mint_price, min_total_supply)


async def process_contract(w3, tx_hash, mint_price, min_total_supply):
    contract_address = await get_contract_address_from_transaction(w3, tx_hash)
    if not contract_address:
        return None
    contract = get_contract_instance(w3, contract_address, NFTS2ME_MAIN_ABI)
    contract_mint_price = await check_mint_price(contract)
    max_per_address = await check_max_per_address(contract)
    total_supply = await check_total_supply(contract)

    if contract_mint_price == mint_price and max_per_address > 0 and total_supply >= min_total_supply:
        return contract_address
    return None
