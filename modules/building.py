"""
Module for defining and managing game-buildings.

This module loads building definitions from a YAML file and provides typed access to their properties. It exposes two
main components:

- BUILDINGS: A dictionary of all building definitions loaded from `./data/buildings.yaml`. Keys are building
    identifiers, and values are `BuildingData` mappings with raw attributes.
- Building: A dataclass representing a specific building instance, with runtime attributes such as costs, bonuses,
    storage capacity, worker assignment, and construction requirements.

The system is designed to help players validate game assumptions about what can be built in a city, what it costs, and
how different buildings interact (e.g., dependencies, upgrades, and resource requirements).

Typical usage example:

```python
from buildings import Building

farm = Building(id="farm")
farm.add_workers(3)
farm.show()
```
"""

import yaml

from dataclasses import dataclass, field
from typing import ClassVar, Literal, TypeAlias, TypedDict

from .effects import EffectBonusesData, EffectBonuses
from .geo_features import GeoFeature
from .resources import Resource, ResourceCollectionData, ResourceCollection


"""
Mapping of building identifiers to their counts in a city.

Keys are building IDs (e.g., "farm", "mine"). Values are integers representing how many of that building exist.
"""
BuildingsCount: TypeAlias = dict[str, int]


# * ************** * #
# * BUILDINGS DATA * #
# * ************** * #

class BuildingData(TypedDict):
    """
    This is a helper class meant to be used when reading Building-data from YAML or JSON files. Its only purpose is to
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
    """
    Represents a building in the game.
    
    To create a building simply supply the building identifier for the desired building. The class will look-up all
    other properties for the building such as costs, bonuses, worker capacity, and requirements. Buildings may depend
    on other buildings, resources, or geographic features to be constructed. They can also replace other buildings when
    built (for example, the Temple replaces the Shrine).
    
    Attributes:
        id (str): Unique identifier of the building. This is unique amongst all buildings, not amongst all building
            instances in a city. For example, if 2 Farms are built in a city, both of them will have `id = "farm"`.
        workers (int): Current number of assigned workers.
        name (str): Display name of the building.
        building_cost (ResourceCollection): Resources required to build.
        maintenance_cost (ResourceCollection): Ongoing resource costs.
        productivity_bonuses (ResourceCollection): Productivity bonuses gained by having this building in the city.
        productivity_per_worker (ResourceCollection): Productivity per worker. Only relevant for resource-producing
            buildings.
        effect_bonuses (EffectBonuses): Effect bonuses produced by having the building in the city. There are three
            bonuses in the game
                - Troop training: the experience new troops have when trained in the city.
                - Population growth: multipliers for how fast the population grows.
                - Intelligence: spying ability.
        effect_bonuses_per_worker (EffectBonuses): Effect bonuses produced by staffing the buildings of the city. For
            example, having a Basilica given +50 Population growth if the Basilica is staffed.
        storage_capacity (ResourceCollection): Storage space provided by the building.
        max_workers (int): Maximum assignable workers.
        is_buildable (bool): Whether the building can be constructed. Some buildings, e.g. Supply dump, cannot be built
            by the player. THey are either present in the city at the start or they are not.
        is_deletable (bool): Whether the building can be removed. Some buildings cannot be removed once built. For
            example, halls, mountain mines, fishing villages, etc.
        is_upgradeable (bool): Whether the building can be upgraded.
        required_geo (GeoFeature | None): Required geographic feature, if any. For example, building a Mountain mine
            requires that the city where it is being built has a mountain.
        required_rss (Resource | None): Required resource, if any. For example, building Farms requires that the city
            has production potential for food production.
        required_building (list[str]): List of possible prerequisite buildings (OR condition).
        replaces (str | None): Identifier of the building this one replaces.
    """
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
    
    
    def _validate_building_exists(self) -> None:
        if self.id not in BUILDINGS:
            raise ValueError(f"Building {self.id} does not exist.")
    
    def _validate_initial_number_of_workers(self) -> None:
        if self.workers > self.max_workers:
            raise ValueError(f"Too many workers. Max is {self.max_workers} for {self.name}.")
    
    
    def __post_init__(self) -> None:
        self._validate_building_exists()
        
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
        """
        Assigns additional workers to the building.
        
        Args:
            qty (int): Number of workers to add.
        
        Raises:
            ValueError: If the new total (current + the qty to be added) exceeds the maximum worker capacity.
        """
        if self.workers + qty > self.max_workers:
            raise ValueError(f"Too many workers. Max is {self.max_workers} for {self.name}.")
        
        self.workers += qty
    
    def remove_workers(self, qty: int) -> None:
        """
        Removes workers from the building.
        
        Args:
            qty (int): Number of workers to remove.
        
        Raises:
            ValueError: If the operation results in fewer than zero workers.
        """
        if self.workers - qty < 0:
            raise ValueError(f"Can't remove {qty} workers. Building currently has {self.workers}.")
        
        self.workers -= qty
    
    def set_workers(self, qty: int) -> None:
        """
        Sets the exact number of workers for the building.
        
        Args:
            qty (int): Number of workers to assign.
        
        Raises:
            ValueError: If the value exceeds the maximum number of workers the building can have.
        """
        if qty > self.max_workers:
            raise ValueError(f"{self.name} cannot allocate {qty}. Max is {self.max_workers}.")
        
        self.workers = qty
    
    def show(self) -> None:
        """
        Prints detailed information about the building to stdout.
        """
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
