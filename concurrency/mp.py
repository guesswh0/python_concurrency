import concurrent.futures

import helpers
import tasks
from concurrency import *


@helpers.timeit
def main(task, *args, **kwargs):
    """Multi-process solution (parallel execution).

    :param task: CPU bound blocking task
    :type task: callable
    """

    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
        fs = [
            executor.submit(task, *args, **kwargs)
            for _ in range(NUM_TASKS)
        ]
        concurrent.futures.wait(fs)


if __name__ == '__main__':
    main(tasks.blocking_task, 1)
