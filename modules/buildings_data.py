from typing import TypedDict
from enum import Enum


class GeoFeatureData(Enum):
    LAKE = "lake"
    OUTCROP_ROCK = "outcrop_rock"
    MOUNTAIN = "mountain"
    FOREST = "forest"


class RssData(Enum):
    FOOD = "food"
    ORE = "ore"
    WOOD = "wood"


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
    effect_bonuses_per_worker: EffectsData
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: GeoFeatureData | None
    # Dependencies here need to be interpreted as an OR. Either of the listed buildings unblocks the building. For
    # example, a Stable requires either a Farm, or Large Farm, or Vineyard, or a Fishing Village. A Blacksmith requires
    # either a Mine, or a Large Mine, or a Mountain Mine, or an Outcrop Mine.
    required_rss: RssData | None
    required_building: list[str]
    replaces: str | None
