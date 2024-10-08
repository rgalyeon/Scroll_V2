import asyncio
import random
import traceback

from web3 import AsyncWeb3
from web3.eth import AsyncEth

from config import RPC, REALTIME_SETTINGS_PATH
from settings import (
    CHECK_GWEI, MAX_GWEI,
    RANDOMIZE_GWEI, MAX_GWEI_RANGE,
    GAS_SLEEP_FROM, GAS_SLEEP_TO, REALTIME_GWEI,
    SLEEP_AFTER_TX_FROM, SLEEP_AFTER_TX_TO, USE_SCROLL_GWEI,
    USE_PROXY)
from loguru import logger
import json
from utils.sleeping import sleep
from main import transaction_lock
from functools import wraps


def get_max_gwei_user_settings():
    max_gwei = MAX_GWEI
    if RANDOMIZE_GWEI:
        left_bound, right_bound = MAX_GWEI_RANGE
        max_gwei = random.uniform(left_bound, right_bound)
    if REALTIME_GWEI:
        try:
            with open(REALTIME_SETTINGS_PATH, 'r') as f:
                realtime_settings = json.load(f)
                new_max_gwei = realtime_settings['MAX_GWEI']
                if RANDOMIZE_GWEI and 'MAX_GWEI_RANGE' in realtime_settings:
                    gwei_range = realtime_settings['MAX_GWEI_RANGE']
                    left_bound, right_bound = gwei_range
                    new_max_gwei = random.uniform(left_bound, right_bound)
            if new_max_gwei < 0:
                raise ValueError('Max gwei is not an integer')
            max_gwei = new_max_gwei
        except Exception:
            pass
    return max_gwei


async def get_gas(request_kwargs):
    rpc = None
    try:
        gas_chain = "scroll" if USE_SCROLL_GWEI else "ethereum"
        rpc = random.choice(RPC[gas_chain]["rpc"])
        w3 = AsyncWeb3(
            AsyncWeb3.AsyncHTTPProvider(random.choice(RPC[gas_chain]["rpc"]),
                                        request_kwargs=request_kwargs),
            modules={"eth": (AsyncEth,)},
        )
        gas_price = await w3.eth.gas_price
        gwei = w3.from_wei(gas_price, 'gwei')
        return gwei
    except Exception as e:
        if 'proxy' in request_kwargs:
            logger.error(f"Can't connect to rpc with {request_kwargs['proxy']} proxy")
        else:
            logger.error(f"Can't connect to rpc {rpc}. Try to turn off VPN")
        logger.error(f"Error: {str(e)}")


async def wait_gas(account):
    logger.info("Get GWEI")
    while True:
        try:
            if USE_PROXY:
                gas = await get_gas(account.request_kwargs)
                if gas is None and 'proxy' in account.request_kwargs:
                    gas = await get_gas({})
            else:
                gas = await get_gas({})
            max_gwei = get_max_gwei_user_settings()
            if gas > max_gwei:
                logger.info(f'Current GWEI: {gas} > {max_gwei}')
                await sleep(GAS_SLEEP_FROM, GAS_SLEEP_TO, message="Sleep before next attempt")
            else:
                logger.success(f"GWEI is normal | current: {gas} < {max_gwei}")
                break
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(10)


def check_gas(func):
    @wraps(func)
    async def _wrapper(*args, **kwargs):
        with transaction_lock:
            if CHECK_GWEI:
                await wait_gas(args[0])
            result = await func(*args, **kwargs)
            if CHECK_GWEI:
                await sleep(SLEEP_AFTER_TX_FROM, SLEEP_AFTER_TX_TO, message="Sleep after tx")
            return result

    return _wrapper
