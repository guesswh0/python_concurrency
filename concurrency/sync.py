import tasks
import tools

NUM_TASKS = 10


@tools.timeit
def main(task, *args, **kwargs):
    """Synchronous solution (sequential execution).
    :param task: blocking IO/CPU task
    :type task: callable
    """

    for _ in range(NUM_TASKS):
        task(*args, **kwargs)


if __name__ == '__main__':
    main(tasks.blocking_task, 1)
