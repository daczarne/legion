"""
Module for managing resources.

This module defines enumerations, type hints, and a dataclass for representing the resources:

- Food
- Ore
- Wood

It also includes helper classes for reading resource collection data from YAML/JSON files and interacting with
resources as if they were dictionaries.

Public API:
- Resource (Enum): Named constants for the main resource types.
- ResourceCollectionData (TypedDict): Helper for type hints when reading YAML/JSON. While other modules may rely on
    this for typing, end users are not expected to interact with it directly.
- ResourceCollection (dataclass): Stores resource counts and provides dict-like access.
"""

from collections.abc import Iterator
from dataclasses import dataclass, fields
from enum import Enum
from typing import TypedDict


__all__: list[str] = []


class Resource(Enum):
    """
    Enumeration of resources.
    
    Attributes:
        FOOD: Represents food resources.
        ORE: Represents ore resources.
        WOOD: Represents wood resources.
    """
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
    """
    Stores counts of resources and provides dictionary-like access.
    
    Each instance tracks the resource: food, ore, and wood. Supports iteration and retrieval like a dictionary.
    
    Public methods:
        __iter__(): Iterate over resource names.
        items(): Return (resource_name, value) pairs.
        values(): Return counts of all resources.
        get(key): Get the count for a given resource name. Raises KeyError if the key is not found.
    """
    food: int = 0
    ore: int = 0
    wood: int = 0
    
    def __iter__(self) -> Iterator[str]:
        """
        Iterate over keys, like a dict.
        """
        return (field.name for field in fields(class_or_instance = self))
    
    def items(self) -> Iterator[tuple[str, int]]:
        """
        Return an iterator of (key, value) pairs, like dict.values().
        """
        return ((field.name, getattr(self, field.name)) for field in fields(class_or_instance = self))
    
    def values(self) -> Iterator[int]:
        """
        Return an iterator of values, like dict.values().
        """
        return (getattr(self, field.name) for field in fields(class_or_instance = self))
    
    def get(self, key: str) -> int:
        """
        Get the value for a given resource name.
        """
        if key not in (f.name for f in fields(class_or_instance = self)):
            raise KeyError(f"Invalid resource name: {key}")
        
        return getattr(self, key)
    
    def find_fields_by_value(self, value: int) -> list[str]:
        """
        Return a list of resource names that have the given value.
        """
        return [field.name for field in fields(class_or_instance = self) if getattr(self, field.name) == value]
