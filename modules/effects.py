"""
Module for managing effect bonuses.

This module defines enumerations, type hints, and a dataclass for representing the three types of effect bonuses a
building can provide/a city can have:

- Troop training: experience gained by new troops.
- Population growth: multipliers affecting city population increase.
- Intelligence: improvements to spying ability.

It also includes helper classes for reading effect bonus data from YAML/JSON files and interacting with the bonuses as
if they were dictionaries.

Public API:

- EffectBonus (Enum): Named constants for the three effect types.
- EffectBonusesData (TypedDict): Helper for type hints when reading YAML/JSON. Although part of the public API (used by
    other modules), end users are not expected to interact with it directly.
- EffectBonuses (dataclass): Stores effect values and provides dict-like access.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import TYPE_CHECKING, TypedDict


if TYPE_CHECKING:
    from collections.abc import Iterator


__all__: list[str] = []


class EffectBonus(Enum):
    """
    Enumeration of the three types of effect bonuses a building can provide/a city can have.
    
    Attributes:
        TROOP_TRAINING: Experience gained by newly trained troops.
        POPULATION_GROWTH: Multipliers for population growth in the city.
        INTELLIGENCE: Spying ability improvements.
    """
    
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
    """
    Stores the values of effect bonuses and provides dictionary-like access.
    
    Each instance tracks the three effect types: troop training, population growth, and intelligence. Supports
    iteration and retrieval like a dict.
    
    Public methods:
        __iter__(): Iterate over effect names.
        items(): Return (effect_name, value) pairs.
        values(): Return values of all effects.
        get(key): Get the value for a given effect name. Raises KeyError if the key is not found.
    """
    
    troop_training: int = 0
    population_growth: int = 0
    intelligence: int = 0
    
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
        Get the value for a given effect.
        
        Args:
            key (str): The name of a key to get.
        
        Raises:
            KeyError: If the provided key does not exist.
        
        Returns:
            int: The value for that key.
        """
        
        if key not in (f.name for f in fields(class_or_instance = self)):
            raise KeyError(f"Invalid effect name: {key}")
        
        return getattr(self, key)
