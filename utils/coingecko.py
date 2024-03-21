import asyncio
from aiohttp import ClientSession
from loguru import logger


async def get_token_price(token_name: str, vs_currency: str = 'usd', proxy=None) -> float:
    await asyncio.sleep(10)
    url = 'https://api.coingecko.com/api/v3/simple/price'

    params = {
        'ids': f'{token_name}',
        'vs_currencies': f'{vs_currency}'
    }

    async with ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return float(data[token_name][vs_currency])
            elif response.status == 429:
                logger.warning(f'CoinGecko API got rate limit. Next try in 60 second')
                await asyncio.sleep(60)
            raise ValueError(f'Bad request to CoinGecko API: {response.status}')
