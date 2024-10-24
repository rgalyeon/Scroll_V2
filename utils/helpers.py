from loguru import logger
from settings import RETRY_COUNT, CHECK_BADGES_PROGRESS
from utils.sleeping import sleep
import traceback
from functools import wraps
from main import transaction_lock
from config import BADGES_PATH
import pandas as pd


def retry(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries <= RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                traceback.print_exc()
                await sleep(10, 10)
                retries += 1

    return wrapper


def remove_wallet(private_key: str):
    with open("wallets.txt", "r") as file:
        lines = file.readlines()

    with open("wallets.txt", "w") as file:
        for line in lines:
            if private_key not in line:
                file.write(line)


def badges_checker(func):
    func_to_name = {
        'mint_eth_badge': 'Ethereum Year Badge',
        'mint_main_badge': 'Main Badge',
        'mint_scroll_origin_badge': 'Scroll Origin Badge'
    }

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if CHECK_BADGES_PROGRESS:
            with transaction_lock:
                progress = pd.read_excel(BADGES_PATH, index_col=0)
            account = args[0]
            module_name = func.__name__
            wallet = account.address.lower()

            try:
                status = progress.loc[wallet, func_to_name[module_name]]
            except KeyError:
                logger.error(f"[{account.account_id}][{account.address}] Progress not found. Use Badges Checker first or turn of CHECK_BADGES_PROGRESS in settings")
                # from traceback import print_exc
                # print_exc()
                status = False
            if not status:
                result = await func(*args, **kwargs)
                if result:
                    with transaction_lock:
                        progress.loc[wallet, func_to_name[module_name]] = True
                        progress.fillna(False).to_excel(BADGES_PATH)
                return result
            else:
                logger.warning(f"[{account.account_id}][{account.address}] Module {module_name} already complete. "
                               f"Skip module")
                return -1
        else:
            result = await func(*args, **kwargs)
            return result

    return wrapper
