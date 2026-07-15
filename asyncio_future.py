import asyncio


async def set_result_later(future: asyncio.Future, value, delay=1):
    # Simulate some work (e.g. waiting on I/O) before the result is ready.
    await asyncio.sleep(delay)

    # Fulfilling the future wakes up whoever is awaiting it.
    future.set_result(value)


async def main():

    # A future is an "IOU" for a value that doesn't exist yet. We create an
    # empty one, tied to the current event loop.
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    # At this point the future is pending; nobody has set its result.
    print("Future done?", future.done())

    # Schedule a task that will fill in the result after a short delay.
    asyncio.create_task(set_result_later(future, 42))

    # Awaiting the future suspends here until set_result() is called.
    result = await future

    print("Future done?", future.done())
    print("Result:", result)


if __name__ == "__main__":
    asyncio.run(main())
