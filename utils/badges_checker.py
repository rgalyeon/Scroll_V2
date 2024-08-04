import random
import warnings
from loguru import logger

from config import SCROLLSCAN_URL, SCROLL_API_KEYS, BADGES_PATH
import requests
from typing import List, Dict
import pandas as pd
from tqdm import tqdm
import time
import os

warnings.filterwarnings('ignore')


class ScrollBadges:
    def __init__(self, wallets_data):
        self.wallets_data = wallets_data

    @staticmethod
    def url_maker(module, action, **kwargs) -> str:

        url = SCROLLSCAN_URL + f'?module={module}' \
                              f'&action={action}' \
                              f'&apikey={random.choice(SCROLL_API_KEYS)}'
        if kwargs:
            for key, value in kwargs.items():
                url += f'&{key}={value}'
        return url

    def get_wallet_transactions(self, address, proxies=None):
        url = self.url_maker('account', 'txlist', address=address)
        if proxies:
            try:
                response = requests.get(url, proxies=proxies, timeout=10)
            except:
                response = requests.get(url)
        else:
            response = requests.get(url)
        res = response.json()
        return res

    @staticmethod
    def parse_transactions(transactions: List[Dict], wallet, df: pd.DataFrame):
        df.loc[wallet, :] = False
        for tx in transactions:
            if tx['to'] == '0xB23AF8707c442f59BDfC368612Bd8DbCca8a7a5a'.lower() and tx['methodId'] == '0x4737576e':
                df.loc[wallet, 'Main Badge'] = True
            if tx['to'] == '0x39fb5E85C7713657c2D9E869E974FF1e0B06F20C'.lower() and tx['methodId'] == '0x3c042715':
                df.loc[wallet, 'Ethereum Year Badge'] = True
            if tx['to'] == '0xC47300428b6AD2c7D03BB76D05A176058b47E6B0'.lower() and tx['methodId'] == '0xf17325e7':
                df.loc[wallet, 'Origin NFT Badge'] = True
            if tx['to'] == '0x13babb8C705506Fd71f7e9Aff431B9aF2E659FE9'.lower() and tx['methodId'] == '0x3c042715':
                df.loc[wallet, 'OmniHub Badge'] = True
            if tx['to'] == '0x65AB4b5f30AeF8B29858eA2cbD6b0d0E68010206'.lower() and tx['methodId'] == '0x3c042715':
                df.loc[wallet, 'Trusta MEDIA Score Badge'] = True

    def wait_transactions(self, address, all_proxies):
        n_attemps = 10
        while n_attemps:
            proxy = random.choice(all_proxies)
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            transactions = self.get_wallet_transactions(address.lower(), proxies)
            if transactions['status'] == 1:
                return transactions
            n_attemps -= 1
            time.sleep(5)

    def get_badge_progress(self, replace=False):
        if os.path.exists(BADGES_PATH) and not replace:
            logger.info(f'Load badges from {BADGES_PATH}')
            return
        logger.info('Check quests progress from blockchain data')

        cols = ['Main Badge', 'Ethereum Year Badge', 'Origin NFT Badge', 'OmniHub Badge', 'Trusta MEDIA Score Badge']

        df = pd.DataFrame(columns=cols)
        all_proxies = [wallet_info['proxy'] for wallet_info in self.wallets_data]
        for wallet_info in tqdm(self.wallets_data):
            address = wallet_info['address'].lower()
            proxies = {'http': f'http://{wallet_info["proxy"]}', 'https': f'http://{wallet_info["proxy"]}'}
            try:
                transactions = self.get_wallet_transactions(address, proxies)
                if transactions['status'] != '1':
                    transactions = self.wait_transactions(address, all_proxies)
            except:
                transactions = self.wait_transactions(address, all_proxies)
            try:
                if transactions['status'] == '1':
                    self.parse_transactions(transactions['result'][-100:], wallet_info['address'], df)
                else:
                    print(transactions)
            except Exception as e:
                logger.warning(f'Can not parse {address} wallet. Error: {e}')
        df.fillna(False).to_excel(BADGES_PATH)
