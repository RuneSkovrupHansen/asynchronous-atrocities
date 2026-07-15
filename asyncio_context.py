import contextlib
import asyncio

# Connecting to db ...
# Doing other work
# Connected to db!
# Retrieving element 1
# Retrieved element 1
# Retrieving element 2
# Retrieved element 2
# Retrieving element 3
# Retrieved element 3
# Closing connection to db ...
# Finished doing other work

# Create an asynchronous context manager to provide asynchronous
# setup and teardown, and include a dummy database class with
# its own asyncrhronous operation.
@contextlib.asynccontextmanager
async def database():
    print("Connecting to db ...")
    await asyncio.sleep(1)
    print("Connected to db!")

    class db:
        async def get_element(self, id: int):
            print(f"Retrieving element {id}")
            await asyncio.sleep(1)
            print(f"Retrieved element {id}")

    try:
        yield db()
    finally:
        print("Closing connection to db ...")

# Create wrapper function to perform a number of database operations.
async def perform_database_operations():
    async with database() as db:
        await db.get_element(1)
        await db.get_element(2)
        await db.get_element(3)

# Create a dummy function to simulate doing other work.
async def do_other_work():
    print("Doing other work")
    await asyncio.sleep(6)
    print("Finished doing other work")

async def main():
    # Concurrently perform database operations and other work.
    await asyncio.gather(perform_database_operations(), do_other_work())

if __name__ == "__main__":
    asyncio.run(main())
