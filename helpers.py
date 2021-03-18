import logging
import sys

import time
from pathlib import Path

DATA_DIR = Path(__file__).resolve(strict=True).parent / 'data'

if not Path.exists(DATA_DIR):
    Path.mkdir(DATA_DIR)

# project default logger
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

# stdout stream handler
out = logging.StreamHandler(sys.stdout)
out.setLevel(logging.INFO)
out.addFilter(lambda record: record.levelno <= logging.INFO)
out.setFormatter(logging.Formatter(
    '[PID:%(process)5d][%(threadName)10s][%(asctime)s.%(msecs).3d] %(message)s',
    '%H:%M:%S'
))
logger.addHandler(out)

# stderr stream handler
err = logging.StreamHandler(sys.stderr)
err.setLevel(logging.WARNING)
err.addFilter(lambda record: record.levelno <= logging.WARNING)
err.setFormatter(logging.Formatter(
    '[PID:%(process)5d][%(asctime)s.%(msecs).3d] %(message)s',
    '%H:%M:%S'
))

logger.addHandler(err)


def timeit(fn):
    def wrapper(*args, **kwargs):
        logger.log(logging.WARNING, 'Starting ...')
        t1 = time.perf_counter()
        fn(*args, **kwargs)
        t2 = time.perf_counter()
        logger.log(logging.WARNING, f'Time to complete: {t2 - t1:.2f} seconds')

    return wrapper


def atimeit(coro):
    async def wrapper(*args, **kwargs):
        logger.log(logging.WARNING, 'Starting ...')
        t1 = time.perf_counter()
        await coro(*args, **kwargs)
        t2 = time.perf_counter()
        logger.log(logging.WARNING, f'Time to complete: {t2 - t1:.2f} seconds')

    return wrapper
