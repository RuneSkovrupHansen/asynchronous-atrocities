from typing import AsyncGenerator
import asyncio

# 'async def' + 'yield' makes this an async generator. Values
# are produced lazily, but the generator can yield execution
# through 'await'.
async def load_elements(offset: int = 0, number: int = 5):
    elements = range(offset, offset + number)
    i = 0
    while i < len(elements):
        # Simulate database I/O
        await asyncio.sleep(1)
        yield elements[i]
        i += 1

async def main():
    # Using 'async' here allows us to use iterate over an asynchronous
    # iterator, in this case an asynchronous generator.

    # Critically, the processing here not concurrent, but we would
    # could perform another task concurrently with this processing.
    print("Synchronous processing of elements")
    async for e in load_elements():
        print(e)


    # Create coroutine wrapper that iterates over a generator.
    async def print_elements(generator: AsyncGenerator):
        async for e in generator:
            print(e)

    # Await two coroutines with the wrapper, to show that element processing
    # can happen concurrently with another task.
    print("Concurrent processing of elements")
    await asyncio.gather(
        print_elements(load_elements(offset=0)),
        print_elements(load_elements(offset=10)),
    )
    
if __name__ == "__main__":
    asyncio.run(main())