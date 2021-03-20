import asyncio
import multiprocessing

import tasks
import tools

NUM_TASKS = 24
WORKERS = 4


@tools.async_timeit
async def process_tasks(task, *args, **kwargs):
    fs = []
    # let assume that the number of tasks
    # are equally separable to number of workers
    for _ in range(NUM_TASKS // WORKERS):
        fs.append(asyncio.create_task(task(*args, **kwargs)))
    await asyncio.wait(fs)


def runner(task, *args, **kwargs):
    asyncio.run(process_tasks(task, *args, **kwargs))


@tools.timeit
def main(task, *args, **kwargs):
    """Using a multiple processes, with each running a separate event loop.

    :param task: sequence of non blocking and blocking (CPU-bound) tasks.
    :type task: coroutine function
    """

    processes = []
    for _ in range(WORKERS):
        p = multiprocessing.Process(
            target=runner,
            args=(task, *args),
            kwargs=kwargs
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    main(tasks.complex_task1, 1, 1)
