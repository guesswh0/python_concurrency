import concurrent.futures

import helpers
import tasks
from concurrency import *


@helpers.timeit
def main(task, *args, **kwargs):
    """Multi-thread solution.

    :param task: IO bound blocking task.
    :type task: callable
    """

    with concurrent.futures.ThreadPoolExecutor() as executor:
        fs = [
            executor.submit(task, *args, **kwargs)
            for _ in range(NUM_TASKS)
        ]
        concurrent.futures.wait(fs)


if __name__ == '__main__':
    main(tasks.blocking_task, 1)
