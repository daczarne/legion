from dataclasses import dataclass
from enum import Enum
from typing import TypedDict


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
