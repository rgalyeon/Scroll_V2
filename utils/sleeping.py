import asyncio
import random

from loguru import logger


async def sleep(sleep_from: int, sleep_to: int, message=None):
    delay = random.randint(sleep_from, sleep_to)

    msg = f"💤 Sleep {delay} s."
    if message:
        msg = message + f". {msg}"
    logger.info(msg)
    for _ in range(delay):
        await asyncio.sleep(1)
