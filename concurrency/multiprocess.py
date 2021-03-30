import concurrent.futures
from multiprocessing import cpu_count

import tasks
import tools

NUM_TASKS = 20
WORKERS = cpu_count() - 1


@tools.timeit
def main(task, *args, **kwargs):
    """Multiple processing solution (parallel execution).

    :param task: blocking (CPU-bound) task
    :type task: callable
    """

    with concurrent.futures.ProcessPoolExecutor(WORKERS) as executor:
        fs = [
            executor.submit(task, *args, **kwargs)
            for _ in range(NUM_TASKS)
        ]
        concurrent.futures.wait(fs)


if __name__ == '__main__':
    main(tasks.blocking_task, 1)
