from collections.abc import Iterator
from dataclasses import dataclass, fields
from enum import Enum
from typing import TypedDict


class GeoFeature(Enum):
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
        Get the value for a given resource name.
        """
        if key not in (f.name for f in fields(class_or_instance = self)):
            raise KeyError(f"Invalid geo feature name: {key}")
        
        return getattr(self, key)
