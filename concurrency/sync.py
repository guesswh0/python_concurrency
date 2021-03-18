import helpers
import tasks
from concurrency import *


@helpers.timeit
def main(task, *args, **kwargs):
    """Synchronous solution

    :param task: IO/CPU bound blocking task.
    :type task: callable
    """

    for _ in range(NUM_TASKS):
        task(*args, **kwargs)


if __name__ == '__main__':
    main(tasks.blocking_task, 1)
