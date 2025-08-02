from dataclasses import dataclass, field
from typing import ClassVar, TypeAlias


from .buildings import (
    RssCollection,
    BUILDINGS,
)

from .city_data import CITIES


BuildingsCount: TypeAlias = dict[str, int]


@dataclass
class CityGeoFeatures:
    rock_outcrops: int = 0
    mountains: int = 0
    lakes: int = 0
    forests: int = 0


@dataclass
class CityEffects:
    troop_training: int = 0
    population_growth: int = 0
    intelligence: int = 0


@dataclass
class CityBuildings:
    buildings: BuildingsCount = field(default_factory = dict)
    
    MAX_NUMBER_OF_BUILDINGS_PER_CITY: ClassVar[int] = 9
    
    def __post_init__(self) -> None:
        # Ensure city_hall is always present
        if "city_hall" not in self.buildings:
            self.buildings["city_hall"] = 1
        
        unknown: set[str] = set(self.buildings) - BUILDINGS.keys()
        if unknown:
            raise ValueError(f"Unknown building(s): {', '.join(unknown)}")
        
        total: int = sum(self.buildings.values())
        if total > self.MAX_NUMBER_OF_BUILDINGS_PER_CITY:
            raise ValueError(f"Too many buildings: {total} (max allowed is {self.MAX_NUMBER_OF_BUILDINGS_PER_CITY})")
    
    def get_count(self, name: str) -> int:
        return self.buildings.get(name, 0)


@dataclass
class City:
    campaign: str
    name: str
    buildings: CityBuildings
    
    # Post init attrs
    resource_potentials: RssCollection = field(init = False)
    geo_features: CityGeoFeatures = field(init = False)
    city_effects: CityEffects = field(init = False)
    base_production: RssCollection = field(init = False)
    productivity_bonuses: RssCollection = field(init = False)
    total_production: RssCollection = field(init = False)
    maintenance_costs: RssCollection = field(init = False)
    balance: RssCollection = field(init = False)
    
    # Class variables
    RSS_BASE_PRODUCTIVITY_PER_WORKER: ClassVar[int] = 12
    MAX_WORKERS: ClassVar[int] = 18
    
    
    def _get_rss_potentials(self) -> RssCollection:
        """
        Finds the city supplied by the user in the directory of cities and returns its resource potentials.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return RssCollection(**city["resource_potentials"])
        
        return RssCollection()
    
    def _get_geo_features(self) -> CityGeoFeatures:
        """
        Finds the city supplied by the user in the directory of cities and returns its geo-features.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return CityGeoFeatures(**city["geo_features"])
        
        return CityGeoFeatures()
    
    def _get_base_effects(self) -> CityEffects:
        """
        Finds the city supplied by the user in the directory of cities and returns its effects.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return CityEffects(**city["effects"])
        
        return CityEffects()
    
    #* Validate city buildings
    # Validations need to include the following situations.
    # 
    # Rss buildings are allowed. This is because a city with, for example, rss potential of 0 for food, cannot create
    # food-producing buildings (like farms, vineyards, or fishing villages), even if it has a lake (the lake is, sadly,
    # a waisted building spot in this case).
    # 
    # Guilds. Building guilds requires the production building itself. For example, if there are no farms, there can be
    # no farmers guild. Similarly, if there are no lumber mills, there can be no carpenters guild, and so on.
    #
    # Additionally, there are other dependencies between buildings. For example, a city needs:
    #   farm or vineyard => stables
    #   lumber mill => fletcher
    #   mine (not outcrop or mountain) => blacksmith
    #   fort => quartermaster
    #   training grounds => other training facilities (like gladiator school, imperial residence, bordello)
    #
    # But, all dependencies can be bypassed by building the required building (e.g. a farm), then building the 
    # dependent building (e.g. stables), and then deleting the required building and using that spot to build something
    # else. Some of these dependencies makes sense to validate them because the dependent building makes no sense
    # without the dependency building. For example, no sense in having a city with a farmers guild, if the city has no
    # farms.
    #
    # Lastly, not all cities can accept all potential building scenarios. For example, a city with a lake and enough
    # food potential for a fishing village, "cannot" build 6 mines. Since there are only a maximum of 18 workers per
    # city, this configuration (1 fishing village + 6 mines) would mean that at least one of the buildings is not
    # staffed (potentially, even empty). The validation should warn against this scenario.
    
    #* Production calculations
    def _calculate_base_production(self) -> RssCollection:
        """
        Given the buildings in the city, it calculates the base production of those buildings for each resource. Base
        production is defined here as production before productivity bonuses. It is determined only by the buildings
        and the city's production potential for each rss. Buildings are assumed to be fully staffed and fully upgraded.
        For example, "1 mine" means "1 large mine with all 3 workers".
        """
        from math import floor
        
        base_production: RssCollection = RssCollection()
        
        for building, qty_buildings in self.buildings.buildings.items():
            
            production_per_worker: RssCollection = BUILDINGS[building]["productivity_per_worker"]
            max_workers: int = BUILDINGS[building]["max_workers"]
            
            # Production per worker
            prod_per_worker_food: int = int(floor(production_per_worker.food * self.resource_potentials.food / 100.0))
            prod_per_worker_ore: int = int(floor(production_per_worker.ore * self.resource_potentials.ore / 100.0))
            prod_per_worker_wood: int = int(floor(production_per_worker.wood * self.resource_potentials.wood / 100.0))
            
            # Base production
            base_production_food: int = prod_per_worker_food * qty_buildings * max_workers
            base_production_ore: int = prod_per_worker_ore * qty_buildings * max_workers
            base_production_wood: int = prod_per_worker_wood * qty_buildings * max_workers
            
            base_production.food = base_production.food + base_production_food
            base_production.ore = base_production.ore + base_production_ore
            base_production.wood = base_production.wood + base_production_wood
        
        return base_production
    
    def _calculate_productivity_bonuses(self) -> RssCollection:
        """
        Based on the buildings found in the city, it calculates the productivity bonuses for each resource.
        """
        productivity_bonuses: RssCollection = RssCollection()
        
        for building in self.buildings.buildings:
            productivity_bonuses.food = productivity_bonuses.food + BUILDINGS[building]["productivity_bonus"].food
            productivity_bonuses.ore = productivity_bonuses.ore + BUILDINGS[building]["productivity_bonus"].ore
            productivity_bonuses.wood = productivity_bonuses.wood + BUILDINGS[building]["productivity_bonus"].wood
        
        return productivity_bonuses
    
    def _calculate_total_production(self) -> RssCollection:
        """
        Given the base production and the productivity bonuses of a city, it calculates the total production.
        """
        from math import floor
        
        total_production: RssCollection = RssCollection()
        
        total_production.food = int(floor(self.base_production.food * (1 + self.productivity_bonuses.food / 100)))
        total_production.ore = int(floor(self.base_production.ore * (1 + self.productivity_bonuses.ore / 100)))
        total_production.wood = int(floor(self.base_production.wood * (1 + self.productivity_bonuses.wood / 100)))
        
        return total_production
    
    def _calculate_maintenance_costs(self) -> RssCollection:
        """
        Based on the buildings found in the city, it calculates the maintenance costs for each resource.
        """
        maintenance_costs: RssCollection = RssCollection()
        
        for building in self.buildings.buildings:
            maintenance_costs.food = maintenance_costs.food + BUILDINGS[building]["maintenance_cost"].food
            maintenance_costs.ore = maintenance_costs.ore + BUILDINGS[building]["maintenance_cost"].ore
            maintenance_costs.wood = maintenance_costs.wood + BUILDINGS[building]["maintenance_cost"].wood
        
        return maintenance_costs
    
    def _calculate_balance(self) -> RssCollection:
        """
        Calculate the balance for each rss. The balance is the difference between the total production and the
        maintenance costs.
        """
        balance: RssCollection = RssCollection()
        
        balance.food = self.total_production.food - self.maintenance_costs.food
        balance.ore = self.total_production.ore - self.maintenance_costs.ore
        balance.wood = self.total_production.wood - self.maintenance_costs.wood
        
        return balance
    
    
    #* Effects calculations
    def _calculate_city_effects(self) -> CityEffects:
        """
        Calculate the total city effects (base + given by buildings).
        """
        city_effects: CityEffects = self._get_base_effects()
        
        for building in self.buildings.buildings:
            city_effects.troop_training = city_effects.troop_training + BUILDINGS[building]["effect_bonuses"].troop_training
            city_effects.population_growth = city_effects.population_growth + BUILDINGS[building]["effect_bonuses"].population_growth
            city_effects.intelligence = city_effects.intelligence + BUILDINGS[building]["effect_bonuses"].intelligence
        
        return city_effects
    
    
    def __post_init__(self) -> None:
        self.resource_potentials = self._get_rss_potentials()
        self.geo_features = self._get_geo_features()
        self.city_effects = self._calculate_city_effects()
        self.base_production = self._calculate_base_production()
        self.productivity_bonuses = self._calculate_productivity_bonuses()
        self.total_production = self._calculate_total_production()
        self.maintenance_costs = self._calculate_maintenance_costs()
        self.balance = self._calculate_balance()
    
    
    #* Display results
    def _display_city_information(self) -> None:
        
        print(f"Campaign: {self.campaign}")
        print(f"City: {self.name}")
    
    def _display_city_buildings(self) -> None:
        
        print(f"City buildings")
        print(f"==============")
        
        for building, qty in self.buildings.buildings.items():
            print(f"  - {building.replace("_", " ").capitalize()} ({qty})")
    
    def _display_city_production(self) -> None:
        col_headers: list[str] = [
            "Resource",
            "Rss. pot.",
            "Base prod.",
            "Prod. bonus",
            "Total prod.",
            "Maintenance",
            "Balance",
        ]
        table_header: str = "| " + " | ".join(col_headers) + " |"
        horizontal_rule: str = "-" * len(table_header)
        
        #* Table header row
        print(horizontal_rule)
        print(table_header)
        print(horizontal_rule)
        
        #* Food row
        rss_potential: int = self.resource_potentials.food
        base_production: int = self.base_production.food
        prod_bonus: int = self.productivity_bonuses.food
        total_production: int = self.total_production.food
        maintenance_cost: int = self.maintenance_costs.food * (-1 if self.maintenance_costs.food > 0 else 1)
        balance: int = self.balance.food
        print(
            f"| Food{" " * 4} "
            f"| {" " * (len(col_headers[1]) - len(str(rss_potential)))}{rss_potential} "
            f"| {" " * (len(col_headers[2]) - len(str(base_production)))}{base_production} "
            f"| {" " * (len(col_headers[3]) - len(str(prod_bonus)))}{prod_bonus} "
            f"| {" " * (len(col_headers[4]) - len(str(total_production)))}{total_production} "
            f"| {" " * (len(col_headers[5]) - len(str(maintenance_cost)))}{maintenance_cost} "
            f"| {" " * (len(col_headers[6]) - len(str(balance)))}{balance} "
            f"|"
        )
        
        #* Ore row
        rss_potential: int = self.resource_potentials.ore
        base_production: int = self.base_production.ore
        prod_bonus: int = self.productivity_bonuses.ore
        total_production: int = self.total_production.ore
        maintenance_cost: int = self.maintenance_costs.ore * (-1 if self.maintenance_costs.food > 0 else 1)
        balance: int = self.balance.ore
        print(
            f"| Ore{" " * 5} "
            f"| {" " * (len(col_headers[1]) - len(str(rss_potential)))}{rss_potential} "
            f"| {" " * (len(col_headers[2]) - len(str(base_production)))}{base_production} "
            f"| {" " * (len(col_headers[3]) - len(str(prod_bonus)))}{prod_bonus} "
            f"| {" " * (len(col_headers[4]) - len(str(total_production)))}{total_production} "
            f"| {" " * (len(col_headers[5]) - len(str(maintenance_cost)))}{maintenance_cost} "
            f"| {" " * (len(col_headers[6]) - len(str(balance)))}{balance} "
            f"|"
        )
        
        #* Wood row
        rss_potential: int = self.resource_potentials.wood
        base_production: int = self.base_production.wood
        prod_bonus: int = self.productivity_bonuses.wood
        total_production: int = self.total_production.wood
        maintenance_cost: int = self.maintenance_costs.wood * (-1 if self.maintenance_costs.food > 0 else 1)
        balance: int = self.balance.wood
        print(
            f"| Wood{" " * 4} "
            f"| {" " * (len(col_headers[1]) - len(str(rss_potential)))}{rss_potential} "
            f"| {" " * (len(col_headers[2]) - len(str(base_production)))}{base_production} "
            f"| {" " * (len(col_headers[3]) - len(str(prod_bonus)))}{prod_bonus} "
            f"| {" " * (len(col_headers[4]) - len(str(total_production)))}{total_production} "
            f"| {" " * (len(col_headers[5]) - len(str(maintenance_cost)))}{maintenance_cost} "
            f"| {" " * (len(col_headers[6]) - len(str(balance)))}{balance} "
            f"|"
        )
        
        #* Bottom horizontal row
        print(horizontal_rule)
    
    def _display_city_effects(self) -> None:
        col_headers: list[str] = [
            "Effect",
            "Total",
        ]
        
        rows: list[str] = [
            "Troop training",
            "Population growth",
            "Intelligence",
        ]
        
        row_lengths: list[int] = [len(row) for row in rows]
        
        table_header: str = f"| {col_headers[0]}{" " * (max(row_lengths) - len(col_headers[0]) + 1)}| {col_headers[1]} |"
        horizontal_rule: str = "-" * len(table_header)
        
        #* Table header row
        print(horizontal_rule)
        print(table_header)
        print(horizontal_rule)
        
        #* Troop training row
        print(
            f"| Troop training{" " * 4}"
            f"| {" " * (len(col_headers[1]) - len(str(self.city_effects.troop_training)))}{self.city_effects.troop_training} "
            f"|"
        )
        
        #* Population growth row
        print(
            f"| Population growth "
            f"| {' ' * (len(col_headers[1]) - len(str(self.city_effects.population_growth)))}{self.city_effects.population_growth} "
            f"|"
        )
        
        #* Intelligence row
        print(
            f"| Intelligence{" " * 6}"
            f"| {' ' * (len(col_headers[1]) - len(str(self.city_effects.intelligence)))}{self.city_effects.intelligence} "
            f"|"
        )
        
        #* Bottom horizontal rule
        print(horizontal_rule)
    
    def display_results(
            self,
            include_city_information: bool = False,
            include_city_buildings: bool = True,
            include_city_production: bool = True,
            include_city_effects: bool = False,
        ) -> None:
        print()
        
        if include_city_information:
            self._display_city_information()
            print()
        
        if include_city_buildings:
            self._display_city_buildings()
            print()
        
        if include_city_production:
            self._display_city_production()
            print()
        
        if include_city_effects:
            self._display_city_effects()
            print()
