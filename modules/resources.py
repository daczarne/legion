from dataclasses import dataclass
from enum import Enum
from typing import TypedDict


class Resource(Enum):
    FOOD = "food"
    ORE = "ore"
    WOOD = "wood"


class ResourceCollectionData(TypedDict):
    """
    This is a helper class meant to be used when reading ResouceCollections from YAML or JSON files. Its only purpose
    is to provide good type annotations and hints.
    """
    food: int
    ore: int
    wood: int


@dataclass
class ResourceCollection:
    food: int = 0
    ore: int = 0
    wood: int = 0
