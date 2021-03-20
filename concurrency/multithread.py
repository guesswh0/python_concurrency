import concurrent.futures

import tasks
import tools

NUM_TASKS = 40
WORKERS = 8


@tools.timeit
def main(task, *args, **kwargs):
    """Multiple threading solution.

    :param task: blocking (IO-bound) task
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
