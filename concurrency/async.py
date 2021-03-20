import asyncio

import tasks
import tools

NUM_TASKS = 100


@tools.async_timeit
async def main(task, *args, **kwargs):
    """Asynchronous solution (concurrent execution).

    :param task: non blocking task
    :type task: coroutine function
    """

    aws = []
    for _ in range(NUM_TASKS):
        aws.append(task(*args, **kwargs))
    await asyncio.gather(*aws)


if __name__ == '__main__':
    asyncio.run(main(tasks.non_blocking_task, 1))
