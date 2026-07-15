from typing import Final, Any

from pydantic import field_validator, BaseModel

POKEAPI: Final[str] = "https://pokeapi.co/api/v2/pokemon/"

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