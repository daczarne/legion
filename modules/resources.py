from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, TypedDict, Literal
from collections.abc import Generator, Iterator

class Resource(Enum):
    FOOD = "food"
    ORE = "ore"
    WOOD = "wood"


class ResourceCollectionData(TypedDict):
    food: int
    ore: int
    wood: int


@dataclass
class ResourceCollection:
    food: int = 0
    ore: int = 0
    wood: int = 0
    
    def __iter__(self) -> Iterator[str]:
        """Iterate over keys, like a dict."""
        return (field.name for field in fields(self))
    
    def items(self) -> Iterator[tuple[str, int]]:
        """Return an iterator of (key, value) pairs."""
        return ((field.name, getattr(self, field.name)) for field in fields(self))
    
    def values(self) -> Iterator[int]:
        """Return an iterator of values, like dict.values()."""
        return (getattr(self, field.name) for field in fields(self))
