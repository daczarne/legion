import yaml

from dataclasses import dataclass, field
from typing import ClassVar, Literal, TypedDict

from .building import Building, BuildingsCount
from .effects import EffectBonusesData, EffectBonuses
from .geo_features import GeoFeaturesData, GeoFeatures
from .resources import Resource, ResourceCollectionData, ResourceCollection


class CityDict(TypedDict):
    """
    This is a helper class meant to be used when reading defining cities using dictionaries. Its only purpose is to
    provide good type annotations and hints.
    """
    name: str
    campaign: str
    buildings: BuildingsCount


# * *********** * #
# * CITIES DATA * #
# * *********** * #

class CityData(TypedDict):
    """
    This is a helper class meant to be used when reading CityData from YAML or JSON files. Its only purpose is to
    provide good type annotations and hints.
    """
    campaign: str
    name: str
    resource_potentials: ResourceCollectionData
    geo_features: GeoFeaturesData
    effects: EffectBonusesData
    garrison: str

with open(file = "./data/cities.yaml", mode = "r") as file:
    cities_data: dict[Literal["cities"], list[CityData]] = yaml.safe_load(stream = file)

CITIES: list[CityData] = cities_data["cities"]


# * **** * #
# * CITY * #
# * **** * #

@dataclass(kw_only = True)
class CityEffectBonuses:
    """
    A helper class to model the city's effect bonuses. Should not be used outside this module.
    """
    city: EffectBonuses = field(default_factory = EffectBonuses)
    buildings: EffectBonuses = field(default_factory = EffectBonuses)
    workers: EffectBonuses = field(default_factory = EffectBonuses)
    total: EffectBonuses = field(default_factory = EffectBonuses)


@dataclass(kw_only = True)
class CityProduction:
    """
    A helper class to model the city's production. Should not be used outside this module.
    """
    base: ResourceCollection = field(default_factory = ResourceCollection)
    productivity_bonuses: ResourceCollection = field(default_factory = ResourceCollection)
    total: ResourceCollection = field(default_factory = ResourceCollection)
    maintenance_costs: ResourceCollection = field(default_factory = ResourceCollection)
    balance: ResourceCollection = field(default_factory = ResourceCollection)


@dataclass(kw_only = True)
class CityStorage:
    """
    A helper class to model the city's storage capacity. Should not be used outside this module.
    """
    city: ResourceCollection = field(default_factory = ResourceCollection)
    buildings: ResourceCollection = field(default_factory = ResourceCollection)
    warehouse: ResourceCollection = field(default_factory = ResourceCollection)
    supply_dump: ResourceCollection = field(default_factory = ResourceCollection)
    total: ResourceCollection = field(default_factory = ResourceCollection)


@dataclass(kw_only = True)
class CityDefenses:
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
        geo_features (GeoFeatures): Geographical features present in the city (mountains, lakes, etc).
        effects (CityEffectBonuses): Effect bonuses from the city, its buildings, and workers.
        production (CityProduction): Production statistics for the city.
        storage (CityStorage): Resource storage capacities of the city.
        defenses (CityDefenses): Defense of the city (number of squads and their size).
        focus (Resource | None): If a Resource, the highest producing resource of the city.
    
    Class Attributes:
        POSSIBLE_CITY_HALLS (set[str]): The valid hall building IDs for a city.
        MAX_WORKERS (BuildingsCount): Mapping of hall type to maximum number of workers the city can have.
        MAX_BUILDINGS_PER_CITY (BuildingsCount): Mapping of hall type to maximum allowed buildings the city can have.
    """
    campaign: str = field(init = True, default = "", repr = True, compare = True, hash = True)
    name: str = field(init = True, default = "", repr = True, compare = True, hash = True)
    buildings: list[Building] = field(init = True, default_factory = list, repr = False, compare = False, hash = False)
    
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
    
    effects: CityEffectBonuses = field(
        init = False,
        default_factory = CityEffectBonuses,
        repr = False,
        compare = False,
        hash = False,
    )
    production: CityProduction = field(
        init = False,
        default_factory = CityProduction,
        repr = False,
        compare = False,
        hash = False,
    )
    storage: CityStorage = field(
        init = False,
        default_factory = CityStorage,
        repr = False,
        compare = False,
        hash = False,
    )
    defenses: CityDefenses = field(
        init = False,
        default_factory = CityDefenses,
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
    POSSIBLE_CITY_HALLS: ClassVar[set[str]] = {"village_hall", "town_hall", "city_hall"}
    MAX_WORKERS: ClassVar[BuildingsCount] = {
        "village_hall": 18, # This value needs to be corrected. I think the correct number is 7.
        "town_hall": 18, # This value needs to be corrected. I think the correct number is 12.
        "city_hall": 18,
    }
    MAX_BUILDINGS_PER_CITY: ClassVar[BuildingsCount] = {
        "village_hall": 4,
        "town_hall": 6,
        "city_hall": 8,
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
    def _validate_halls(self) -> None:
        halls: BuildingsCount = {}
        
        for building in self.buildings:
            if building.id not in self.POSSIBLE_CITY_HALLS:
                continue
            
            if building.id in halls:
                halls[building.id] += 1
            else:
                halls[building.id] = 1
        
        if not halls:
            raise ValueError(f"City must include a hall (village, town, or city)")
        
        if len(halls) > 1:
            raise ValueError(f"Too many halls for this city")
        
        if list(halls.values())[0] != 1:
            raise ValueError(f"Too many halls for this city")
    
    def _validate_number_of_buildings(self) -> None:
        number_of_declared_buildings: int = len(self.buildings)
        max_number_of_buildings_in_city: int = self.MAX_BUILDINGS_PER_CITY[self.get_hall().id]
        
        if number_of_declared_buildings > max_number_of_buildings_in_city + 1:
            raise ValueError(
                f"Too many buildings for this city: "
                f"{number_of_declared_buildings} provided, "
                f"max of {max_number_of_buildings_in_city + 1} possible ({max_number_of_buildings_in_city} + hall)"
            )
    
    
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
            if building.id not in [*self.POSSIBLE_CITY_HALLS, "warehouse", "supply_dump"]:
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
        
        raise ValueError(f"No garrison found for {self.campaign} - {self.name}")
    
    def _calculate_garrison_size(self) -> int:
        if self.has_building(id = "large_fort"):
            return 4
        
        if self.has_building(id = "medium_fort"):
            return 3
        
        if self.has_building(id = "small_fort"):
            return 2
        
        return 1
    
    def _calculate_squadron_size(self) -> str:
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
        
        if self.production.balance.food == highest_balance:
            return Resource.FOOD
        
        if self.production.balance.ore == highest_balance:
            return Resource.ORE
        
        if self.production.balance.wood == highest_balance:
            return Resource.WOOD
    
    
    def __post_init__(self) -> None:
        self.resource_potentials = self._get_rss_potentials()
        self.geo_features = self._get_geo_features()
        
        #* Validate city
        self._validate_halls()
        self._validate_number_of_buildings()
        
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
        
        raise KeyError(f"No building with ID={id} found in {self.name}")
    
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
            if building.id not in self.POSSIBLE_CITY_HALLS:
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
