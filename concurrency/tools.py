import logging
import sys
import time
import uuid
from functools import wraps


def get_logger():
    # stdout stream handler
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.INFO)
    out.addFilter(lambda record: record.levelno <= logging.INFO)
    out.setFormatter(logging.Formatter(
        '[PID:%(process)5d]'
        '[%(asctime)s.%(msecs).3d]'
        # '[%(threadName)10s]'
        ' %(message)s',
        '%H:%M:%S'
    ))

    # stderr stream handler
    err = logging.StreamHandler(sys.stderr)
    err.setLevel(logging.WARNING)
    err.addFilter(lambda record: record.levelno <= logging.WARNING)
    err.setFormatter(logging.Formatter(
        '[PID:%(process)5d]'
        '[%(asctime)s.%(msecs).3d]'
        ' %(message)s',
        '%H:%M:%S'
    ))

    log = logging.getLogger()
    log.setLevel(logging.NOTSET)
    log.addHandler(out)
    log.addHandler(err)
    return log


# project default logger
logger = get_logger()


def timeit(fn):
    def wrapper(*args, **kwargs):
        logger.log(logging.WARNING, 'Starting ...')
        t1 = time.perf_counter()
        fn(*args, **kwargs)
        t2 = time.perf_counter()
        logger.log(logging.WARNING, f'Time to complete: {t2 - t1:.2f} seconds')

    return wrapper


def async_timeit(coro):
    async def wrapper(*args, **kwargs):
        logger.log(logging.WARNING, 'Starting ...')
        t1 = time.perf_counter()
        await coro(*args, **kwargs)
        t2 = time.perf_counter()
        logger.log(logging.WARNING, f'Time to complete: {t2 - t1:.2f} seconds')

    return wrapper


def _format_args(*args, **kwargs):
    s1 = ','.join(str(arg) for arg in args)
    s2 = ','.join(f'{key}={value}' for key, value in kwargs.items())
    if not s2:
        return s1
    return ','.join((s1, s2))


def log_task(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        name = uuid.uuid4().hex[:5]
        s = _format_args(*args, **kwargs)
        logger.info(f"{fn.__name__}({s}): {name}")
        t1 = time.perf_counter()
        fn(*args, **kwargs)
        t2 = time.perf_counter()
        logger.info(f"{fn.__name__}({s}): {name}, done in {t2 - t1:.2f} seconds")

    return wrapper


def log_async_task(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        name = uuid.uuid4().hex[:5]
        s = _format_args(*args, **kwargs)
        logger.info(f"{coro.__name__}({s}): {name}")
        t1 = time.perf_counter()
        await coro(*args, **kwargs)
        t2 = time.perf_counter()
        logger.info(f"{coro.__name__}({s}): {name}, done in {t2 - t1:.2f} seconds")

    return wrapper
