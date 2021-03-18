import asyncio

import helpers
import tasks
from concurrency import *


@helpers.atimeit
async def main(task, *args, **kwargs):
    """Asynchronous solution

    :param task: IO bound non blocking task.
    :type task: coroutine function
    """

    aws = []
    for _ in range(NUM_TASKS):
        aws.append(task(*args, **kwargs))
    await asyncio.gather(*aws)


if __name__ == '__main__':
    asyncio.run(main(tasks.non_blocking_task, 1))
