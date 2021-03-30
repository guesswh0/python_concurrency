import asyncio
import concurrent.futures
import functools
from multiprocessing import cpu_count

import tasks
import tools

NUM_TASKS = 24
WORKERS = cpu_count() - 1


@tools.async_timeit
async def case1(non_blocking_task, blocking_task):
    """Asynchronous solution with multiprocessing for CPU-bound blocking tasks.

    Case: [non blocking task] --> [blocking task]
    """

    aws = []
    for i in range(NUM_TASKS):
        aws.append(asyncio.create_task(non_blocking_task()))

    fs = []
    with concurrent.futures.ProcessPoolExecutor(WORKERS) as executor:
        for coro in asyncio.as_completed(aws):
            await coro
            fs.append(executor.submit(blocking_task))
    concurrent.futures.wait(fs)


@tools.async_timeit
async def case2(non_blocking_task, blocking_task):
    """Asynchronous solution with multiprocessing for CPU-bound blocking tasks.

    Case: [blocking task] --> [non blocking task]
    """
    fs = []
    with concurrent.futures.ProcessPoolExecutor(WORKERS) as executor:
        loop = asyncio.get_running_loop()
        for i in range(NUM_TASKS):
            fs.append(loop.run_in_executor(executor, blocking_task))

        aws = []
        for coro in asyncio.as_completed(fs):
            await coro
            aws.append(asyncio.create_task(non_blocking_task()))
    await asyncio.wait(aws)


if __name__ == '__main__':
    taskA = functools.partial(tasks.non_blocking_task, 1)
    taskB = functools.partial(tasks.blocking_task, 1)
    asyncio.run(case1(taskA, taskB))
    # asyncio.run(case2(taskA, taskB))
