import asyncio
import time

from helpers import logger


# Emulated tasks

def blocking_task(n, name=''):
    logger.info(f'blocking task {name}')
    time.sleep(n)
    return True


async def non_blocking_task(n, name=''):
    logger.info(f'non-blocking task {name}')
    await asyncio.sleep(n)
    return True


async def complex_task1():
    await non_blocking_task(1, 'A')
    blocking_task(1, 'B')
    await non_blocking_task(1, 'C')
    return True
