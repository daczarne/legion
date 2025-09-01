"""
Module for defining and managing cities.

This module loads city definitions from a YAML file and provides typed access to their properties. It exposes the
public API for working with cities, including creating city instances, counting buildings, and inspecting city
attributes like production, storage, defenses, and effect bonuses.

Public API:

- City (dataclass): Represents a city within a campaign. Handles city validation, calculates production, storage,
    defenses, effect bonuses, and city focus.

Assets shared with other modules:

- CityDict (TypedDict): Helper type for defining cities via dictionaries.
- CITIES (list[_CityData]): List of all city definitions loaded from `./data/cities.yaml`.

Internal objects (not part of the public API):
- `_CityDisplay`: Display functionality for an object of `City` class. It displays the object into a
    terminal-friendly layout, showing various aspects of the city such as buildings, effects, production, storage, and
    defenses.
- _CityData (TypedDict): Type for internal use when reading city data from YAML/JSON.
- _CityEffectBonuses, _CityProduction, _CityStorage, _CityDefenses: helper dataclasses for modeling city internals.
"""

import yaml

from dataclasses import dataclass, field
from typing import ClassVar, Literal, TypedDict

from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .building import Building, BuildingsCount, _BUILDINGS
from .display import DisplayConfiguration, DisplaySectionConfiguration, DEFAULT_SECTION_COLORS
from .effects import EffectBonusesData, EffectBonuses
from .exceptions import (
    NoCityHallError,
    TooManyHallsError,
    FortsCannotHaveBuildingsError,
    TooManyBuildingsError,
    NoGarrisonFoundError,
    UnknownBuildingError,
    BuildingCannotBeAddedToTheCityError,
)
from .geo_features import GeoFeaturesData, GeoFeatures
from .resources import Resource, ResourceCollectionData, ResourceCollection


__all__: list[str] = ["City"]


class CityDict(TypedDict):
    """
    This is a helper class meant to be used when defining cities using dictionaries. Its only purpose is to provide
    good type annotations and hints.
    """
    name: str
    campaign: str
    buildings: BuildingsCount


# * *********** * #
# * CITIES DATA * #
# * *********** * #

class _CityData(TypedDict):
    """
    This is a helper class meant to be used when reading city data from YAML or JSON files. Its only purpose is to
    provide good type annotations and hints.
    """
    campaign: str
    name: str
    resource_potentials: ResourceCollectionData
    geo_features: GeoFeaturesData
    effects: EffectBonusesData
    has_supply_dump: bool
    is_fort: bool
    garrison: str

with open(file = "./data/cities.yaml", mode = "r") as file:
    _cities_data: dict[Literal["cities"], list[_CityData]] = yaml.safe_load(stream = file)

CITIES: list[_CityData] = _cities_data["cities"]


# * **** * #
# * CITY * #
# * **** * #

@dataclass(kw_only = True)
class _CityEffectBonuses:
    """
    A helper class to model the city's effect bonuses. Should not be used outside this module.
    """
    city: EffectBonuses = field(default_factory = EffectBonuses)
    buildings: EffectBonuses = field(default_factory = EffectBonuses)
    workers: EffectBonuses = field(default_factory = EffectBonuses)
    total: EffectBonuses = field(default_factory = EffectBonuses)


@dataclass(kw_only = True)
class _CityProduction:
    """
    A helper class to model the city's production. Should not be used outside this module.
    """
    base: ResourceCollection = field(default_factory = ResourceCollection)
    productivity_bonuses: ResourceCollection = field(default_factory = ResourceCollection)
    total: ResourceCollection = field(default_factory = ResourceCollection)
    maintenance_costs: ResourceCollection = field(default_factory = ResourceCollection)
    balance: ResourceCollection = field(default_factory = ResourceCollection)


@dataclass(kw_only = True)
class _CityStorage:
    """
    A helper class to model the city's storage capacity. Should not be used outside this module.
    """
    city: ResourceCollection = field(default_factory = ResourceCollection)
    buildings: ResourceCollection = field(default_factory = ResourceCollection)
    warehouse: ResourceCollection = field(default_factory = ResourceCollection)
    supply_dump: ResourceCollection = field(default_factory = ResourceCollection)
    total: ResourceCollection = field(default_factory = ResourceCollection)


@dataclass(kw_only = True)
class _CityDefenses:
    """
    A helper class to model the city's defenses. Should not be used outside this module.
    """
    garrison: str = field(default = "")
    squadrons: int = field(default = 1)
    squadron_size: str = field(default = "Small")


@dataclass(
    match_args = False,
    order = False,
    kw_only = True,
)
class City:
    """
    Represents a city within a campaign of the game.
    
    A `City` is defined by its campaign, name, and a collection of buildings. The campaign and city name will be used
    to look-up city characteristics like the resource potential of the city and its garrison. Based on the supplied
    buildings, it will calculate the production of the city, the storage capacity, the defenses, etc.
    
    On initialization, the city validates its buildings to ensure consistency:
    
    - Exactly one hall must be present (Village, Town, or City hall).
    - The number of buildings must not exceed the maximum allowed for the hall type.
        - For Village: 4
        - For Town: 6
        - For City: 8
    
    Attributes:
        campaign (str): The campaign identifier the city belongs to.
        name (str): The name of the city.
        buildings (list[Building]): A list of buildings present in the city.
        
        resource_potentials (ResourceCollection): The resource potentials of the city.
        geo_features (GeoFeatures): Geographical features present in the city (lakes, mountains, etc).
        has_supply_dump (bool): A boolean indicating whether the city has a Supply Dump (True), or not (False).
        effects (CityEffectBonuses): Effect bonuses from the city, its buildings, and workers.
        production (CityProduction): Production statistics for the city.
        storage (CityStorage): Resource storage capacities of the city.
        defenses (CityDefenses): Defense of the city (number of squads and their size).
        focus (Resource | None): If a Resource, the highest producing resource of the city.
    """
    campaign: str = field(init = True, default = "", repr = True, compare = True, hash = True)
    name: str = field(init = True, default = "", repr = True, compare = True, hash = True)
    buildings: list[Building] = field(init = True, default_factory = list, repr = False, compare = False, hash = False)
    has_supply_dump: bool = field(init = False, default = False, repr = False, compare = False, hash = False)
    is_fort: bool = field(init = False, default = False, repr = False, compare = False, hash = False)
    
    # Post init fields
    resource_potentials: ResourceCollection = field(
        init = False,
        default_factory = ResourceCollection,
        repr = False,
        compare = False,
        hash = False,
    )
    geo_features: GeoFeatures = field(
        init = False,
        default_factory = GeoFeatures,
        repr = False,
        compare = False,
        hash = False,
    )
    
    effects: _CityEffectBonuses = field(
        init = False,
        default_factory = _CityEffectBonuses,
        repr = False,
        compare = False,
        hash = False,
    )
    production: _CityProduction = field(
        init = False,
        default_factory = _CityProduction,
        repr = False,
        compare = False,
        hash = False,
    )
    storage: _CityStorage = field(
        init = False,
        default_factory = _CityStorage,
        repr = False,
        compare = False,
        hash = False,
    )
    defenses: _CityDefenses = field(
        init = False,
        default_factory = _CityDefenses,
        repr = False,
        compare = False,
        hash = False,
    )
    focus: Resource | None = field(
        init = False,
        default = None,
        repr = False,
        compare = False,
        hash = False,
    )
    
    
    # Class variables
    MAX_WORKERS: ClassVar[BuildingsCount] = {
        "fort": 0,
        "village_hall": 10,
        "town_hall": 14,
        "city_hall": 18,
    }
    
    __match_args__: ClassVar[tuple[str, ...]] = ("campaign", "name")
    
    
    def _get_rss_potentials(self) -> ResourceCollection:
        """
        Finds the city supplied by the user in the directory of cities and returns its resource potentials.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return ResourceCollection(**city["resource_potentials"])
        
        return ResourceCollection()
    
    def _get_geo_features(self) -> GeoFeatures:
        """
        Finds the city supplied by the user in the directory of cities and returns its geo-features.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return GeoFeatures(**city["geo_features"])
        
        return GeoFeatures()
    
    def _has_supply_dump(self) -> bool:
        """
        Checks if the city has a Supply dump.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return city["has_supply_dump"]
        
        return False
    
    def _is_fort(self) -> bool:
        """
        Checks if the city is a "Small Fort" city.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return city["is_fort"]
        
        return False
    
    
    #* Alternative city creator methods
    @classmethod
    def from_buildings_count(
        cls,
        campaign: str,
        name: str,
        buildings: BuildingsCount,
    ) -> "City":
        """
        Create a `City` instance from a count of buildings. The count must be a dictionary with building IDs as keys
        and the quantity of each building type as values.
        
        This method expands the building counts into actual `Building` objects and initializes a new city with them.
        This implies that you can pass 0-count buildings and they will automatically be ignored.
        
        Args:
            campaign (str): the campaign identifier the city belongs to.
            name (str): the name of the city.
            buildings (BuildingsCount): a dictionary mapping building IDs to quantities.
        
        Returns:
            City: a new `City` instance populated with the given buildings.
        """
        city_buildings: list[Building] = []
        
        for id, qty in buildings.items():
            for _ in range(qty):
                city_buildings.append(Building(id = id))
        
        return cls(
            campaign = campaign,
            name = name,
            buildings = city_buildings,
        )
    
    
    #* Validate city buildings
    def _add_supply_dump_to_buildings(self) -> None:
        if not self.has_supply_dump:
            return
        
        if self.has_building(id = "supply_dump"):
            return
        
        self.buildings.append(Building(id = "supply_dump"))
    
    def _add_fort_to_buildings(self) -> None:
        if not self.is_fort:
            return
        
        if self.has_building(id = "fort"):
            return
        
        self.buildings.append(Building(id = "fort"))
    
    
    #* Effect bonuses
    def _get_city_effects(self) -> EffectBonuses:
        """
        Finds the city supplied by the user in the directory of cities and returns its effects.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return EffectBonuses(**city["effects"])
        
        return EffectBonuses()
    
    def _calculate_building_effects(self) -> EffectBonuses:
        """
        Calculates the effects produced by buildings. These do not include worker level effects.
        """
        building_effects: EffectBonuses = EffectBonuses()
        
        for building in self.buildings:
            building_effects.troop_training += building.effect_bonuses.troop_training
            building_effects.population_growth += building.effect_bonuses.population_growth
            building_effects.intelligence += building.effect_bonuses.intelligence
        
        return building_effects
    
    def _calculate_worker_effects(self) -> EffectBonuses:
        """
        Calculates the effects produced by building workers.
        """
        worker_effects: EffectBonuses = EffectBonuses()
        
        for building in self.buildings:
            worker_effects.troop_training += building.effect_bonuses_per_worker.troop_training * building.max_workers
            worker_effects.population_growth += building.effect_bonuses_per_worker.population_growth * building.max_workers
            worker_effects.intelligence += building.effect_bonuses_per_worker.intelligence * building.max_workers
        
        return worker_effects
    
    def _calculate_total_effects(self) -> EffectBonuses:
        """
        Calculate the total effects (base + given by buildings and its workers).
        """
        total_effects: EffectBonuses = EffectBonuses()
        
        total_effects.troop_training = (
            self.effects.city.troop_training
            + self.effects.buildings.troop_training
            + self.effects.workers.troop_training
        )
        total_effects.population_growth = (
            self.effects.city.population_growth
            + self.effects.buildings.population_growth
            + self.effects.workers.population_growth
        )
        total_effects.intelligence = (
            self.effects.city.intelligence
            + self.effects.buildings.intelligence
            + self.effects.workers.intelligence
        )
        
        return total_effects
    
    
    #* Production
    def _calculate_base_production(self) -> ResourceCollection:
        """
        Given the buildings in the city, it calculates the base production of those buildings for each resource. Base
        production is defined here as production before productivity bonuses. It is determined only by the buildings
        and the city's production potential for each rss. Buildings are assumed to be fully staffed. For example, "1
        large mine" means "1 large mine with all 3 workers".
        """
        from math import floor
        
        base_production: ResourceCollection = ResourceCollection()
        
        for building in self.buildings:
            
            productivity_per_worker: ResourceCollection = building.productivity_per_worker
            max_workers: int = building.max_workers
            
            # Production per worker
            prod_per_worker_food: int = int(floor(productivity_per_worker.food * self.resource_potentials.food / 100.0))
            prod_per_worker_ore: int = int(floor(productivity_per_worker.ore * self.resource_potentials.ore / 100.0))
            prod_per_worker_wood: int = int(floor(productivity_per_worker.wood * self.resource_potentials.wood / 100.0))
            
            # Base production
            base_production_food: int = prod_per_worker_food * max_workers
            base_production_ore: int = prod_per_worker_ore * max_workers
            base_production_wood: int = prod_per_worker_wood * max_workers
            
            base_production.food += base_production_food
            base_production.ore += base_production_ore
            base_production.wood += base_production_wood
        
        return base_production
    
    def _calculate_productivity_bonuses(self) -> ResourceCollection:
        """
        Based on the buildings found in the city, it calculates the productivity bonuses for each resource.
        """
        productivity_bonuses: ResourceCollection = ResourceCollection()
        
        for building in self.buildings:
            productivity_bonuses.food += building.productivity_bonuses.food
            productivity_bonuses.ore += building.productivity_bonuses.ore
            productivity_bonuses.wood += building.productivity_bonuses.wood
        
        return productivity_bonuses
    
    def _calculate_total_production(self) -> ResourceCollection:
        """
        Given the base production and the productivity bonuses of a city, it calculates the total production.
        """
        from math import floor
        
        total_food: int = int(floor(self.production.base.food * (1 + self.production.productivity_bonuses.food / 100)))
        total_ore: int = int(floor(self.production.base.ore * (1 + self.production.productivity_bonuses.ore / 100)))
        total_wood: int = int(floor(self.production.base.wood * (1 + self.production.productivity_bonuses.wood / 100)))
        
        return ResourceCollection(food = total_food, ore = total_ore, wood = total_wood)
    
    def _calculate_maintenance_costs(self) -> ResourceCollection:
        """
        Based on the buildings found in the city, it calculates the maintenance costs for each resource.
        """
        maintenance_costs: ResourceCollection = ResourceCollection()
        
        for building in self.buildings:
            maintenance_costs.food += building.maintenance_cost.food
            maintenance_costs.ore += building.maintenance_cost.ore
            maintenance_costs.wood += building.maintenance_cost.wood
        
        return maintenance_costs
    
    def _calculate_production_balance(self) -> ResourceCollection:
        """
        Calculate the balance for each rss. The balance is the difference between the total production and the
        maintenance costs for each rss.
        """
        balance_food: int = self.production.total.food - self.production.maintenance_costs.food
        balance_ore: int = self.production.total.ore - self.production.maintenance_costs.ore
        balance_wood: int = self.production.total.wood - self.production.maintenance_costs.wood
        
        return ResourceCollection(food = balance_food, ore = balance_ore, wood = balance_wood)
    
    
    #* Storage capacity
    def _calculate_city_storage(self) -> ResourceCollection:
        return self.get_hall().storage_capacity
    
    def _calculate_buildings_storage(self) -> ResourceCollection:
        buildings_storage: ResourceCollection = ResourceCollection()
        
        for building in self.buildings:
            if building.id not in [*_CityValidator.POSSIBLE_CITY_HALLS, "warehouse", "supply_dump"]:
                buildings_storage.food += building.storage_capacity.food
                buildings_storage.ore += building.storage_capacity.ore
                buildings_storage.wood += building.storage_capacity.wood
        
        return buildings_storage
    
    def _calculate_warehouse_storage(self) -> ResourceCollection:
        if self.has_building(id = "warehouse"):
            return self.get_building(id = "warehouse").storage_capacity
        
        return ResourceCollection()
    
    def _calculate_supply_dump_storage(self) -> ResourceCollection:
        if self.has_building(id = "supply_dump"):
            return self.get_building(id = "supply_dump").storage_capacity
        
        return ResourceCollection()
    
    def _calculate_total_storage_capacity(self) -> ResourceCollection:
        """
        Calculate the total effects (base + given by buildings and its workers).
        """
        total_storage: ResourceCollection = ResourceCollection()
        
        total_storage.food = (
            self.storage.city.food
            + self.storage.buildings.food
            + self.storage.warehouse.food
            + self.storage.supply_dump.food
        )
        total_storage.ore = (
            self.storage.city.ore
            + self.storage.buildings.ore
            + self.storage.warehouse.ore
            + self.storage.supply_dump.ore
        )
        total_storage.wood = (
            self.storage.city.wood
            + self.storage.buildings.wood
            + self.storage.warehouse.wood
            + self.storage.supply_dump.wood
        )
        
        return total_storage
    
    
    #* Defenses
    def _get_garrison(self) -> str:
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return city["garrison"]
        
        raise NoGarrisonFoundError(f"No garrison found for {self.campaign} - {self.name}")
    
    def _calculate_garrison_size(self) -> int:
        if self.is_fort:
            return 3
        
        if self.has_building(id = "large_fort"):
            return 4
        
        if self.has_building(id = "medium_fort"):
            return 3
        
        if self.has_building(id = "small_fort"):
            return 2
        
        return 1
    
    def _calculate_squadron_size(self) -> str:
        if self.is_fort:
            return "Medium"
        
        if self.has_building(id = "quartermaster"):
            return "Huge"
        
        if self.has_building(id = "barracks"):
            return "Large"
        
        if any([
            self.has_building(id = "small_fort"),
            self.has_building(id = "medium_fort"),
            self.has_building(id = "large_fort"),
        ]):
            return "Medium"
        
        return "Small"
    
    
    #* City focus
    def _find_city_focus(self) -> Resource | None:
        highest_balance: int = max(self.production.balance.food, self.production.balance.ore, self.production.balance.wood)
        
        if highest_balance < 0:
            return None
        
        rss_with_highest_balance: list[str] = self.production.balance.find_fields_by_value(value = highest_balance)
        
        if len(rss_with_highest_balance) > 1:
            return None
        
        return Resource(value = rss_with_highest_balance[0])
    
    
    def __post_init__(self) -> None:
        self.resource_potentials = self._get_rss_potentials()
        self.geo_features = self._get_geo_features()
        
        self.has_supply_dump = self._has_supply_dump()
        self._add_supply_dump_to_buildings()
        
        self.is_fort = self._is_fort()
        self._add_fort_to_buildings()
        
        #* Validate city
        validator: _CityValidator = _CityValidator(city = self)
        validator._validate_halls()
        validator._validate_number_of_buildings()
        
        #* Effect bonuses
        self.effects.city = self._get_city_effects()
        self.effects.buildings = self._calculate_building_effects()
        self.effects.workers = self._calculate_worker_effects()
        self.effects.total = self._calculate_total_effects()
        
        #* Production
        self.production.base = self._calculate_base_production()
        self.production.productivity_bonuses = self._calculate_productivity_bonuses()
        self.production.total = self._calculate_total_production()
        self.production.maintenance_costs = self._calculate_maintenance_costs()
        self.production.balance = self._calculate_production_balance()
        
        #* Storage
        self.storage.city = self._calculate_city_storage()
        self.storage.buildings = self._calculate_buildings_storage()
        self.storage.warehouse = self._calculate_warehouse_storage()
        self.storage.supply_dump = self._calculate_supply_dump_storage()
        self.storage.total = self._calculate_total_storage_capacity()
        
        #* Defenses
        self.defenses.garrison = self._get_garrison()
        self.defenses.squadrons = self._calculate_garrison_size()
        self.defenses.squadron_size = self._calculate_squadron_size()
        
        #* Focus
        self.focus = self._find_city_focus()
    
    
    def get_building(self, id: str) -> Building:
        """
        Retrieve a building from the city by its ID. In case the city has more than one it will return the first one.
        
        Args:
            id (str): the building ID to search for.
        
        Returns:
            Building: the first building in the city with the given ID.
        
        Raises:
            KeyError: if no building with the given ID exists in the city.
        """
        for building in self.buildings:
            if building.id == id:
                return building
        
        raise KeyError(f"No building with ID={id} found in {self.name}.")
    
    def has_building(self, id: str) -> bool:
        """
        Check whether the city contains a building with the specified ID.
        
        Args:
            id (str): the building ID to search for.
        
        Returns:
            bool: True if the building is present, False otherwise.
        """
        for building in self.buildings:
            if building.id == id:
                return True
        
        return False
    
    def get_hall(self) -> Building: # type: ignore
        """
        Retrieve the hall building of the city.
        
        The hall is the central building of the city and must be one of "Village hall", "Town hall", or "City hall".
        
        Returns:
            Building: the hall building of the city.
        """
        for building in self.buildings:
            if building.id not in _CityValidator.POSSIBLE_CITY_HALLS:
                continue
            
            return building
    
    def get_buildings_count(self, by: Literal["name", "id"]) -> BuildingsCount:
        """
        Count the number of buildings in the city grouped by ID or name.
        
        Args:
            by (Literal["name", "id"]): whether to group counts by building name or ID.
        
        Returns:
            BuildingsCount: a dictionary mapping either building IDs or names to their respective counts.
        """
        from collections import Counter
        
        if by == "name":
            buildings_count: BuildingsCount = Counter([building.name for building in self.buildings])
            return buildings_count
        
        if by == "id":
            buildings_count: BuildingsCount = Counter([building.id for building in self.buildings])
            return buildings_count
    
    def build_city_displayer(self, configuration: DisplayConfiguration | None = None) -> "_CityDisplay":
        """
        Creates a displayer for the City.
        
        Args:
            configuration: An optional dictionary for customizing the display. This can be used to hide specific
                sections or change their appearance.
        
        Returns:
            _CityDisplay: An instance of the _CityDisplay class.
        """
        return _CityDisplay(city = self, configuration = configuration)
    
    def display_city(self, configuration: DisplayConfiguration | None = None) -> None:
        """
        Renders and prints the city's statistics to the console.
        
        This method acts as a facade, delegating the display logic to the `_CityDisplay` class.
        
        Args:
            configuration: An optional dictionary for customizing the display. This can be used to hide specific
                sections or change their appearance.
        """
        displayer: _CityDisplay = self.build_city_displayer(configuration = configuration)
        displayer.display_city()


# * ******************** * #
# * CITY BUILDINGS GRAPH * #
# * ******************** * #

class _CityBuildingNode:
    """
    Internal node used by `_CityBuildingsGraph` to represent a single type of building within the context of a specific
    city.
    
    Each node keeps track of:
    
    - The building it represents (`building`)
    - The maximum number of such buildings that may exist in the city (`allowed_count`)
    - How many instances have currently been placed (`current_count`)
    - Whether the building is still available for construction (`is_available`)
    
    Key invariants:
    
    - `allowed_count` is immutable after initialization and must be >= 0.
    - `building` is immutable after initialization.
    - `current_count` is always in the range [0, allowed_count].
    - `is_available` is True if and only if `current_count < allowed_count`.
    
    Nodes are not meant to be mutated directly. The only way to update state is through `increment_count()`, which
    enforces these invariants.
    """
    
    __slots__: tuple[str, ...] = ("_building", "_allowed_count", "_current_count", "_is_available")
    
    def __init__(
            self,
            building: Building,
            allowed_count: int = 1,
        ) -> None:
        if allowed_count < 0:
            raise ValueError(
                f"allowed_count must be >= 0 (got {allowed_count}) for building \"{building.id}\"."
            )
        self._building: Building = building
        self._allowed_count: int = allowed_count
        self._current_count: int = 0
        self._is_available: bool = allowed_count > 0
    
    @property
    def building(self) -> Building:
        return self._building
    
    @property
    def allowed_count(self) -> int:
        return self._allowed_count
    
    @property
    def current_count(self) -> int:
        return self._current_count
    
    @property
    def is_available(self) -> bool:
        return self._is_available
    
    def increment_count(self) -> None:
        """
        Increment the count of this building in the city by one.
        
        Raises:
            ValueError: If the building is no longer available for construction (i.e. `is_available` is False).
            RuntimeError: If incrementing would cause `current_count` to exceed `allowed_count`. This indicates a logic
                error elsewhere in the validation or graph traversal process.
        
        Side effects:
            - Increases `current_count` by one.
            - If `current_count` reaches `allowed_count`, sets `is_available` to False.
        """
        if not self._is_available:
            raise ValueError(
                f"Cannot build \"{self._building.id}\": "
                f"limit of {self._allowed_count} reached (current = {self._current_count})."
            )
        
        if self._current_count + 1 > self._allowed_count:
            raise RuntimeError(
                f"Internal error: \"{self._building.id}\" exceeded allowed_count. "
                f"current = {self._current_count}, allowed = {self._allowed_count}"
            )
        
        self._current_count += 1
        
        if self._current_count == self.allowed_count:
            self._is_available = False
    
    def __repr__(self) -> str:
        return (
            f"_CityBuildingNode(id = \"{self.building.id}\", "
            f"count = {self._current_count}/{self._allowed_count}, "
            f"is_available = {self._is_available})"
        )


class _CityBuildingsGraph:
    
    def __init__(
            self,
            city: City,
        ) -> None:
        self.city: City = city
        self.nodes: dict[str, _CityBuildingNode] = {}
        self._initialize_nodes()
    
    def _initialize_nodes(self) -> None:
        """
        Create _CityBuildingNode instances for all buildings in _BUILDINGS and store them in self.nodes.
        """
        allowed_counts: dict[str, int] = self._calculate_allowed_counts()
        
        for building_id in _BUILDINGS:
            self.nodes[building_id] = _CityBuildingNode(
                building = Building(id = building_id),
                allowed_count = allowed_counts[building_id],
            )
    
    def _calculate_allowed_counts(self) -> BuildingsCount:
        """
        Determine the allowed_count for each building based on city state.
        """
        if self.city.is_fort:
            allowed_counts: BuildingsCount = {building_id: 0 for building_id in _BUILDINGS}
            allowed_counts["fort"] = 1
            return allowed_counts
        
        basic_production_buildings: list[str] = [
            "farm",
            "large_farm",
            "mine",
            "large_mine",
            "lumber_mill",
            "large_lumber_mill",
        ]
        
        allowed_counts: BuildingsCount = {building_id: 1 for building_id in _BUILDINGS}
        
        total_spots: int = _CityValidator.MAX_BUILDINGS_PER_CITY[self.city.get_hall().id]
        
        pre_occupied_spots: int = self.city.geo_features.lakes \
            + self.city.geo_features.rock_outcrops \
            + self.city.geo_features.mountains
        
        if self.city.has_supply_dump:
            pre_occupied_spots += 1
        
        for building_id in _BUILDINGS:
            # Cities that are not forts, cannot build the fort
            if building_id == "fort":
                allowed_counts[building_id] = 0
            
            #! I need to work-out the rules for the hunters_lodge, so for now, setting it to 0
            if building_id == "hunters_lodge":
                allowed_counts[building_id] = 0
            
            # Supply dumps are available in only three cities. There's only one per city and they are either there from
            # the start or they are not. They cannot be deleted.
            if building_id == "supply_dump":
                if not self.city.has_supply_dump:
                    allowed_counts[building_id] = 0
            
            # We start by assuming that basic production buildings can build as many as there are building slots
            # available in that city. This is determined by the hall minus the pre_occupied_spots.
            if building_id in basic_production_buildings:
                allowed_counts[building_id] = total_spots - pre_occupied_spots
            
            # Adjustments for geo features
            if building_id == "fishing_village":
                allowed_counts[building_id] = self.city.geo_features.lakes
            
            if building_id == "outcrop_mine":
                allowed_counts[building_id] = self.city.geo_features.rock_outcrops
            
            if building_id == "mountain_mine":
                allowed_counts[building_id] = self.city.geo_features.mountains
            
            if building_id in ["forest", "hidden_grove"]:
                allowed_counts[building_id] = self.city.geo_features.forests
            
            # Adjustments for resource production potentials
            if building_id in ["farm", "large_farm", "vineyard", "fishing_village", "farmers_guild", "stables"]:
                if self.city.resource_potentials.food == 0:
                    allowed_counts[building_id] = 0
            
            if building_id in ["mine", "large_mine", "outcrop_mine", "mountain_mine", "miners_guild", "blacksmith"]:
                if self.city.resource_potentials.ore == 0:
                    allowed_counts[building_id] = 0
            
            if building_id in ["lumber_mill", "large_lumber_mill", "carpenters_guild", "fletcher"]:
                if self.city.resource_potentials.wood == 0:
                    allowed_counts[building_id] = 0
        
        return allowed_counts
    
    def traverse_and_add(self, building_id: str) -> None:
        """
        Traverse the graph using DFS to validate and add the given building.
        
        Args:
            building_id (str): The ID of the building to add.
        
        Raises:
            UnknownBuildingError: If the building does not exist.
            BuildingCannotBeAddedToTheCityError: If the building cannot be added (limit reached or unavailable).
        """
        if building_id not in self.nodes:
            raise UnknownBuildingError(f"No building with ID = \"{building_id}\" found.")
        
        start: _CityBuildingNode = self.nodes["village_hall"]
        visited: set[str] = set()
        
        def dfs(node: _CityBuildingNode) -> bool:
            if node.building.id == building_id:
                node.increment_count()
                self._propagate_replacements(node = node)
                return True
            
            visited.add(node.building.id)
            
            for child in self._get_children(node = node):
                if (
                    child.building.id not in visited
                    and dfs(node = child)
                ):
                    return True
            
            return False
        
        if not dfs(node = start):
            raise BuildingCannotBeAddedToTheCityError(f"Building \"{building_id}\" cannot be added.")
    
    def _propagate_replacements(self, node: _CityBuildingNode) -> None:
        """
        Walk upward and increment any replaced buildings in the chain.
        """
        replaced: str | None = node.building.replaces
        
        while replaced:
            parent_node: _CityBuildingNode = self.nodes[replaced]
            parent_node.increment_count()
            replaced = parent_node.building.replaces
    
    def _get_children(self, node: _CityBuildingNode) -> list[_CityBuildingNode]:
        """
        Get children nodes of the current node, based on building dependencies.
        """
        children: list[_CityBuildingNode] = []
        for candidate in self.nodes.values():
            for requirement in candidate.building.required_building:
                if node.building.id in requirement:
                    children.append(candidate)
                    break
        
        return children


# * ************** * #
# * CITY VALIDATOR * #
# * ************** * #

@dataclass
class _CityValidator:
    city: City
    
    POSSIBLE_CITY_HALLS: ClassVar[set[str]] = {"village_hall", "town_hall", "city_hall", "fort"}
    
    # The maximum number of buildings the city can have, not counting the hall itself.
    MAX_BUILDINGS_PER_CITY: ClassVar[BuildingsCount] = {
        "fort": 0,
        "village_hall": 4,
        "town_hall": 6,
        "city_hall": 8,
    }
    
    def _validate_halls(self) -> None:
        halls: BuildingsCount = {}
        
        for building in self.city.buildings:
            if building.id not in self.POSSIBLE_CITY_HALLS:
                continue
            
            if building.id in halls:
                halls[building.id] += 1
            else:
                halls[building.id] = 1
        
        if not halls:
            raise NoCityHallError(f"City must include a hall (Village, Town, or City).")
        
        if len(halls) > 1:
            raise TooManyHallsError(f"Too many halls for this city.")
        
        if list(halls.values())[0] != 1:
            raise TooManyHallsError(f"Too many halls for this city.")
    
    def _validate_number_of_buildings(self) -> None:
        number_of_declared_buildings: int = len(self.city.buildings)
        max_number_of_buildings_in_city: int = self.MAX_BUILDINGS_PER_CITY[self.city.get_hall().id]
        
        if number_of_declared_buildings > max_number_of_buildings_in_city + 1:
            
            if self.city.is_fort:
                raise FortsCannotHaveBuildingsError(
                    f"Forts cannot have buildings."
                )
            
            raise TooManyBuildingsError(
                f"Too many buildings for this city: "
                f"{number_of_declared_buildings} provided, "
                f"max of {max_number_of_buildings_in_city + 1} possible ({max_number_of_buildings_in_city} + hall)."
            )


# * ************ * #
# * CITY DISPLAY * #
# * ************ * #

class _CityDisplay:
    """
    Handles the rendering and display of a `City` object in a structured, styled terminal layout using the Rich library.
    
    Each `_CityDisplay` instance takes a `City` object and an optional `DisplayConfiguration` that allows
    customizing which sections are shown, their heights, and colors.
    
    Sections displayed:
        - City information (campaign and name)
        - Buildings list
        - Effect bonuses (city, buildings, workers, total)
        - Production (resource potentials, base production, bonuses, total, maintenance, balance)
        - Storage capacity (city, buildings, warehouse, supply dump, total)
        - Defenses (garrison, number of squadrons, squadron size)
    
    Public API:
        build_city_display() -> Panel
            Constructs a Rich Panel representing the city display layout.
        display_city() -> None
            Prints the city display to the console.
    """
    def __init__(
            self,
            city: City,
            configuration: DisplayConfiguration | None = None,
        ) -> None:
        self.city: City = city
        self._user_configuration: DisplayConfiguration = configuration or {}
        self.configuration: DisplayConfiguration = self._build_configuration()
    
    #* Display configuration
    def _build_default_configuration(self) -> DisplayConfiguration:
        sections: list[str] = [
            "city",
            "buildings",
            "effects",
            "production",
            "storage",
            "defenses",
        ]
        
        default_configuration: DisplayConfiguration = {}
        for section in sections:
            default_configuration[section] = {
                "include": True,
                "height": self._calculate_default_section_height(section = section),
                "color": DEFAULT_SECTION_COLORS.get(section, "white"),
            }
        
        return default_configuration
    
    def _calculate_default_section_height(self, section) -> int:
        match section:
            case "city":
                return 2
            case "buildings":
                return len(self.city.get_buildings_count(by = "id")) + 2
            case "effects":
                return 8
            case "production":
                return 8
            case "storage":
                return 8
            case "defenses":
                return 6
        
        return 0
    
    def _build_configuration(self) -> DisplayConfiguration:
        
        display_configuration: DisplayConfiguration = self._build_default_configuration()
        
        for section in display_configuration:
            section_config: DisplaySectionConfiguration = display_configuration[section]
            if section in self._user_configuration:
                display_configuration[section] = {**section_config, **self._user_configuration[section]}
        
        return display_configuration
    
    
    #* Display results
    def _build_city_information(self) -> Text:
        fort: str = f" (Fort)" if self.city.is_fort else ""
        
        city_information: Text = Text(
            text = f" {self.city.campaign} --- {self.city.name}{fort} ",
            style = "bold black on white",
            justify = "center",
        )
        return city_information
    
    def _build_city_buildings_list(self) -> Table:
        city_buildings_text: Text = Text()
        
        for building, qty in self.city.get_buildings_count(by = "name").items():
            city_buildings_text.append(text = f"  - {building} ({qty})\n")
        
        city_buildings_table: Table = Table(title = "Buildings", show_header = False, box = None, padding = (0, 1))
        city_buildings_table.add_column()
        city_buildings_table.add_row()
        city_buildings_table.add_row(city_buildings_text)
        
        return city_buildings_table
    
    def _build_city_effects_table(self) -> Table:
        table_style: Style = Style(color = self.configuration.get("effects", {}).get("color", "#5f5fff"))
        table: Table = Table(
            title = Text(text = "Effects", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Effect", header_style = "bold", justify = "center")
        table.add_column(header = "City", header_style = "bold", justify = "right")
        table.add_column(header = "Buildings", header_style = "bold", justify = "right")
        table.add_column(header = "Workers", header_style = "bold", justify = "right")
        table.add_column(header = "Total", header_style = "bold", justify = "right")
        
        table.add_row(
            "Troop training",
            f"{self.city.effects.city.troop_training}",
            f"{self.city.effects.buildings.troop_training}",
            f"{self.city.effects.workers.troop_training}",
            Text(text = f"{self.city.effects.total.troop_training}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            "Pop. growth",
            f"{self.city.effects.city.population_growth}",
            f"{self.city.effects.buildings.population_growth}",
            f"{self.city.effects.workers.population_growth}",
            Text(text = f"{self.city.effects.total.population_growth}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            "Intelligence",
            f"{self.city.effects.city.intelligence}",
            f"{self.city.effects.buildings.intelligence}",
            f"{self.city.effects.workers.intelligence}",
            Text(text = f"{self.city.effects.total.intelligence}", style = table_style + Style(bold = True)),
        )
        
        return table
    
    def _build_city_production_table(self) -> Table:
        table_style: Style = Style(color = self.configuration.get("production", {}).get("color", "#228b22"))
        table: Table = Table(
            title = Text(text = "Production", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Resource", header_style = "bold", justify = "left")
        table.add_column(header = "Rss. pot.", header_style = "bold", justify = "right")
        table.add_column(header = "Base prod.", header_style = "bold", justify = "right")
        table.add_column(header = "Prod. bonus", header_style = "bold", justify = "right")
        table.add_column(header = "Total prod", header_style = "bold", justify = "right")
        table.add_column(header = "Maintenance", header_style = "bold", justify = "right")
        table.add_column(header = "Balance", header_style = "bold", justify = "right")
        
        table.add_row(
            f"Food",
            f"{self.city.resource_potentials.food}",
            f"{self.city.production.base.food}",
            f"{self.city.production.productivity_bonuses.food}",
            f"{self.city.production.total.food}",
            f"{-1 * self.city.production.maintenance_costs.food}",
            Text(text = f"{self.city.production.balance.food}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            f"Ore",
            f"{self.city.resource_potentials.ore}",
            f"{self.city.production.base.ore}",
            f"{self.city.production.productivity_bonuses.ore}",
            f"{self.city.production.total.ore}",
            f"{-1 * self.city.production.maintenance_costs.ore}",
            Text(text = f"{self.city.production.balance.ore}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            f"Wood",
            f"{self.city.resource_potentials.wood}",
            f"{self.city.production.base.wood}",
            f"{self.city.production.productivity_bonuses.wood}",
            f"{self.city.production.total.wood}",
            f"{-1 * self.city.production.maintenance_costs.wood}",
            Text(text = f"{self.city.production.balance.wood}", style = table_style + Style(bold = True)),
        )
        
        return table
    
    def _build_city_storage_table(self) -> Table:
        table_style: Style = Style(color = self.configuration.get("storage", {}).get("color", "purple"))
        table: Table = Table(
            title = Text(text = "Storage capacity", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Resource", header_style = "bold", justify = "left")
        table.add_column(header = "City", header_style = "bold", justify = "right")
        table.add_column(header = "Buildings", header_style = "bold", justify = "right")
        table.add_column(header = "Warehouse", header_style = "bold", justify = "right")
        table.add_column(header = "Supply dump", header_style = "bold", justify = "right")
        table.add_column(header = "Total", header_style = "bold", justify = "right")
        
        table.add_row(
            "Food",
            f"{self.city.storage.city.food}",
            f"{self.city.storage.buildings.food}",
            f"{self.city.storage.warehouse.food}",
            f"{self.city.storage.supply_dump.food}",
            Text(text = f"{self.city.storage.total.food}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            "Ore",
            f"{self.city.storage.city.ore}",
            f"{self.city.storage.buildings.ore}",
            f"{self.city.storage.warehouse.ore}",
            f"{self.city.storage.supply_dump.ore}",
            Text(text = f"{self.city.storage.total.ore}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            "Wood",
            f"{self.city.storage.city.wood}",
            f"{self.city.storage.buildings.wood}",
            f"{self.city.storage.warehouse.wood}",
            f"{self.city.storage.supply_dump.wood}",
            Text(text = f"{self.city.storage.total.wood}", style = table_style + Style(bold = True)),
        )
        
        return table
    
    def _build_defenses_table(self) -> Table:
        table_style: Style = Style(color = self.configuration.get("defenses", {}).get("color", "red"))
        table: Table = Table(
            title = Text(text = "Defenses", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Garrison", header_style = "bold", justify = "center")
        table.add_column(header = "Squadrons", header_style = "bold", justify = "center")
        table.add_column(header = "Squadron size", header_style = "bold", justify = "center")
        
        table.add_row(
            f"{self.city.defenses.garrison}",
            f"{self.city.defenses.squadrons}",
            f"{self.city.defenses.squadron_size}",
        )
        
        return table
    
    def build_city_display(self) -> Panel:
        """
        Constructs a Rich Panel representing the city display layout.
        
        This method assembles the various display components (tables, lists, etc.) into a single Rich Panel object,
        which can then be rendered.
        
        Returns:
            Panel: A `rich.panel.Panel` object ready for printing.
        """
        # Expected Layout
        # |---------------------------|
        # |      Campaign - City      |
        # |- - - - - - - - - - - - - -|
        # | List  |   Effects table   |
        # | of                        |
        # | build |                   |
        # | ings                      |
        # |- - - - - - - - - - - - - -|
        # |     Production table      |
        # |- - - - - - - - - - - - - -|
        # |  Storage capacity table   |
        # |- - - - - - - - - - - - - -|
        # |      Defenses table       |
        # |---------------------------|
        
        #* Include booleans
        include_city: bool = self.configuration.get("city", {}).get("include", True)
        include_buildings: bool = self.configuration.get("buildings", {}).get("include", True)
        include_effects: bool = self.configuration.get("effects", {}).get("include", True)
        include_production: bool = self.configuration.get("production", {}).get("include", True)
        include_storage: bool = self.configuration.get("storage", {}).get("include", True)
        include_defenses: bool = self.configuration.get("defenses", {}).get("include", True)
        
        #* Heights
        city_height: int = self.configuration.get("city", {}).get("height", 0) if include_city else 0
        buildings_height: int = self.configuration.get("buildings", {}).get("height", 0) if include_buildings else 0
        effects_height: int = self.configuration.get("effects", {}).get("height", 0) if include_effects else 0
        production_height: int = self.configuration.get("production", {}).get("height", 0) if include_production else 0
        storage_height: int = self.configuration.get("storage", {}).get("height", 0) if include_storage else 0
        defenses_height: int = self.configuration.get("defenses", {}).get("height", 0) if include_defenses else 0
        
        buildings_and_effects_height: int = max(buildings_height, effects_height)
        main_height: int = buildings_and_effects_height + production_height + storage_height + defenses_height
        
        total_layout_height: int = city_height + main_height + 2
        total_layout_width: int = 92
        
        #* Layout
        layout: Layout = Layout()
        
        layout.split(
            Layout(
                name = "header",
                size = city_height,
                ratio = 0,
                visible = include_city,
            ),
            Layout(
                name = "main",
                size = main_height,
                ratio = 0,
                visible = any([
                    include_buildings,
                    include_effects,
                    include_production,
                    include_storage,
                    include_defenses,
                ]),
            ),
        )
        
        layout["header"].update(
            renderable = Align(renderable = self._build_city_information(), align = "center"),
        )
        
        layout["main"].split(
            Layout(
                name = "buildings_and_effects",
                size = buildings_and_effects_height,
                ratio = 0,
                visible = any([include_buildings, include_effects]),
            ),
            Layout(
                name = "production",
                size = production_height,
                ratio = 0,
                visible = include_production,
            ),
            Layout(
                name = "storage_capacity",
                size = storage_height,
                ratio = 0,
                visible = include_storage,
            ),
            Layout(
                name = "defenses",
                size = defenses_height,
                ratio = 0,
                visible = include_defenses,
            ),
        )
        
        layout["buildings_and_effects"].split_row(
            Layout(name = "buildings", ratio = 1),
            Layout(name = "effects", ratio = 2),
        )
        
        if include_buildings:
            layout["buildings"].update(
                renderable = Align(renderable = self._build_city_buildings_list(), align = "center"),
            )
        else:
            layout["buildings"].update(
                renderable = Align(renderable = "", align = "center"),
            )
        
        if include_effects:
            layout["effects"].update(
                renderable = Align(renderable = self._build_city_effects_table(), align = "center"),
            )
        else:
            layout["effects"].update(
                renderable = Align(renderable = "", align = "center"),
            )
        
        layout["production"].update(
            renderable = Align(renderable = self._build_city_production_table(), align = "center"),
        )
        
        layout["storage_capacity"].update(
            renderable = Align(renderable = self._build_city_storage_table(), align = "center"),
        )
        
        layout["defenses"].update(
            renderable = Align(renderable = self._build_defenses_table(), align = "center"),
        )
        
        return Panel(
            renderable = layout,
            width = total_layout_width,
            height = total_layout_height,
        )
    
    def display_city(self) -> None:
        """
        Prints the city display to the console.
        
        This method uses the `build_city_display` method to create the panel and then prints it to the terminal via a
        `rich.console.Console` instance.
        """
        console: Console = Console()
        console.print(self.build_city_display())
