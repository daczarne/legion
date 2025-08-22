import yaml

from dataclasses import dataclass, field
from typing import ClassVar, Literal, TypedDict

from .building import BuildingsCount, BUILDINGS
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
class CityProduction:
    base: ResourceCollection = field(default_factory = ResourceCollection)
    productivity_bonuses: ResourceCollection = field(default_factory = ResourceCollection)
    total: ResourceCollection = field(default_factory = ResourceCollection)
    maintenance_costs: ResourceCollection = field(default_factory = ResourceCollection)
    balance: ResourceCollection = field(default_factory = ResourceCollection)


@dataclass(kw_only = True)
class CityDefenses:
    garrison: str = ""
    squadrons: int = 1
    squadron_size: str = "Small"


@dataclass(
    match_args = False,
    order = False,
    kw_only = True,
)
class City:
    campaign: str = field(init = True, default = "", repr = True, compare = True, hash = True)
    name: str = field(init = True, default = "", repr = True, compare = True, hash = True)
    buildings: BuildingsCount = field(init = True, default_factory = dict, repr = False, compare = False, hash = False)
    
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
    
    city_effects: EffectBonuses = field(
        init = False,
        default_factory = EffectBonuses,
        repr = False,
        compare = False,
        hash = False,
    )
    building_effects: EffectBonuses = field(
        init = False,
        default_factory = EffectBonuses,
        repr = False,
        compare = False,
        hash = False,
    )
    worker_effects: EffectBonuses = field(
        init = False,
        default_factory = EffectBonuses,
        repr = False,
        compare = False,
        hash = False,
    )
    total_effects: EffectBonuses = field(
        init = False,
        default_factory = EffectBonuses,
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
    
    city_storage: ResourceCollection = field(
        init = False,
        default_factory = ResourceCollection,
        repr = False,
        compare = False,
        hash = False,
    )
    buildings_storage: ResourceCollection = field(
        init = False,
        repr = False,
        default_factory = ResourceCollection,
        compare = False,
        hash = False,
    )
    warehouse_storage: ResourceCollection = field(
        init = False,
        default_factory = ResourceCollection,
        repr = False,
        compare = False,
        hash = False,
    )
    supply_dump_storage: ResourceCollection = field(
        init = False,
        default_factory = ResourceCollection,
        repr = False,
        compare = False,
        hash = False,
    )
    total_storage: ResourceCollection = field(
        init = False,
        default_factory = ResourceCollection,
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
    
    focus: Resource | None = field(init = False, default = None, repr = False, compare = False, hash = False)
    
    
    # Class variables
    MAX_WORKERS: ClassVar[int] = 18
    POSSIBLE_CITY_HALLS: ClassVar[set[str]] = {"village_hall", "town_hall", "city_hall"}
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
    
    
    #* Validate city buildings
    def _validate_halls(self) -> None:
        halls: BuildingsCount = {k: v for k, v in self.buildings.items() if k in self.POSSIBLE_CITY_HALLS}
        
        if not halls:
            raise ValueError(f"City must include a hall (village, town, or city)")
        
        if len(halls) > 1:
            raise ValueError(f"Too many halls for this city")
        
        if list(halls.values())[0] != 1:
            raise ValueError(f"Too many halls for this city")
    
    def _get_hall(self) -> str:
        halls: BuildingsCount = {k: v for k, v in self.buildings.items() if k in self.POSSIBLE_CITY_HALLS}
        return list(halls.keys())[0]
    
    def _validate_number_of_buildings(self) -> None:
        number_of_declared_buildings: int = sum(self.buildings.values())
        max_number_of_buildings_in_city: int = self.MAX_BUILDINGS_PER_CITY[self._get_hall()]
        
        if number_of_declared_buildings > max_number_of_buildings_in_city + 1:
            raise ValueError(
                f"Too many buildings for this city: "
                f"{number_of_declared_buildings} provided, "
                f"max of {max_number_of_buildings_in_city + 1} possible ({max_number_of_buildings_in_city} + hall)"
            )
    
    def _validate_unknown_buildings(self) -> None:
        unknown: set[str] = set(self.buildings) - BUILDINGS.keys()
        if unknown:
            raise ValueError(f"Unknown building(s): {", ".join(unknown)}")
    
    
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
            building_effects.troop_training += BUILDINGS[building].effect_bonuses.troop_training
            building_effects.population_growth += BUILDINGS[building].effect_bonuses.population_growth
            building_effects.intelligence += BUILDINGS[building].effect_bonuses.intelligence
        
        return building_effects
    
    def _calculate_worker_effects(self) -> EffectBonuses:
        """
        Calculates the effects produced by building workers.
        """
        worker_effects: EffectBonuses = EffectBonuses()
        
        for building in self.buildings:
            worker_effects.troop_training += BUILDINGS[building].effect_bonuses_per_worker.troop_training * BUILDINGS[building].max_workers
            worker_effects.population_growth += BUILDINGS[building].effect_bonuses_per_worker.population_growth * BUILDINGS[building].max_workers
            worker_effects.intelligence += BUILDINGS[building].effect_bonuses_per_worker.intelligence * BUILDINGS[building].max_workers
        
        return worker_effects
    
    def _calculate_total_effects(self) -> EffectBonuses:
        """
        Calculate the total effects (base + given by buildings and its workers).
        """
        total_effects: EffectBonuses = EffectBonuses()
        
        total_effects.troop_training = (
            self.city_effects.troop_training
            + self.building_effects.troop_training
            + self.worker_effects.troop_training
        )
        total_effects.population_growth = (
            self.city_effects.population_growth
            + self.building_effects.population_growth
            + self.worker_effects.population_growth
        )
        total_effects.intelligence = (
            self.city_effects.intelligence
            + self.building_effects.intelligence
            + self.worker_effects.intelligence
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
        
        for building, qty_buildings in self.buildings.items():
            
            production_per_worker: ResourceCollection = BUILDINGS[building].productivity_per_worker
            max_workers: int = BUILDINGS[building].max_workers
            
            # Production per worker
            prod_per_worker_food: int = int(floor(production_per_worker.food * self.resource_potentials.food / 100.0))
            prod_per_worker_ore: int = int(floor(production_per_worker.ore * self.resource_potentials.ore / 100.0))
            prod_per_worker_wood: int = int(floor(production_per_worker.wood * self.resource_potentials.wood / 100.0))
            
            # Base production
            base_production_food: int = prod_per_worker_food * qty_buildings * max_workers
            base_production_ore: int = prod_per_worker_ore * qty_buildings * max_workers
            base_production_wood: int = prod_per_worker_wood * qty_buildings * max_workers
            
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
            productivity_bonuses.food += BUILDINGS[building].productivity_bonuses.food
            productivity_bonuses.ore += BUILDINGS[building].productivity_bonuses.ore
            productivity_bonuses.wood += BUILDINGS[building].productivity_bonuses.wood
        
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
            maintenance_costs.food += BUILDINGS[building].maintenance_cost.food
            maintenance_costs.ore += BUILDINGS[building].maintenance_cost.ore
            maintenance_costs.wood += BUILDINGS[building].maintenance_cost.wood
        
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
        return BUILDINGS[self._get_hall()].storage_capacity
    
    def _calculate_buildings_storage(self) -> ResourceCollection:
        buildings_storage: ResourceCollection = ResourceCollection()
        
        for building, qty in self.buildings.items():
            if building not in [*self.POSSIBLE_CITY_HALLS, "warehouse", "supply_dump"]:
                buildings_storage.food += BUILDINGS[building].storage_capacity.food * qty
                buildings_storage.ore += BUILDINGS[building].storage_capacity.ore * qty
                buildings_storage.wood += BUILDINGS[building].storage_capacity.wood * qty
        
        return buildings_storage
    
    def _calculate_warehouse_storage(self) -> ResourceCollection:
        if "warehouse" in self.buildings:
            return BUILDINGS["warehouse"].storage_capacity
        
        return ResourceCollection()
    
    def _calculate_supply_dump_storage(self) -> ResourceCollection:
        if "supply_dump" in self.buildings:
            return BUILDINGS["supply_dump"].storage_capacity
        
        return ResourceCollection()
    
    def _calculate_total_storage_capacity(self) -> ResourceCollection:
        """
        Calculate the total effects (base + given by buildings and its workers).
        """
        total_storage: ResourceCollection = ResourceCollection()
        
        total_storage.food = (
            self.city_storage.food
            + self.buildings_storage.food
            + self.warehouse_storage.food
            + self.supply_dump_storage.food
        )
        total_storage.ore = (
            self.city_storage.ore
            + self.buildings_storage.ore
            + self.warehouse_storage.ore
            + self.supply_dump_storage.ore
        )
        total_storage.wood = (
            self.city_storage.wood
            + self.buildings_storage.wood
            + self.warehouse_storage.wood
            + self.supply_dump_storage.wood
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
        if "large_fort" in self.buildings:
            return 4
        
        if "medium_fort" in self.buildings:
            return 3
        
        if "small_fort" in self.buildings:
            return 2
        
        return 1
    
    def _calculate_squadron_size(self) -> str:
        if "quartermaster" in self.buildings:
            return "Huge"
        
        if "barracks" in self.buildings:
            return "Large"
        
        if any(fort in self.buildings for fort in ["small_fort", "medium_fort", "large_fort"]):
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
        self._validate_unknown_buildings()
        self._validate_halls()
        self._validate_number_of_buildings()
        
        #* Effect bonuses
        self.city_effects = self._get_city_effects()
        self.building_effects = self._calculate_building_effects()
        self.worker_effects = self._calculate_worker_effects()
        self.total_effects = self._calculate_total_effects()
        
        #* Production
        self.production.base = self._calculate_base_production()
        self.production.productivity_bonuses = self._calculate_productivity_bonuses()
        self.production.total = self._calculate_total_production()
        self.production.maintenance_costs = self._calculate_maintenance_costs()
        self.production.balance = self._calculate_production_balance()
        
        #* Storage
        self.city_storage = self._calculate_city_storage()
        self.buildings_storage = self._calculate_buildings_storage()
        self.warehouse_storage = self._calculate_warehouse_storage()
        self.supply_dump_storage = self._calculate_supply_dump_storage()
        self.total_storage = self._calculate_total_storage_capacity()
        
        #* Defenses
        self.defenses = CityDefenses(
            garrison = self._get_garrison(),
            squadrons = self._calculate_garrison_size(),
            squadron_size = self._calculate_squadron_size(),
        )
        
        #* Focus
        self.focus = self._find_city_focus()
