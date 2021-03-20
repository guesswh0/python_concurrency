import asyncio
import time
from urllib.request import urlopen, Request

import tools


# Emulated tasks

@tools.log_task
def blocking_task(n: int):
    time.sleep(n)
    return True


@tools.log_async_task
async def non_blocking_task(n: int):
    await asyncio.sleep(n)
    return True


@tools.log_async_task
async def complex_task1(a: int, b: int):
    await asyncio.sleep(a)
    time.sleep(b)
    return True


@tools.log_async_task
async def complex_task2(a: int, b: int):
    time.sleep(a)
    await asyncio.sleep(b)
    return True


# Real tasks

def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a process pool.
    return sum(i * i for i in range(10 ** 7))


def blocking_request():
    # Make request to Wikipedia to receive random article.
    request = Request('https://en.wikipedia.org/wiki/Special:Random')
    with urlopen(request) as response:
        if response.status > 399:
            # If getting a 429 Too Many Requests
            raise Exception(f'Received a {response.status} instead of 200.')
        return response
