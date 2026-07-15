from typing import Final

import asyncio
import aiohttp

from common import POKEAPI, Pokemon

# We could probably use the size of the queue to scale the number
# of consumers instead of hard-coding it.

# Adjusting the number of conumers allows us to easily scale the
# processing independently of the production.

# If we wanted to scale producers, we would need some strategy to
# prevent overlapping, such as sharding.
NO_CONSUMERS: Final[int] = 5

async def get_pokemon(id) -> Pokemon:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{POKEAPI}/{id}") as res:
            assert res.status == 200
            return Pokemon.model_validate_json(await res.text())

# Generally, the best pattern appears to be creating all coroutines
# using list interpretation inside a gather().
async def pokemon_fetcher(queue):
    # Create wrapper to place pokemons onto queue to be processed
    async def fetch_pokemon(id):
        print(f"Fetching Pokemon, {id}")
        pokemon = await get_pokemon(id)
        print(f"Pokemon fetched, {id}")
        await queue.put(pokemon)

    # Fetch all pokemons concurrently and place them onto the queue
    await asyncio.gather(*(fetch_pokemon(id) for id in range(1, 50)))
    
    # Add sentinel values to terminate conumers
    for _ in range(NO_CONSUMERS):
        await queue.put(None)

async def store_in_db(pokemon: Pokemon):
    # Simulates storing Pokemon data in a database with I/O delay
    print(f"Storing pokemon in database, {pokemon.id}")
    await asyncio.sleep(1)
    print(f"Pokemon stored in database, {pokemon.id}")

async def pokemon_persister(queue):
    # Persists Pokemon to a database
    while True:
        pokemon = await queue.get()
        if pokemon is None:
            break

        await store_in_db(pokemon)

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(pokemon_fetcher(queue), *(pokemon_persister(queue) for _ in range(NO_CONSUMERS)))


if __name__ == "__main__":
    asyncio.run(main())