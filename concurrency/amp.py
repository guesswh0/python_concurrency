import asyncio
import concurrent.futures

import helpers
import tasks
from concurrency import *


@helpers.atimeit
async def main():
    """Asynchronous with multi-processing solution.
    Uses single (MainThread) event loop. CPU bound blocking tasks
    are executed in separate process pool.
    """

    a, b, c = [], [], []
    for _ in range(NUM_TASKS):
        # IO bound non blocking task A
        a.append(asyncio.create_task(tasks.non_blocking_task(1, 'A')))

    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
        for coro in asyncio.as_completed(a):
            await coro
            # CPU bound blocking task B
            b.append(executor.submit(tasks.blocking_task, 1, 'B'))

    for f in concurrent.futures.as_completed(b):
        # IO bound non blocking task C
        c.append(asyncio.create_task(tasks.non_blocking_task(1, 'C')))
    await asyncio.wait(c)


if __name__ == '__main__':
    asyncio.run(main())
