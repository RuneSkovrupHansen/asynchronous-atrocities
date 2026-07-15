import asyncio
import time

# sleep_coroutine will execute until await is hit, at which time the
# event loop will begin execution of the next available coroutine.

# 0 started!
# 0 synchronous blocking sleep
# 0 asynchronous sleep
# 1 started!
# 1 synchronous blocking sleep
# 1 asynchronous sleep
# 2 started!
# 2 synchronous blocking sleep
# 2 asynchronous sleep
# 0 finished
# 1 finished
# 2 finished

async def sleep_coroutine(index: int):
    print(f"{index} started!")

    print(f"{index} synchronous blocking sleep")
    time.sleep(1)

    print(f"{index} asynchronous sleep")
    await asyncio.sleep(1)

    print(f"{index} finished")

async def main():
    await asyncio.gather(*(sleep_coroutine(index) for index in range(3)))

if __name__ == "__main__":
    asyncio.run(main())
