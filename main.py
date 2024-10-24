import asyncio
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import questionary
from loguru import logger
from questionary import Choice

from settings import (
    RANDOM_WALLET,
    SLEEP_TO,
    SLEEP_FROM,
    QUANTITY_THREADS,
    THREAD_SLEEP_FROM,
    THREAD_SLEEP_TO,
    SAVE_LOGS,
    CHECK_BADGES_PROGRESS
)
from modules_settings import *
from utils.sleeping import sleep
from utils.logs_handler import filter_out_utils
from utils.password_handler import get_wallet_data
from itertools import count
import threading
from config import HEADER


transaction_lock = threading.Lock()


def get_module():
    counter = count(1)
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice(f"{next(counter)}) Encrypt private keys", encrypt_privates),
            Choice(f"{next(counter)}) Deposit to Scroll", deposit_scroll),
            Choice(f"{next(counter)}) Withdraw from OKX", withdraw_okx),
            Choice(f"{next(counter)}) Transfer to OKX", transfer_to_okx),
            Choice(f"{next(counter)}) Withdraw from Scroll", withdraw_scroll),
            Choice(f"{next(counter)}) Bridge Orbiter", bridge_orbiter),
            Choice(f"{next(counter)}) Bridge Layerswap", bridge_layerswap),
            Choice(f"{next(counter)}) Bridge Nitro", bridge_nitro),
            Choice(f"{next(counter)}) Bridge Relay", bridge_relay),
            Choice(f"{next(counter)}) Wrap ETH", wrap_eth),
            Choice(f"{next(counter)}) Unwrap ETH", unwrap_eth),
            Choice(f"{next(counter)}) Swap on Skydrome", swap_skydrome),
            Choice(f"{next(counter)}) Swap on Zebra", swap_zebra),
            Choice(f"{next(counter)}) Swap on SyncSwap", swap_syncswap),
            Choice(f"{next(counter)}) Swap on Ambient", swap_ambient),
            Choice(f"{next(counter)}) Deposit LayerBank", deposit_layerbank),
            Choice(f"{next(counter)}) Withdraw LayerBank", withdraw_layerbank),
            Choice(f"{next(counter)}) Deposit Aave", deposit_aave),
            Choice(f"{next(counter)}) Withdraw Aave", withdraw_aave),
            Choice(f"{next(counter)}) Deposit RocketSam", deposit_rocketsam),
            Choice(f"{next(counter)}) Withdraw RocketSam", withdraw_rocketsam),
            Choice(f"{next(counter)}) Mint and Bridge Zerius NFT", mint_zerius),
            Choice(f"{next(counter)}) Mint ZkStars NFT", mint_zkstars),
            Choice(f"{next(counter)}) Create NFT collection on Omnisea", create_omnisea),
            Choice(f"{next(counter)}) Mint NFT on NFTS2ME", mint_nft),
            Choice(f"{next(counter)}) Parse NFTS2ME collections", parse_nfts2me_contracts),
            Choice(f"{next(counter)}) Dmail send email", send_mail),
            Choice(f"{next(counter)}) Create gnosis safe", create_safe),
            Choice(f"{next(counter)}) Deploy contract", deploy_contract),
            Choice(f"{next(counter)}) Vote on Rubyscore", vote_rubyscore),
            Choice(f"{next(counter)}) Sign In on SecondLive", check_in_secondlive),
            Choice(f"{next(counter)}) Check In on Owlto", owlto_check_in),
            Choice(f"{next(counter)}) Deploy OmniHub NFT", deploy_omnihub_nft),
            Choice(f"{next(counter)}) Swap tokens to ETH", swap_tokens),
            Choice(f"{next(counter)}) Use Multiswap\n", swap_multiswap),
            Choice(f"{next(counter)}) Mint main badge [Canvas]", mint_canvas_badge),
            Choice(f"{next(counter)}) Mint Scroll Origin Badge [Canvas]", mint_scroll_origin_badge),
            Choice(f"{next(counter)}) Mint All Badges [Canvas]\n", mint_all_badges),
            Choice(f"{next(counter)}) Claim ScrollPump tokens", claim_scrollpump),
            Choice(f"{next(counter)}) Use custom routes", custom_routes),
            Choice(f"{next(counter)}) Use automatic routes", automatic_routes),
            Choice(f"{next(counter)}) Check transaction count", "tx_checker"),
            Choice(f"{next(counter)}) Scroll Marks checker (need proxy)", marks_progress_check),
            Choice(f"{next(counter)}) Badges checker (need proxy)", badges_progress_check),
            Choice(f"{next(counter)}) Transfer ERC20", transfer_erc20),
            Choice(f"{next(counter)}) Claim Airdrop", claim_airdrop),
            Choice(f"{next(counter)}) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("❤️ Author – https://t.me/block_nine\n")
        sys.exit()
    return result


def get_wallets():
    wallets_data = get_wallet_data()
    return list(wallets_data.values())


async def run_module(module, wallet_data):
    try:
        await module(wallet_data)
    except Exception as e:
        logger.error(e)
        import traceback

        traceback.print_exc()

    await sleep(SLEEP_FROM, SLEEP_TO, message=f"Move to the next wallet or end of script")


def _async_run_module(module, wallet_data):
    asyncio.run(run_module(module, wallet_data))


def main(module):
    if module == encrypt_privates:
        return encrypt_privates(force=True)
    if module == parse_nfts2me_contracts:
        return asyncio.run(parse_nfts2me_contracts())

    wallets_data = get_wallets()

    if module == marks_progress_check:
        return marks_progress_check(wallets_data)

    if module == badges_progress_check:
        return badges_progress_check(wallets_data)

    if RANDOM_WALLET:
        random.shuffle(wallets_data)

    if CHECK_BADGES_PROGRESS:
        ScrollBadges(wallets_data).get_badge_progress()

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, wallet_data in enumerate(wallets_data, start=1):
            executor.submit(
                _async_run_module,
                module,
                wallet_data
            )
            if _ != len(wallet_data):
                time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))


if __name__ == '__main__':
    print(HEADER)
    print("Author – https://t.me/block_nine\n")

    if sys.platform.startswith("win"):
        # for windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if SAVE_LOGS:
        logger.add('logs.txt', filter=filter_out_utils)

    module = get_module()
    if module == "tx_checker":
        get_tx_count()
    else:
        main(module)

    print("ALL DONE")
    print("Author – https://t.me/block_nine\n")
