import yaml

from typing import TypeAlias, Literal, Any
from enum import Enum
from dataclasses import dataclass


class GeoFeature(Enum):
    LAKE = "lake"
    OUTCROP_ROCK = "outcrop_rock"
    MOUNTAIN = "mountain"
    FOREST = "forest"


class Resource(Enum):
    FOOD = "food"
    ORE = "ore"
    WOOD = "wood"


@dataclass
class ResourceCollection:
    food: int = 0
    ore: int = 0
    wood: int = 0


@dataclass
class EffectBonuses:
    troop_training: int = 0
    population_growth: int = 0
    intelligence: int = 0


@dataclass
class Building:
    id: str
    name: str
    building_cost: ResourceCollection
    maintenance_cost: ResourceCollection
    productivity_bonuses: ResourceCollection
    productivity_per_worker: ResourceCollection
    effect_bonuses: EffectBonuses
    effect_bonuses_per_worker: EffectBonuses
    storage_capacity: ResourceCollection
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: GeoFeature | None
    # Dependencies here need to be interpreted as an OR. Either of the listed buildings unblocks the building. For
    # example, a Stable requires either a Farm, or Large Farm, or Vineyard, or a Fishing Village. If the city has any
    # one for them it can build a Stable. Similarly, a Blacksmith requires either a Mine, or a Large Mine, or a
    # Mountain Mine, or an Outcrop Mine.
    required_rss: Resource | None
    required_building: list[str]
    replaces: str | None


Buildings: TypeAlias = dict[str, Building]


with open(file = "./data/buildings.yaml", mode = "r") as file:
    buildings_data: dict[Literal["buildings"], list[dict[str, Any]]] = yaml.safe_load(stream = file)

buildings_list: list[dict[str, Any]] = buildings_data["buildings"]

BUILDINGS: Buildings = {}

for building in buildings_list:
    BUILDINGS[building["id"]] = Building(
        id = building["id"],
        name = building["name"],
        building_cost = ResourceCollection(**building["building_cost"]),
        maintenance_cost = ResourceCollection(**building["maintenance_cost"]),
        productivity_bonuses = ResourceCollection(**building["productivity_bonuses"]),
        productivity_per_worker = ResourceCollection(**building["productivity_per_worker"]),
        effect_bonuses = EffectBonuses(**building["effect_bonuses"]),
        effect_bonuses_per_worker = EffectBonuses(**building["effect_bonuses_per_worker"]),
        storage_capacity = ResourceCollection(**building["storage_capacity"]),
        max_workers = building["max_workers"],
        is_buildable = building["is_buildable"],
        is_deletable = building["is_deletable"],
        is_upgradeable = building["is_upgradeable"],
        required_geo = GeoFeature(value = building["required_geo"]) if building["required_geo"] else None,
        required_rss = Resource(value = building["required_rss"]) if building["required_rss"] else None,
        required_building = building["required_building"],
        replaces = building["replaces"],
    )
