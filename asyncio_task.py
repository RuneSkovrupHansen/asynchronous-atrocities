from typing import Any
import asyncio

async def return_value(value: Any, sleep_time=1, raise_exception=False):
    await asyncio.sleep(sleep_time)

    if raise_exception:
        raise RuntimeError
    
    return value


async def main():

    # Create a task to wrap the coroutine and automatically schedule it.
    task_1 = asyncio.create_task(return_value(1))

    await asyncio.sleep(2)

    print("Task 1 is done, ", task_1.done())
    print(await task_1)

    # Using a TaskGroup provides a convenient way to wait for all tasks.
    async with asyncio.TaskGroup() as tg:
        task_2 = tg.create_task(return_value(2))
        task_3 = tg.create_task(return_value(3))

    print(f"Both tasks have completed now: {task_2.result()}, {task_3.result()}")

    # A TaskGroup can also provide error handling. If any task raises, the
    # group cancels the remaining tasks and propagates an ExceptionGroup.
    try:
        async with asyncio.TaskGroup() as tg:
            task_4 = tg.create_task(return_value(4, sleep_time=2))
            task_5 = tg.create_task(return_value(5, raise_exception=True))

    # The 'except*' interprets the exceptions as a list. Check if empty.
    except* RuntimeError as eg:
        # 'except*' handles the ExceptionGroup raised by the TaskGroup.
        print(f"Caught {len(eg.exceptions)} error(s) from the task group: {eg.exceptions}")
        # task_5 failed, so task_4 was cancelled before completing.
        print("Task 4 cancelled:", task_4.cancelled())


if __name__ == "__main__":
    asyncio.run(main())