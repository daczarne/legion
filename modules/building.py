import yaml
from typing import TypeAlias, Literal, Any, TypedDict
from dataclasses import dataclass

from .effects import EffectBonuses, EffectBonusesData
from .geo_features import GeoFeature
from .resources import Resource, Resources, ResourcesData

BuildingsCount: TypeAlias = dict[str, int]


# * ******** * #
# * BUILDING * #
# * ********** #

@dataclass
class Building:
    id: str
    name: str
    building_cost: Resources
    maintenance_cost: Resources
    productivity_bonuses: Resources
    productivity_per_worker: Resources
    effect_bonuses: EffectBonuses
    effect_bonuses_per_worker: EffectBonuses
    storage_capacity: Resources
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: GeoFeature | None
    required_rss: Resource | None
    # Dependencies here need to be interpreted as an OR. Either of the listed buildings unblocks the building. For
    # example, a Stable requires either a Farm, or a Large Farm, or a Vineyard, or a Fishing Village. If the city has
    # any one for them it can build a Stable. Similarly, a Blacksmith requires either a Mine, or a Large Mine, or a
    # Mountain Mine, or an Outcrop Mine. If a building has no dependencies the list will be empty.
    required_building: list[str]
    replaces: str | None


# * ************** * #
# * BUILDINGS DATA * #
# * ************** * #

class BuildingData(TypedDict):
    id: str
    name: str
    building_cost: ResourcesData
    maintenance_cost: ResourcesData
    productivity_bonuses: ResourcesData
    productivity_per_worker: ResourcesData
    effect_bonuses: EffectBonusesData
    effect_bonuses_per_worker: EffectBonusesData
    storage_capacity: ResourcesData
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: GeoFeature | None
    required_rss: Resource | None
    required_building: list[str]
    replaces: str | None


with open(file = "./data/buildings.yaml", mode = "r") as file:
    buildings_data: dict[Literal["buildings"], list[BuildingData]] = yaml.safe_load(stream = file)

BUILDINGS: dict[str, Building] = {}

for building in buildings_data["buildings"]:
    BUILDINGS[building["id"]] = Building(
        id = building["id"],
        name = building["name"],
        building_cost = Resources(**building["building_cost"]),
        maintenance_cost = Resources(**building["maintenance_cost"]),
        productivity_bonuses = Resources(**building["productivity_bonuses"]),
        productivity_per_worker = Resources(**building["productivity_per_worker"]),
        effect_bonuses = EffectBonuses(**building["effect_bonuses"]),
        effect_bonuses_per_worker = EffectBonuses(**building["effect_bonuses_per_worker"]),
        storage_capacity = Resources(**building["storage_capacity"]),
        max_workers = building["max_workers"],
        is_buildable = building["is_buildable"],
        is_deletable = building["is_deletable"],
        is_upgradeable = building["is_upgradeable"],
        required_geo = GeoFeature(value = building["required_geo"]) if building["required_geo"] else None,
        required_rss = Resource(value = building["required_rss"]) if building["required_rss"] else None,
        required_building = building["required_building"],
        replaces = building["replaces"],
    )
