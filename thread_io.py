import threading
from concurrent.futures import ThreadPoolExecutor

# Only one thread may write at a time, so lines don't get garbled together.
# This is required because of the preemptive scheduling of threads.
print_lock = threading.Lock()


def count_range(start: int, end: int) -> None:
    """Count from start to end (inclusive). The unit of work each thread runs."""
    for i in range(start, end + 1):
        with print_lock:
            print(i)


if __name__ == "__main__":

    chunk = 100
    workers = 4

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for worker in range(workers):
            start = worker * chunk + 1
            end = (worker + 1) * chunk
            executor.submit(count_range, start, end)
