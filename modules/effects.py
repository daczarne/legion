from dataclasses import dataclass
from enum import Enum
from typing import TypedDict


class EffectBonus(Enum):
    TROOP_TRAINING = "troop_training"
    POPULATION_GROWTH = "population_growth"
    INTELLIGENCE = "intelligence"


class EffectBonusesData(TypedDict):
    troop_training: int
    population_growth: int
    intelligence: int


@dataclass
class EffectBonuses:
    troop_training: int = 0
    population_growth: int = 0
    intelligence: int = 0
