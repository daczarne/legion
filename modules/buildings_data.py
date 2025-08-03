from typing import TypedDict
from enum import Enum


class GeoFeatureData(Enum):
    LAKE = "lake"
    OUTCROP_ROCK = "outcrop_rock"
    MOUNTAIN = "mountain"
    FOREST = "forest"


class RssCollectionData(TypedDict):
    food: int
    ore: int
    wood: int


class EffectsData(TypedDict):
    troop_training: int
    population_growth: int
    intelligence: int


class BuildingData(TypedDict):
    id: str
    name: str
    building_cost: RssCollectionData
    maintenance_cost: RssCollectionData
    productivity_bonuses: RssCollectionData
    productivity_per_worker: RssCollectionData
    effect_bonuses: EffectsData
    effect_per_worker: EffectsData
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: GeoFeatureData | None
    required_buildings: list[str]
    replaces: str | None
