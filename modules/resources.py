from collections.abc import Iterator
from dataclasses import dataclass, fields
from enum import Enum
from typing import TypedDict

class Resource(Enum):
    FOOD = ("food", 1)
    ORE = ("ore", 2)
    WOOD = ("wood", 3)
    NONE = (None, 4)
    
    def __init__(
            self,
            resource_name: str | None,
            order: int
        ) -> None:
        self._value_: str | None = resource_name
        self.order: int = order
    
    @classmethod
    def from_str(cls, name: str | None) -> "Resource":
        if name is None:
            return cls.NONE
        for resource in cls:
            if resource.value == name:
                return resource
        raise ValueError(f"Invalid resource name: {name}")


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
    
    def __iter__(self) -> Iterator[str]:
        """Iterate over keys, like a dict."""
        return (field.name for field in fields(self))
    
    def items(self) -> Iterator[tuple[str, int]]:
        """Return an iterator of (key, value) pairs."""
        return ((field.name, getattr(self, field.name)) for field in fields(self))
    
    def values(self) -> Iterator[int]:
        """Return an iterator of values, like dict.values()."""
        return (getattr(self, field.name) for field in fields(self))
    
    def get(self, key: str) -> int:
        """Get the value for a given resource name, or return default if not found."""
        if key not in (f.name for f in fields(self)):
            raise KeyError(f"Invalid resource name: {key}")
        
        return getattr(self, key)
