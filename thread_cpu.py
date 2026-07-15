"""CPU-bound threading demo: sum integers across worker threads.

Benchmark GIL enabled vs disabled with hyperfine
------------------------------------------------
Requires the free-threaded interpreter (install once with `uv python install 3.14t`):

    FT=$(uv python find 3.14t)
    hyperfine --warmup 3 \
        -n "GIL enabled"  '.venv/bin/python thread_cpu.py' \
        -n "GIL disabled" "$FT -X gil=0 thread_cpu.py"

Results (Apple Silicon, 4 workers, chunk = 10_000_000)
------------------------------------------------------
    GIL enabled     620.1 ms ± 6.8 ms
    GIL disabled    250.8 ms ± 17.7 ms
    => GIL disabled ran 2.47 ± 0.18 times faster

With the GIL, only one thread runs Python bytecode at a time, so the workers
run effectively serially. On the free-threaded build they run in parallel
across cores, roughly quartering the compute time.
"""

from concurrent.futures import ThreadPoolExecutor


def sum_range(start: int, end: int) -> int:
    """Sum every integer from start to end (inclusive).

    This is CPU-bound work: with the GIL enabled, threads can't run this in
    parallel; on a free-threaded build they can, so more workers actually help.
    """
    total = 0
    for i in range(start, end + 1):
        total += i
    return total


if __name__ == "__main__":

    chunk = 10_000_000
    workers = 4

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for worker in range(workers):
            start = worker * chunk + 1
            end = (worker + 1) * chunk
            futures.append(executor.submit(sum_range, start, end))

        total = sum(future.result() for future in futures)

    print(total)
