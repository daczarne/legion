import yaml

from dataclasses import dataclass, field
from typing import ClassVar, Literal, TypeAlias, TypedDict

from .effects import EffectBonusesData, EffectBonuses
from .geo_features import GeoFeature
from .resources import Resource, ResourceCollectionData, ResourceCollection

BuildingsCount: TypeAlias = dict[str, int]


# * ************** * #
# * BUILDINGS DATA * #
# * ************** * #

class BuildingData(TypedDict):
    """
    This is a helper class meant to be used when reading Building from YAML or JSON files. Its only purpose is to
    provide good type annotations and hints.
    """
    id: str
    name: str
    building_cost: ResourceCollectionData
    maintenance_cost: ResourceCollectionData
    productivity_bonuses: ResourceCollectionData
    productivity_per_worker: ResourceCollectionData
    effect_bonuses: EffectBonusesData
    effect_bonuses_per_worker: EffectBonusesData
    storage_capacity: ResourceCollectionData
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: str | None
    required_rss: str | None
    required_building: list[str]
    replaces: str | None

with open(file = "./data/buildings.yaml", mode = "r") as file:
    buildings_data: dict[Literal["buildings"], list[BuildingData]] = yaml.safe_load(stream = file)

BUILDINGS: dict[str, BuildingData] = {building["id"]: building for building in buildings_data["buildings"]}


# * ******** * #
# * BUILDING * #
# * ******** * #

@dataclass(match_args = False, kw_only = True)
class Building:
    id: str = field(init = True, repr = True, compare = True, hash = True)
    workers: int = field(default = 0, repr = False, compare = False, hash = False)
    
    name: str = field(init = False, repr = False, compare = False, hash = False)
    building_cost: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    maintenance_cost: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    productivity_bonuses: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    productivity_per_worker: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    effect_bonuses: EffectBonuses = field(init = False, repr = False, compare = False, hash = False)
    effect_bonuses_per_worker: EffectBonuses = field(init = False, repr = False, compare = False, hash = False)
    storage_capacity: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    max_workers: int = field(init = False, repr = False, compare = False, hash = False)
    is_buildable: bool = field(init = False, repr = False, compare = False, hash = False)
    is_deletable: bool = field(init = False, repr = False, compare = False, hash = False)
    is_upgradeable: bool = field(init = False, repr = False, compare = False, hash = False)
    required_geo: GeoFeature | None = field(init = False, default = None, repr = False, compare = False, hash = False)
    required_rss: Resource | None = field(init = False, default = None, repr = False, compare = False, hash = False)
    # Dependencies here need to be interpreted as an OR. Either of the listed buildings unblocks the building. For
    # example, a Stable requires either a Farm, or a Large Farm, or a Vineyard, or a Fishing Village. If the city has
    # any one for them it can build a Stable. Similarly, a Blacksmith requires either a Mine, or a Large Mine, or a
    # Mountain Mine, or an Outcrop Mine. If a building has no dependencies the list will be empty.
    required_building: list[str] = field(init = False, default_factory = list, repr = False, compare = False, hash = False)
    replaces: str | None = field(init = False, default = None, repr = False, compare = False, hash = False)
    
    __match_args__: ClassVar[str] = ("id")
    
    def _validate_initial_number_of_workers(self) -> None:
        if self.workers > self.max_workers:
            raise ValueError(f"Too many workers. Max is {self.max_workers} for {self.name}.")
    
    def __post_init__(self) -> None:
        self.name = BUILDINGS[self.id]["name"]
        self.building_cost = ResourceCollection(**BUILDINGS[self.id]["building_cost"])
        self.maintenance_cost = ResourceCollection(**BUILDINGS[self.id]["maintenance_cost"])
        self.productivity_bonuses = ResourceCollection(**BUILDINGS[self.id]["productivity_bonuses"])
        self.productivity_per_worker = ResourceCollection(**BUILDINGS[self.id]["productivity_per_worker"])
        self.effect_bonuses = EffectBonuses(**BUILDINGS[self.id]["effect_bonuses"])
        self.effect_bonuses_per_worker = EffectBonuses(**BUILDINGS[self.id]["effect_bonuses_per_worker"])
        self.storage_capacity = ResourceCollection(**BUILDINGS[self.id]["storage_capacity"])
        self.max_workers = BUILDINGS[self.id]["max_workers"]
        self.is_buildable = BUILDINGS[self.id]["is_buildable"]
        self.is_deletable = BUILDINGS[self.id]["is_deletable"]
        self.is_upgradeable = BUILDINGS[self.id]["is_upgradeable"]
        self.required_geo = GeoFeature(value = BUILDINGS[self.id]["required_geo"]) if BUILDINGS[self.id]["required_geo"] else None
        self.required_rss = Resource(value = BUILDINGS[self.id]["required_rss"]) if BUILDINGS[self.id]["required_rss"] else None
        self.required_building = BUILDINGS[self.id]["required_building"]
        self.replaces = BUILDINGS[self.id]["replaces"]
        
        self._validate_initial_number_of_workers()
    
    def add_workers(self, qty: int) -> None:
        if self.workers + qty > self.max_workers:
            raise ValueError(f"Too many workers. Max is {self.max_workers} for {self.name}.")
        
        self.workers += qty
    
    def remove_workers(self, qty: int) -> None:
        if self.workers - qty < 0:
            raise ValueError(f"Can't remove {qty} workers. Building currently has {self.workers}.")
        
        self.workers -= qty
    
    def set_workers(self, qty: int) -> None:
        if qty > self.max_workers:
            raise ValueError(f"{self.name} cannot allocate {qty}. Max is {self.max_workers}.")
        
        self.workers = qty
    
    def show(self) -> None:
        print(self)
        print(f"Name: {self.name}")
        print(f"Building costs: {self.building_cost}")
        print(f"Maintenance costs: {self.maintenance_cost}")
        print(f"Productivity bonuses: {self.productivity_bonuses}")
        print(f"Productivity per worker: {self.productivity_per_worker}")
        print(f"Effect bonuses: {self.effect_bonuses}")
        print(f"Effect bonuses per worker: {self.effect_bonuses_per_worker}")
        print(f"Storage capacity: {self.storage_capacity}")
        print(f"Max. workers: {self.max_workers}")
        print(f"Is buildable: {self.is_buildable}")
        print(f"Is deletable: {self.is_deletable}")
        print(f"Is upgradeable: {self.is_upgradeable}")
        print(f"Required GeoFeature: {self.required_geo}")
        print(f"Required Resource: {self.required_rss}")
        print(f"Required building: {self.required_building}")
        print(f"Replaces: {self.replaces}")
        print(f"Current workers: {self.workers}")
