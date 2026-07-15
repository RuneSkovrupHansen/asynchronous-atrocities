import asyncio

async def main():
    await asyncio.sleep(1)
    print("Hello World!")

# Use the asyncio REPL to await outside a function:
#
#   uv run -m asyncio
#
# Then, inside the REPL:
#
#   >>> from asyncio_repl import main
#   >>> await main()