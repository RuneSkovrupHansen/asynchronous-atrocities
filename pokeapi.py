from typing import Any, Final
import time
import asyncio

import requests
from pydantic import BaseModel, field_validator
import aiohttp

POKEAPI: Final[str] = "https://pokeapi.co/api/v2/pokemon/"

IDS: Final[list[int]] = list(range(1,10))

class Pokemon(BaseModel):
    id: int
    name: str
    abilities: list[str]

    @field_validator("abilities", mode="before")
    @classmethod
    def parse_abilities(cls, value: Any) -> Any:
        # PokeAPI returns: [{"ability": {"name": "blaze", ...}, ...}, ...]
        if isinstance(value, list):
            return [
                item["ability"]["name"]
                if isinstance(item, dict) and "ability" in item
                else item
                for item in value
            ]
        return value

def get_pokemons() -> list[Pokemon]:
    pokemons: list[Pokemon] = []
    for id in IDS:
        res = requests.get(f"{POKEAPI}/{id}")
        assert res.status_code == 200
        pokemons.append(Pokemon.model_validate_json(res.text))
    return pokemons

async def get_pokemons_async() -> list[Pokemon]:
    pokemons: list[Pokemon] = []
    async with aiohttp.ClientSession() as session:
        for id in IDS:
            async with session.get(f"{POKEAPI}/{id}") as res:
                assert res.status == 200
                pokemons.append(Pokemon.model_validate_json(await res.text()))
    return pokemons

if __name__ == "__main__":
    start = time.perf_counter()
    get_pokemons()
    end = time.perf_counter()
    print(end-start) # 0.8198634169530123

    start = time.perf_counter()
    asyncio.run(get_pokemons_async())
    end = time.perf_counter()
    print(end-start) # 0.21463387500261888 - significantly faster
