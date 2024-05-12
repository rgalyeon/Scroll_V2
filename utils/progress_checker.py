import random

from loguru import logger

from config import ETHERSCAN_API_KEYS, PROGRESS_PATH, SCROLL_API_KEYS
import requests
from typing import List, Dict
import pandas as pd
from tqdm import tqdm
import time
import os


class Scan:
    def __init__(self, wallets_data):
        self.wallets_data = wallets_data
        self.scrollscan_url = 'https://api.scrollscan.com/api'
        self.etherscan_url = 'https://api.etherscan.io/api'

    def url_maker(self, module, action, scan_url, **kwargs) -> str:

        if scan_url == self.scrollscan_url:
            api_keys = SCROLL_API_KEYS
        else:
            api_keys = ETHERSCAN_API_KEYS

        url = scan_url + f'?module={module}' \
                         f'&action={action}' \
                         f'&apikey={random.choice(api_keys)}'
        if kwargs:
            for key, value in kwargs.items():
                url += f'&{key}={value}'
        return url

    def get_wallet_transactions(self, address, scan_url, proxies=None):
        url = self.url_maker('account', 'txlist', scan_url, address=address)
        if proxies:
            try:
                resp = requests.get(url, proxies=proxies, timeout=10)
            except:
                resp = requests.get(url)
        else:
            resp = requests.get(url)
        res = resp.json()
        return res

    def parse_transactions(self, transactions: List[Dict], wallet, df: pd.DataFrame, scan_url):
        df.loc[wallet, :] = False

        if scan_url == self.etherscan_url:
            for tx in transactions:
                if (
                    (tx['to'] == '0x6774bcbd5cecef1336b5300fb5186a12ddd8b367' and tx['methodId'] == '0xb2267a7b') or
                    (tx['to'] == '0xf8b1378579659d8f7ee5f3c929c2f3e332e41fd6' and tx['methodId'] == '0x9f8420b3')
                ):
                    df.loc[wallet, 'native_bridge_deposit'] = True

        if scan_url == self.scrollscan_url:
            for tx in transactions:
                pass

    def wait_transactions(self, address, all_proxies, scan_url):
        n_attemps = 10
        while n_attemps:
            proxy = random.choice(all_proxies)
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            transactions = self.get_wallet_transactions(address.lower(), scan_url, proxies)
            if transactions['status'] == 1:
                return transactions
            n_attemps -= 1
            time.sleep(5)

    def get_wallet_progress(self, replace=False, check_eth=True):
        if os.path.exists(PROGRESS_PATH) and not replace:
            logger.info(f'Load progress from {PROGRESS_PATH}')
            return
        logger.info('Check quests progress from blockchain data')

        cols = ['native_bridge_deposit']

        scanners = [self.scrollscan_url]
        if check_eth:
            scanners.append(self.etherscan_url)

        df = pd.DataFrame(columns=cols)
        all_proxies = [wallet_info['proxy'] for wallet_info in self.wallets_data]
        for wallet_info in tqdm(self.wallets_data):
            address = wallet_info['address'].lower()
            for scan_url in scanners:
                transactions = self.get_transaction_list(wallet_info, all_proxies, scan_url)
                try:
                    if transactions['status'] == '1':
                        self.parse_transactions(transactions['result'][:100], wallet_info['address'], df, scan_url)
                    else:
                        print(transactions)
                except Exception as e:
                    logger.warning(f'Can not parse {address} wallet. Error: {e}')
        df.fillna(False).to_excel(PROGRESS_PATH)

    def get_transaction_list(self, wallet_info, all_proxies, scan_url):
        address = wallet_info['address'].lower()
        proxies = {'http': f'http://{wallet_info["proxy"]}', 'https': f'http://{wallet_info["proxy"]}'}
        try:
            transactions = self.get_wallet_transactions(address, scan_url, proxies)
            if transactions['status'] != '1':
                transactions = self.wait_transactions(address, all_proxies, scan_url)
        except:
            transactions = self.wait_transactions(address, all_proxies, scan_url)

        return transactions
