"""
Module for managing resources.

This module defines enumerations, type hints, and a dataclass for representing the resources:

- Food
- Ore
- Wood

It also includes helper classes for reading resource collection data from YAML/JSON files and interacting with
resources as if they were dictionaries.

Public API:

- Resource (Enum): Named constants for the resource types.
- ResourceCollectionData (TypedDict): Helper for type hints when reading YAML/JSON.
- ResourceCollection (dataclass): Stores resource counts and provides dict-like access.

This classes and types are meant to be used only in other modules. End-users should have no use for them.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import TYPE_CHECKING, TypedDict


if TYPE_CHECKING:
    from collections.abc import Iterator


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
    Stores resource values and provides dictionary-like access.
    
    Each instance tracks the resources: food, ore, and wood. Supports iteration and retrieval like a dictionary.
    
    Public methods:
        __iter__(): Iterate over resource names.
        items(): Return (resource_name, value) pairs.
        values(): Return counts of all resources.
        get(key): Get the count for a given resource name. Raises KeyError if the key is not found.
        find_fields_by_value(value): Returns a list of all the resources that have a given value.
    """
    
    food: int = 0
    ore: int = 0
    wood: int = 0
    
    def __iter__(self) -> Iterator[str]:
        return (field.name for field in fields(class_or_instance = self))
    
    def items(self) -> Iterator[tuple[str, int]]:
        """
        Returns an iterator of (key, value) pairs, like `dict.items()`.
        
        Returns:
            Iterator[tuple[str, int]]: An iterator of (key, value) pairs
        """
        
        return ((field.name, getattr(self, field.name)) for field in fields(class_or_instance = self))
    
    def values(self) -> Iterator[int]:
        """
        Return an iterator of values, like `dict.values()`.
        
        Returns:
            Iterator[int]: An iterator of values.
        """
        
        return (getattr(self, field.name) for field in fields(class_or_instance = self))
    
    def get(self, key: str) -> int:
        """
        Get the value for a given resource.
        
        Args:
            key (str): The name of a key to get.
        
        Raises:
            KeyError: If the provided key does not exist.
        
        Returns:
            int: The value for that key.
        """
        
        if key not in (f.name for f in fields(class_or_instance = self)):
            raise KeyError(f"Invalid resource name: {key}")
        
        return getattr(self, key)
    
    def find_fields_by_value(self, value: int) -> list[str]:
        """
        Return a list of resource names that have the given value.
        
        Args:
            value (int): The value to look for.
        
        Returns:
            list[str]: A list of resources that have that value.
        """
        
        return [field.name for field in fields(class_or_instance = self) if getattr(self, field.name) == value]
