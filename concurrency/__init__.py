__all__ = [
    'NUM_TASKS',
    'NUM_CORES'
]

from multiprocessing import cpu_count

NUM_TASKS = 24
NUM_CORES = cpu_count()
