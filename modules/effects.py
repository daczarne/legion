from collections.abc import Iterator
from dataclasses import dataclass, fields
from enum import Enum
from typing import TypedDict


class EffectBonus(Enum):
    TROOP_TRAINING = "troop_training"
    POPULATION_GROWTH = "population_growth"
    INTELLIGENCE = "intelligence"


class EffectBonusesData(TypedDict):
    """
    This is a helper class meant to be used when reading EffectBonuses from YAML or JSON files. Its only purpose is to
    provide good type annotations and hints.
    """
    troop_training: int
    population_growth: int
    intelligence: int


@dataclass
class EffectBonuses:
    troop_training: int = 0
    population_growth: int = 0
    intelligence: int = 0
    
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
        Get the value for a given effect name.
        """
        if key not in (f.name for f in fields(class_or_instance = self)):
            raise KeyError(f"Invalid effect name: {key}")
        
        return getattr(self, key)
