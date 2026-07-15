from typing import Any
import asyncio

async def return_value(value: Any, sleep_time=1, raise_exception=False):
    await asyncio.sleep(sleep_time)

    if raise_exception:
        raise RuntimeError
    
    return value


async def main():
    print(await return_value(1)) # 1

    # 'gather' runs coroutines concurrently, returning results in input order.
    values = await asyncio.gather(return_value(2), return_value(3))
    print(values) # [2, 3]

    # 'as_completed' yields tasks as they finish, so the shorter sleep returns first.
    for task in asyncio.as_completed([return_value(4, 2), return_value(5, 1)]):
        value = await task
        print(value)

    # 'gather' can also return exceptions.
    values = await asyncio.gather(return_value(6), return_value(7, raise_exception=True), return_exceptions=True)
    for value in values:
        print(type(value)) # int, RuntimeError

if __name__ == "__main__":
    asyncio.run(main())