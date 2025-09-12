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

from dataclasses import dataclass, field
from typing import ClassVar, Literal, TypedDict

import yaml
from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .building import _BUILDINGS, Building, BuildingsCount
from .display import DEFAULT_SECTION_COLORS, DisplayConfiguration, DisplaySectionConfiguration
from .effects import EffectBonuses, EffectBonusesData
from .exceptions import (
    CityNotFoundError,
    FortsCannotHaveBuildingsError,
    InvalidBuidlingConfigurationError,
    MoreThanOneGuildTypeError,
    MoreThanOneHallTypeError,
    NoCityHallError,
    TooManyBuildingsError,
    TooManyGuildsError,
    TooManyHallsError,
    UnknownBuildingStaffingStrategyError,
)
from .geo_features import GeoFeatures, GeoFeaturesData
from .resources import Resource, ResourceCollection, ResourceCollectionData


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


class City:
    """
    Represents a city in the game, including its properties, buildings, and derived statistics.
    
    This class encapsulates all the data and logic related to a city, from its fundamental attributes like name and
    campaign to complex derived statistics such as production, storage capacity, and military defenses. It serves as a
    comprehensive model for a city, ensuring all its properties are correctly validated and calculated upon
    instantiation.
    
    Class Variables:
        POSSIBLE_HALLS (ClassVar[set[str]]): A set of building IDs that are recognized as city halls.
        POSSIBLE_GUILDS (ClassVar[set[str]]): A set of building IDs that are recognized as guilds.
        MAX_BUILDINGS (ClassVar[BuildingsCount]): A dictionary mapping each hall type to the maximum number of non-hall
            buildings it can support.
        MAX_WORKERS (ClassVar[BuildingsCount]): A dictionary mapping each hall type to the maximum number of workers it
            can support.
    
    Args:
        campaign (str): The identifier of the campaign the city belongs to.
        name (str): The name of the city, which is used to look up its data from a central repository.
        buildings (list[Building]): A list of `Building` objects that exist in the city.
        staffing_strategy (str): The name of the staffing strategy to be used. Defaults to "production_first". The
            strategy determines how workers that have not being assigned at creation time will be assigned. This is not
            relevant when creating cities with `from_buildings_count()` method as all buildings are created with zero
            workers. But if the city is created based on a list of buildings, the worker assignments introduced at
            creation time will always be respected. The only exception to this rule is the `zero` strategy, which will
            set the assigned workers of all buildings to zero.
            
            Possible values are:
            
            - "zero" will set the assigned workers for all buildings to zero.
            - "none" will not assign any additional workers to any buildings. This is relevant when creating cities by
                passing collections of buildings that already assign workers to buildings.
            - "production_first" will first assign workers production-buildings and then effects-buildings.
            - "production_only" will only assign workers to production-buildings.
            - "effects_first" will first assign workers effects-buildings and then production-buildings.
            - "effects_only" will only assign workers to effects-buildings.
            
            The staffing of production-buildings always happens sorting buildings by productivity (descending). This
            means that production-buildings will be staffed in the following order:
            
            1. "large_farm" (3 workers)
            2. "large_mine" (3 workers)
            3. "large_lumber_mill" (3 workers)
            4. "vineyard" (3 workers)
            5. "fishing_village" (3 workers)
            6. "outcrop_mine" (2 workers)
            7. "farm" (3 workers)
            8. "mine" (3 workers)
            9. "lumber_mill" (3 workers)
            10. "mountain_mine" (1 worker)
            11. "hunters_lodge" (3 workers)
            
            In all cases, assignment of workers will stop once there are no more workers available in the city.
    
    Raises:
        CityNotFoundError: If no city data is found for the given campaign and name.
        NoCityHallError: If the city does not include a valid hall ("village_hall", "town_hall", or "city_hall").
        MoreThanOneHallTypeError: If the city contains more than one type of hall.
        TooManyHallsError: If the city contains multiple halls of the same type.
        FortsCannotHaveBuildingsError: If a "fort" is instantiated with buildings.
        TooManyBuildingsError: If the number of buildings exceeds the limit for the city.
        MoreThanOneGuildTypeError: If the city contains more than one guild type.
        TooManyGuildsError: If the city contains multiple guilds of the same type.
        UnknownBuildingStaffingStrategyError: If an unknown staffing strategy is passed.
    """
    
    # Set of possible halls and guilds.
    POSSIBLE_HALLS: ClassVar[set[str]] = {"fort", "village_hall", "town_hall", "city_hall"}
    POSSIBLE_GUILDS: ClassVar[set[str]] = {"farmers_guild", "carpenters_guild", "miners_guild"}
    
    # The maximum number of buildings a city can have, not counting the hall itself.
    MAX_BUILDINGS: ClassVar[BuildingsCount] = {
        "fort": 0,
        "village_hall": 4,
        "town_hall": 6,
        "city_hall": 8,
    }
    
    # The maximum number of workers a city can have.
    MAX_WORKERS: ClassVar[BuildingsCount] = {
        "fort": 0,
        "village_hall": 10,
        "town_hall": 14,
        "city_hall": 18,
    }
    
    __match_args__: ClassVar[tuple[str, str]] = ("campaign", "name")
    
    
    def __init__(
            self,
            campaign: str,
            name: str,
            buildings: list[Building],
            staffing_strategy: str = "production_first",
        ) -> None:
        self._city_data: _CityData = self._get_city_data(campaign = campaign, name = name)
        self.campaign: str = self._get_campaign()
        self.name: str = self._get_city_name()
        
        self.resource_potentials: ResourceCollection = self._get_rss_potentials()
        self.geo_features: GeoFeatures = self._get_geo_features()
        
        self.buildings: list[Building] = buildings
        
        self.is_fort: bool = self._is_fort()
        self._add_fort_to_buildings()
        
        self.has_supply_dump: bool = self._has_supply_dump()
        self._add_supply_dump_to_buildings()
        
        self._validate_halls()
        self.hall: Building = self._get_hall()
        
        self._validate_forts_have_no_other_buildings()
        self._validate_total_number_of_buildings()
        self._validate_building_counts()
        self._validate_guilds()
        self._validate_empty_building_spots()
        
        #* Staff buildings
        self._validate_staffing_strategy(staffing_strategy = staffing_strategy)
        self.staffing_strategy: str = staffing_strategy
        self.available_workers: int = City.MAX_WORKERS[self.hall.id]
        self.assigned_workers: int = self._updated_assigned_workers()
        self._staff_buildings()
        
        #* Calculate effects
        self.effects: _CityEffectBonuses = _CityEffectBonuses()
        self.effects.city = self._get_city_effects()
        self.effects.buildings = self._calculate_building_effects()
        self.effects.workers = self._calculate_worker_effects()
        self.effects.total = self._calculate_total_effects()
        
        #* Calculate production
        self.production: _CityProduction = _CityProduction()
        self.production.base = self._calculate_base_production()
        self.production.productivity_bonuses = self._calculate_productivity_bonuses()
        self.production.total = self._calculate_total_production()
        self.production.maintenance_costs = self._calculate_maintenance_costs()
        self.production.balance = self._calculate_production_balance()
        
        #* Calculate storage capacity
        self.storage: _CityStorage = _CityStorage()
        self.storage.city = self._calculate_city_storage()
        self.storage.buildings = self._calculate_buildings_storage()
        self.storage.warehouse = self._calculate_warehouse_storage()
        self.storage.supply_dump = self._calculate_supply_dump_storage()
        self.storage.total = self._calculate_total_storage_capacity()
        
        #* City defenses
        self.defenses: _CityDefenses = _CityDefenses()
        self.defenses.garrison = self._get_garrison()
        self.defenses.squadrons = self._calculate_garrison_size()
        self.defenses.squadron_size = self._calculate_squadron_size()
        
        #* City focus
        self.focus: Resource | None = self._find_city_focus()
    
    
    def __hash__(self) -> int:
        return hash((self.campaign, self.name))
    
    def __bool__(self) -> bool:
        return True
    
    def __contains__(self, building_id: str) -> bool:
        for building in self.buildings:
            if building.id == building_id:
                return True
        
        return False
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, City):
            return NotImplemented
        
        return self.campaign == other.campaign and self.name == other.name
    
    def __repr__(self) -> str:
        return (f"City(campaign = \"{self.campaign}\", name = \"{self.name}\"")
    
    def __str__(self) -> str:
        return f"{self.campaign} - {self.name}"
    
    
    #* Init and validation helpers
    def _get_city_data(self, campaign: str, name: str) -> _CityData:
        for city in CITIES:
            if (
                city["campaign"] == campaign
                and city["name"] == name
            ):
                return city
        
        raise CityNotFoundError(
            f"No city found for campaing = \"{campaign}\" and name = \"{name}\""
        )
    
    def _get_campaign(self) -> str:
        return self._city_data["campaign"]
    
    def _get_city_name(self) -> str:
        return self._city_data["name"]
    
    def _get_rss_potentials(self) -> ResourceCollection:
        return ResourceCollection(**self._city_data["resource_potentials"])
    
    def _get_geo_features(self) -> GeoFeatures:
        return GeoFeatures(**self._city_data["geo_features"])
    
    def _is_fort(self) -> bool:
        return self._city_data["is_fort"]
    
    def _add_fort_to_buildings(self) -> None:
        if not self.is_fort:
            return
        
        if self.has_building(id = "fort"):
            return
        
        self.buildings.append(Building(id = "fort"))
    
    def _has_supply_dump(self) -> bool:
        return self._city_data["has_supply_dump"]
    
    def _add_supply_dump_to_buildings(self) -> None:
        if not self.has_supply_dump:
            return
        
        if self.has_building(id = "supply_dump"):
            return
        
        self.buildings.append(Building(id = "supply_dump"))
    
    def _validate_halls(self) -> None:
        halls: BuildingsCount = {}
        
        for building in self.buildings:
            if building.id not in City.POSSIBLE_HALLS:
                continue
            
            if building.id in halls:
                halls[building.id] += 1
            else:
                halls[building.id] = 1
        
        if not halls:
            raise NoCityHallError(f"City must include a hall (Village, Town, or City).")
        
        if len(halls) > 1:
            raise MoreThanOneHallTypeError(f"Only one hall per city is allowed. Found {", ".join(halls.keys())}.")
        
        if list(halls.values())[0] != 1:
            raise TooManyHallsError(f"Too many halls for this city.")
    
    def _get_hall(self) -> Building:
        for building in self.buildings:
            if building.id not in City.POSSIBLE_HALLS:
                continue
            
            return building
        
        raise NoCityHallError(f"City must include a hall (Village, Town, or City).")
    
    def _calculate_allowed_building_counts(self) -> BuildingsCount:
        if self.is_fort:
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
        
        buildings_that_require_town_hall: list[str] = [
            "city_hall",
            "bath_house",
            "hospital",
            "vineyard",
            "training_ground",
            "bordello",
            "gladiator_school",
            "medium_fort",
            "barracks",
            "temple",
        ]
        
        buildings_that_require_city_hall: list[str] = [
            "large_fort",
            "quartermaster",
            "basilica",
            "imperial_residence",
            "farmers_guild",
            "carpenters_guild",
            "miners_guild",
        ]
        
        allowed_counts: BuildingsCount = {building_id: 1 for building_id in _BUILDINGS}
        
        total_spots: int = City.MAX_BUILDINGS[self.hall.id]
        
        pre_occupied_spots: int = self.geo_features.lakes \
            + self.geo_features.rock_outcrops \
            + self.geo_features.mountains
        
        if self.has_supply_dump:
            pre_occupied_spots += 1
        
        for building_id in _BUILDINGS:
            
            # Cities that are not forts, cannot build the fort, they have it from the start.
            if building_id == "fort":
                allowed_counts[building_id] = 0
                continue
            
            # Hunters' lodges are special buildings. They require all rss to be present in the city, but can only
            # be built in cities with town and village halls. Once the city hall is built, the city loses the availity
            # to build hunters' lodges.
            if building_id == "hunters_lodge":
                
                if not (
                    self.resource_potentials.food > 0
                    and self.resource_potentials.ore > 0
                    and self.resource_potentials.wood > 0
                ):
                    allowed_counts[building_id] = 0
                    continue
                
                if self.hall.id == "city_hall":
                    allowed_counts[building_id] = City.MAX_BUILDINGS["town_hall"] - pre_occupied_spots
                    continue
                
                allowed_counts[building_id] = total_spots - pre_occupied_spots
            
            # Supply dumps are available in only three cities. There's only one per city and they are either there from
            # the start or they are not. They cannot be deleted.
            if building_id == "supply_dump":
                if not self.has_supply_dump:
                    allowed_counts[building_id] = 0
            
            # We start by assuming that basic production buildings can build as many as there are building slots
            # available in that city. This is determined by the hall minus the pre_occupied_spots.
            if building_id in basic_production_buildings:
                allowed_counts[building_id] = total_spots - pre_occupied_spots
            
            # Adjustments for geo features
            if building_id == "fishing_village":
                allowed_counts[building_id] = self.geo_features.lakes
            
            if building_id == "outcrop_mine":
                allowed_counts[building_id] = self.geo_features.rock_outcrops
            
            if building_id == "mountain_mine":
                allowed_counts[building_id] = self.geo_features.mountains
            
            if building_id in ["forest", "hidden_grove"]:
                allowed_counts[building_id] = self.geo_features.forests
            
            # Adjustments for resource production potentials
            if building_id in ["farm", "large_farm", "vineyard", "fishing_village", "farmers_guild", "stables"]:
                if self.resource_potentials.food == 0:
                    allowed_counts[building_id] = 0
            
            if building_id in ["mine", "large_mine", "outcrop_mine", "mountain_mine", "miners_guild", "blacksmith"]:
                if self.resource_potentials.ore == 0:
                    allowed_counts[building_id] = 0
            
            if building_id in ["lumber_mill", "large_lumber_mill", "carpenters_guild", "fletcher"]:
                if self.resource_potentials.wood == 0:
                    allowed_counts[building_id] = 0
            
            # Adjustments for hall level
            if building_id in [*buildings_that_require_town_hall, *buildings_that_require_city_hall]:
                if self.hall.id in ["fort", "village_hall"]:
                    allowed_counts[building_id] = 0
            
            if building_id in buildings_that_require_city_hall:
                if self.hall.id in ["fort", "village_hall", "town_hall"]:
                    allowed_counts[building_id] = 0
        
        return allowed_counts
    
    def _validate_forts_have_no_other_buildings(self) -> None:
        if self.is_fort:
            if len(self.buildings) > 1:
                raise FortsCannotHaveBuildingsError(
                    f"Forts cannot have buildings."
                )
    
    def _validate_total_number_of_buildings(self) -> None:
        number_of_declared_buildings: int = len(self.buildings)
        max_number_of_buildings_in_city: int = City.MAX_BUILDINGS[self.hall.id]
        
        if number_of_declared_buildings > max_number_of_buildings_in_city + 1:
            
            raise TooManyBuildingsError(
                f"Too many buildings for this city: "
                f"{number_of_declared_buildings} provided, "
                f"max of {max_number_of_buildings_in_city + 1} possible ({max_number_of_buildings_in_city} + hall)."
            )
    
    def _validate_building_counts(self) -> None:
        allowed_building_counts: BuildingsCount = self._calculate_allowed_building_counts()
        current_building_counts: BuildingsCount = self.get_buildings_count(by = "id")
        
        for building_id, current_count in current_building_counts.items():
            if current_count > allowed_building_counts[building_id]:
                raise TooManyBuildingsError(
                    f"Too many buildings of type \"{building_id}\". "
                    f"Allowed {allowed_building_counts[building_id]}, but found {current_count}."
                )
    
    def _validate_guilds(self) -> None:
        guilds: BuildingsCount = {}
        
        for building in self.buildings:
            if building.id not in City.POSSIBLE_GUILDS:
                continue
            
            if building.id in guilds:
                guilds[building.id] += 1
            else:
                guilds[building.id] = 1
        
        if len(guilds) > 1:
            raise MoreThanOneGuildTypeError(
                f"Only one guild per city is allowed. Found {", ".join(guilds.keys())}."
            )
        
        if len(guilds) == 1:
            if list(guilds.values())[0] != 1:
                raise TooManyGuildsError(f"Too many guilds for this city.")
    
    def _validate_empty_building_spots(self) -> None:
        # Throughout this method the concept of an "empty building spot" reflects more of an actual or potential
        # characteristic of a building spot. A more appropriate name would probably be "empty or emptyable building
        # spot" but I will keep it as "empty" for simplicity and brevity.
        
        qty_buildings_that_require_empty_spot: int = 0
        
        for building in self.buildings:
            if all([
                # Non-buildable buildings cannot be built. The city either starts with them, or it will never have them.
                # The only non-buildable "building" that is deletable is the forest. But those validations are already
                # considered elsewhere.
                building.is_buildable,
                # Buildings that require geo features can only be built in geo-feature spots.
                building.required_geo is None,
                # The hall has its own dedicated "building" spot.
                building.id != self.hall.id,
            ]):
                qty_buildings_that_require_empty_spot += 1
        
        supply_dump_spot: int = 1 if self.has_supply_dump else 0
        qty_geo_building_spots: int = self.geo_features.lakes + self.geo_features.rock_outcrops + self.geo_features.mountains
        qty_empty_building_spots: int = City.MAX_BUILDINGS[self.hall.id] - supply_dump_spot - qty_geo_building_spots
        
        if qty_buildings_that_require_empty_spot > qty_empty_building_spots:
            raise InvalidBuidlingConfigurationError(
                f"Building configuration is not possible for {self.name}. "
            )
    
    def _validate_staffing_strategy(self, staffing_strategy: str) -> None:
        allowed_building_staffing_strategies: list[str] = [
            "zero",
            "none",
            "production_first",
            "production_only",
            "effects_first",
            "effects_only",
        ]
        
        if staffing_strategy not in allowed_building_staffing_strategies:
            raise UnknownBuildingStaffingStrategyError(
                f"Unknown building staffing strategy. " \
                f"Allowed strategies: {" ".join(allowed_building_staffing_strategies)}."
            )
    
    def _updated_assigned_workers(self) -> int:
        return sum([building.workers for building in self.buildings])
    
    def _staff_building(self, building: Building) -> None:
        while (
            self.assigned_workers < self.available_workers
            and building.workers < building.max_workers
        ):
            building.add_workers(qty = 1)
            self.assigned_workers += 1
    
    def _staff_buildings(self) -> None:
        if self.staffing_strategy == "none":
            return
        
        if self.staffing_strategy == "zero":
            for building in self.buildings:
                building.set_workers(qty = 0)
            
            self.assigned_workers = self._updated_assigned_workers()
            
            return
        
        # Production buildings sorted by productivity levels. The prod. level of each building is determined by the
        # total sum of all produced rss. For most buildings, this is equal to the product of the one rss it produces
        # times the number of workers. The only exception is the HL which produces all 3 rss. Worker productivity is
        # calculated based on 100 prod. pot.
        production_buildings: dict[str, int] = {
            "large_farm": 36, # 12 * 3 = 36
            "large_mine": 36, # 12 * 3 = 36
            "large_lumber_mill": 36, # 12 * 3 = 36
            "vineyard": 30, # 10 * 3 = 30
            "fishing_village": 27, # 9 * 3 = 27
            "outcrop_mine": 26, # 13 * 2 = 26
            "farm": 21, # 7 * 3 = 21
            "mine": 21, # 7 * 3 = 21
            "lumber_mill": 21, # 7 * 3 = 21
            "mountain_mine": 20, # 20 * 1 = 20
            "hunters_lodge": 18, # (2 * 3) * 3 = 18
        }
        
        production_buildings_in_city: list[Building] = sorted(
            [building for building in self.buildings if building.id in production_buildings],
            key = lambda building: production_buildings[building.id],
            reverse = True,
        )
        non_production_buildings_in_city: list[Building] = [
            building for building in self.buildings if building.id not in production_buildings
        ]
        
        if self.staffing_strategy in ["production_first", "production_only"]:
            for building in production_buildings_in_city:
                self._staff_building(building = building)
            
            if self.staffing_strategy == "production_first":
                for building in non_production_buildings_in_city:
                    self._staff_building(building = building)
        
        if self.staffing_strategy in ["effects_first", "effects_only"]:
            for building in non_production_buildings_in_city:
                self._staff_building(building = building)
            
            if self.staffing_strategy == "effects_first":
                for building in production_buildings_in_city:
                    self._staff_building(building = building)
    
    
    #* Effect bonuses
    def _get_city_effects(self) -> EffectBonuses:
        return EffectBonuses(**self._city_data["effects"])
    
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
            worker_effects.troop_training += building.effect_bonuses_per_worker.troop_training * building.workers
            worker_effects.population_growth += building.effect_bonuses_per_worker.population_growth * building.workers
            worker_effects.intelligence += building.effect_bonuses_per_worker.intelligence * building.workers
        
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
            
            # Production per worker
            prod_per_worker_food: int = int(floor(productivity_per_worker.food * self.resource_potentials.food / 100.0))
            prod_per_worker_ore: int = int(floor(productivity_per_worker.ore * self.resource_potentials.ore / 100.0))
            prod_per_worker_wood: int = int(floor(productivity_per_worker.wood * self.resource_potentials.wood / 100.0))
            
            # Base production
            base_production_food: int = prod_per_worker_food * building.workers
            base_production_ore: int = prod_per_worker_ore * building.workers
            base_production_wood: int = prod_per_worker_wood * building.workers
            
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
        return self.hall.storage_capacity
    
    def _calculate_buildings_storage(self) -> ResourceCollection:
        buildings_storage: ResourceCollection = ResourceCollection()
        
        for building in self.buildings:
            if building.id not in [*City.POSSIBLE_HALLS, "warehouse", "supply_dump"]:
                buildings_storage.food += building.storage_capacity.food
                buildings_storage.ore += building.storage_capacity.ore
                buildings_storage.wood += building.storage_capacity.wood
        
        return buildings_storage
    
    def _calculate_warehouse_storage(self) -> ResourceCollection:
        if self.has_building(id = "warehouse"):
            return self.get_building(id = "warehouse").storage_capacity
        
        return ResourceCollection()
    
    def _calculate_supply_dump_storage(self) -> ResourceCollection:
        if self.has_supply_dump:
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
    
    
    #* City defenses
    def _get_garrison(self) -> str:
        return self._city_data["garrison"]
    
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
        highest_balance: int = max(
            self.production.balance.food,
            self.production.balance.ore,
            self.production.balance.wood
        )
        
        if highest_balance < 0:
            return None
        
        rss_with_highest_balance: list[str] = self.production.balance.find_fields_by_value(value = highest_balance)
        
        if len(rss_with_highest_balance) > 1:
            return None
        
        return Resource(value = rss_with_highest_balance[0])
    
    
    #* Alternative city creator methods
    @classmethod
    def from_buildings_count(
            cls,
            campaign: str,
            name: str,
            buildings: BuildingsCount,
            staffing_strategy: str = "production_first",
        ) -> "City":
        """
        Create a `City` instance from a count of buildings. The count must be a dictionary with building IDs as keys
        and the quantity of each building type as values.
        
        This method expands the building counts into actual `Building` objects and initializes a new city with them.
        This implies that you can pass 0-count buildings and they will automatically be ignored.
        
        You can not specify the number of workers for each building if you use this method for creating cities.
        
        Args:
            campaign (str): The campaign identifier the city belongs to.
            name (str): The name of the city.
            buildings (BuildingsCount): A dictionary mapping building IDs to quantities.
            staffing_strategy (str): The name of the staffing strategy to be used. Possible values are
                "production_first", "production_only", "effects_first", "effects_only". Defaults to "production_first".
        
        Returns:
            City: a new `City` instance populated with the given buildings and the given workers' distribution.
        """
        city_buildings: list[Building] = []
        
        for id, qty in buildings.items():
            for _ in range(qty):
                city_buildings.append(Building(id = id))
        
        return cls(
            campaign = campaign,
            name = name,
            buildings = city_buildings,
            staffing_strategy = staffing_strategy,
        )
    
    
    def get_building(self, id: str) -> Building:
        """
        Retrieve a building from the city by its ID. In case the city has more than one it will return the first one.
        
        Args:
            id (str): The building ID to search for.
        
        Returns:
            Building: The first building in the city with the given ID.
        
        Raises:
            KeyError: If no building with the given ID exists in the city.
        """
        for building in self.buildings:
            if building.id == id:
                return building
        
        raise KeyError(f"No building with ID = \"{id}\" found in {self.name}.")
    
    def has_building(self, id: str) -> bool:
        """
        Check whether the city contains a building with the specified ID.
        
        Args:
            id (str): The building ID to search for.
        
        Returns:
            bool: True if the building is present, False otherwise.
        """
        for building in self.buildings:
            if building.id == id:
                return True
        
        return False
    
    def get_buildings_count(self, by: Literal["name", "id"]) -> BuildingsCount:
        """
        Count the number of buildings in the city grouped by ID or name.
        
        Args:
            by (Literal["name", "id"]): Whether to group counts by building name or ID.
        
        Returns:
            BuildingsCount: A dictionary mapping either building IDs or names to their respective counts.
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
