import random

from loguru import logger

from config import MARKS_PATH
import requests
import pandas as pd
from tqdm import tqdm
import os
from fake_useragent import UserAgent


class Scan:
    def __init__(self, wallets_data):
        self.wallets_data = wallets_data
        self.scrollscan_url = 'https://api.scrollscan.com/api'
        self.etherscan_url = 'https://api.etherscan.io/api'

        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "origin": "https://scroll.io/",
            "referrer": "https://scroll.io/",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }

    def get_marks(self, replace=False):
        if os.path.exists(MARKS_PATH) and not replace:
            logger.info(f'Load progress from {MARKS_PATH}')
            return
        logger.info('Check Marks')

        cols = ['Marks']

        df = pd.DataFrame(columns=cols)
        all_proxies = [wallet_info['proxy'] for wallet_info in self.wallets_data]
        for wallet_info in tqdm(self.wallets_data):
            address = wallet_info['address'].lower()
            url = f"https://kx58j6x5me.execute-api.us-east-1.amazonaws.com/scroll/wallet-points?walletAddress={address}"
            header = self.headers.copy()
            header.update({"User-Agent": UserAgent(browsers=["chrome"], os=["macos"]).chrome})
            try:
                request_kwargs = {"http": f"http://{wallet_info['proxy']}",
                                  "https": f"http://{wallet_info['proxy']}"}
                response = requests.get(url, headers=header, proxies=request_kwargs)
            except:
                try:
                    random_proxy = random.choice(all_proxies)
                    request_kwargs = {"http": f"http://{random_proxy}",
                                      "https": f"http://{random_proxy}"}
                    response = requests.get(url, headers=header, proxies=request_kwargs)
                except:
                    logger.warning(f'Cannot parse address {wallet_info["address"]}')
                    df.loc[wallet_info['address'], 'Marks'] = 'bad_response'
                    continue
            data = response.json()
            df.loc[wallet_info['address'], 'Marks'] = round(data[0].get("points"), 4)
        df.fillna('bad_response').to_excel(MARKS_PATH)
