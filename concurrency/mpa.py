import asyncio
import multiprocessing

import helpers
import tasks
from concurrency import *


@helpers.atimeit
async def process_tasks(task, *args, **kwargs):
    fs = []
    # lets assume that number tasks equally divisible by number of cores
    for _ in range(NUM_TASKS // NUM_CORES):
        fs.append(asyncio.create_task(task(*args, **kwargs)))
    await asyncio.wait(fs)


def runner(task, *args, **kwargs):
    asyncio.run(process_tasks(task, *args, **kwargs))


@helpers.timeit
def main(task, *args, **kwargs):
    """Multi-process and asynchronous solution.
    Each process runs a separate event loop.

    :param task: IO and CPU bound "complex" task.
    :type task: coroutine function
    """

    processes = []
    for _ in range(NUM_CORES):
        p = multiprocessing.Process(
            target=runner,
            args=(task, *args),
            kwargs={**kwargs}
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    main(tasks.complex_task1)
