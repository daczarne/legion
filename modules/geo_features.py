"""
Module for managing geographic features.

This module defines enumerations, type hints, and a dataclass for representing the geographic features a city might
have:

- Rock outcrops
- Mountains
- Lakes
- Forests

It also includes helper classes for reading geographic feature data from YAML/JSON files and interacting with the
features as if they were dictionaries.

Public API:
- GeoFeature (Enum): Named constants for the main geographic features.
- GeoFeaturesData (TypedDict): Helper for type hints when reading YAML/JSON. While other modules may rely on this for
    typing, end users are not expected to interact with it directly.
- GeoFeatures (dataclass): Stores feature counts and provides dict-like access.
"""

from collections.abc import Iterator
from dataclasses import dataclass, fields
from enum import Enum
from typing import TypedDict


__all__: list[str] = []


class GeoFeature(Enum):
    """
    Enumeration of the geographic features a city may contain.
    
    Attributes:
        OUTCROP_ROCK: Rock outcrops in the city.
        MOUNTAIN: Mountains present in the city.
        LAKE: Lakes within the city area.
        FOREST: Forests surrounding the city.
    """
    OUTCROP_ROCK = "outcrop_rock"
    MOUNTAIN = "mountain"
    LAKE = "lake"
    FOREST = "forest"


class GeoFeaturesData(TypedDict):
    """
    This is a helper class meant to be used when reading GeoFeatures from YAML or JSON files. Its only purpose is to
    provide good type annotations and hints.
    """
    rock_outcrops: int
    mountains: int
    lakes: int
    forests: int


@dataclass
class GeoFeatures:
    """
    Stores counts of geographic features and provides dictionary-like access.
    
    Each instance tracks the four geographic feature types: rock outcrops, mountains, lakes, and forests. Supports
    iteration and retrieval like a dictionary.
    
    Public methods:
        __iter__(): Iterate over feature names.
        items(): Return (feature_name, value) pairs.
        values(): Return counts of all features.
        get(key): Get the count for a given feature name. Raises KeyError if the key is not found.
    """
    rock_outcrops: int = 0
    mountains: int = 0
    lakes: int = 0
    forests: int = 0
    
    def __iter__(self) -> Iterator[str]:
        """
        Iterate over keys, like a dict.
        """
        return (field.name for field in fields(class_or_instance = self))
    
    def items(self) -> Iterator[tuple[str, int]]:
        """
        Return an iterator of (key, value) pairs, like dict.items().
        """
        return ((field.name, getattr(self, field.name)) for field in fields(class_or_instance = self))
    
    def values(self) -> Iterator[int]:
        """
        Return an iterator of values, like dict.values().
        """
        return (getattr(self, field.name) for field in fields(class_or_instance = self))
    
    def get(self, key: str) -> int:
        """
        Get the value for a given geo feature name.
        """
        if key not in (f.name for f in fields(class_or_instance = self)):
            raise KeyError(f"Invalid geo feature name: {key}")
        
        return getattr(self, key)
