from multiprocessing import Value
import yaml
from dataclasses import dataclass, field
from typing import TypedDict, Literal, ClassVar

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .building import BuildingsCount, BUILDINGS
from .effects import EffectBonusesData, EffectBonuses
from .geo_features import GeoFeaturesData, GeoFeatures
from .resources import ResourceCollectionData, ResourceCollection


# * *********** * #
# * CITIES DATA * #
# * *********** * #

class CityData(TypedDict):
    name: str
    campaign: str
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

@dataclass
class City:
    campaign: str
    name: str
    buildings: BuildingsCount
    
    # Post init attrs
    resource_potentials: ResourceCollection = field(init = False)
    geo_features: GeoFeatures = field(init = False)
    
    city_effects: EffectBonuses = field(init = False)
    building_effects: EffectBonuses = field(init = False)
    worker_effects: EffectBonuses = field(init = False)
    total_effects: EffectBonuses = field(init = False)
    
    base_production: ResourceCollection = field(init = False)
    productivity_bonuses: ResourceCollection = field(init = False)
    total_production: ResourceCollection = field(init = False)
    maintenance_costs: ResourceCollection = field(init = False)
    balance: ResourceCollection = field(init = False)
    
    city_storage: ResourceCollection = field(init = False)
    buildings_storage: ResourceCollection = field(init = False)
    warehouse_storage: ResourceCollection = field(init = False)
    supply_dump_storage: ResourceCollection = field(init = False)
    total_storage: ResourceCollection = field(init = False)
    
    garrison: str = field(init = False)
    squadrons: int = field(init = False)
    squadron_size: str = field(init = False)
    
    
    # Class variables
    MAX_WORKERS: ClassVar[int] = 18
    POSSIBLE_CITY_HALLS: ClassVar[set[str]] = {"village_hall", "town_hall", "city_hall"}
    MAX_BUILDINGS_PER_CITY: ClassVar[dict[str, int]] = {
        "village_hall": 4,
        "town_hall": 6,
        "city_hall": 8,
    }
    
    
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
    
    #* Validate city buildings
    def _validate_halls(self) -> None:
        halls: dict[str, int] = {k: v for k, v in self.buildings.items() if k in self.POSSIBLE_CITY_HALLS}
        
        if not halls:
            raise ValueError(f"City must include a hall (village, town, or city)")
        
        if len(halls) > 1:
            raise ValueError(f"Too many halls for this city")
        
        if list(halls.values())[0] != 1:
            raise ValueError(f"Too many halls for this city")
    
    def _get_hall(self) -> str:
        halls: dict[str, int] = {k: v for k, v in self.buildings.items() if k in self.POSSIBLE_CITY_HALLS}
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
    
    # Validations need to include the following situations.
    # 
    #~ Rss buildings are allowed.
    # This is because a city with, for example, rss potential of 0 for food, cannot create food-producing buildings
    # (like farms, vineyards, or fishing villages), even if it has a lake (the lake is, sadly, a waisted building spot
    # in this case).
    # 
    #~ Guilds.
    # Building guilds requires the production building itself. For example, if there are no farms, there can be no
    # farmers' guild. Similarly, if there are no lumber mills, there can be no carpenters guild, and so on.
    #
    # Additionally, there are other dependencies between buildings. For example, a city needs:
    #   farm => stables
    #   lumber mill => fletcher
    #   mine (not outcrop or mountain) => blacksmith
    #   fort => quartermaster
    #   training grounds => other training facilities (like gladiator school, imperial residence, bordello)
    #
    # But, all dependencies can be bypassed by building the required building (e.g. a farm), then building the
    # dependent building (e.g. stables), and then deleting the required building and using that spot to build something
    # else. Some of these dependencies makes sense to validate them because the dependent building makes no sense
    # without the dependency building. For example, no sense in having a city with a farmers' guild, if the city has no
    # farms.
    #
    #~ Blocked building spots.
    # Lastly, not all cities can accept all potential building scenarios. For example, a city with a lake and enough
    # food potential for a fishing village, "cannot" build 6 mines. Since there are only a maximum of 18 workers per
    # city, this configuration (1 fishing village + 6 mines) would mean that at least one of the buildings is not
    # staffed (potentially, even empty). The validation should warn against this scenario.
    
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
            
            base_production.food = base_production.food + base_production_food
            base_production.ore = base_production.ore + base_production_ore
            base_production.wood = base_production.wood + base_production_wood
        
        return base_production
    
    def _calculate_productivity_bonuses(self) -> ResourceCollection:
        """
        Based on the buildings found in the city, it calculates the productivity bonuses for each resource.
        """
        productivity_bonuses: ResourceCollection = ResourceCollection()
        
        for building in self.buildings:
            productivity_bonuses.food = productivity_bonuses.food + BUILDINGS[building].productivity_bonuses.food
            productivity_bonuses.ore = productivity_bonuses.ore + BUILDINGS[building].productivity_bonuses.ore
            productivity_bonuses.wood = productivity_bonuses.wood + BUILDINGS[building].productivity_bonuses.wood
        
        return productivity_bonuses
    
    def _calculate_total_production(self) -> ResourceCollection:
        """
        Given the base production and the productivity bonuses of a city, it calculates the total production.
        """
        from math import floor
        
        total_production: ResourceCollection = ResourceCollection()
        
        total_production.food = int(floor(self.base_production.food * (1 + self.productivity_bonuses.food / 100)))
        total_production.ore = int(floor(self.base_production.ore * (1 + self.productivity_bonuses.ore / 100)))
        total_production.wood = int(floor(self.base_production.wood * (1 + self.productivity_bonuses.wood / 100)))
        
        return total_production
    
    def _calculate_maintenance_costs(self) -> ResourceCollection:
        """
        Based on the buildings found in the city, it calculates the maintenance costs for each resource.
        """
        maintenance_costs: ResourceCollection = ResourceCollection()
        
        for building in self.buildings:
            maintenance_costs.food = maintenance_costs.food + BUILDINGS[building].maintenance_cost.food
            maintenance_costs.ore = maintenance_costs.ore + BUILDINGS[building].maintenance_cost.ore
            maintenance_costs.wood = maintenance_costs.wood + BUILDINGS[building].maintenance_cost.wood
        
        return maintenance_costs
    
    def _calculate_balance(self) -> ResourceCollection:
        """
        Calculate the balance for each rss. The balance is the difference between the total production and the
        maintenance costs.
        """
        balance: ResourceCollection = ResourceCollection()
        
        balance.food = self.total_production.food - self.maintenance_costs.food
        balance.ore = self.total_production.ore - self.maintenance_costs.ore
        balance.wood = self.total_production.wood - self.maintenance_costs.wood
        
        return balance
    
    
    #* Effects bonuses
    def _calculate_building_effects(self) -> EffectBonuses:
        """
        Calculates the base effects produced by buildings. These do not include worker level effects.
        """
        building_effects: EffectBonuses = EffectBonuses()
        
        for building in self.buildings:
            building_effects.troop_training = building_effects.troop_training + BUILDINGS[building].effect_bonuses.troop_training
            building_effects.population_growth = building_effects.population_growth + BUILDINGS[building].effect_bonuses.population_growth
            building_effects.intelligence = building_effects.intelligence + BUILDINGS[building].effect_bonuses.intelligence
        
        return building_effects
    
    def _calculate_worker_effects(self) -> EffectBonuses:
        """
        Calculates the effects produced by building workers.
        """
        worker_effects: EffectBonuses = EffectBonuses()
        
        for building in self.buildings:
            worker_effects.troop_training = worker_effects.troop_training + BUILDINGS[building].effect_bonuses_per_worker.troop_training * BUILDINGS[building].max_workers
            worker_effects.population_growth = worker_effects.population_growth + BUILDINGS[building].effect_bonuses_per_worker.population_growth * BUILDINGS[building].max_workers
            worker_effects.intelligence = worker_effects.intelligence + BUILDINGS[building].effect_bonuses_per_worker.intelligence * BUILDINGS[building].max_workers
        
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
    
    
    #* Storage capacity
    def _calculate_city_storage(self) -> ResourceCollection:
        return BUILDINGS[self._get_hall()].storage_capacity
    
    def _calculate_buildings_storage(self) -> ResourceCollection:
        buildings_storage: ResourceCollection = ResourceCollection()
        
        for building, qty in self.buildings.items():
            if building not in [*self.POSSIBLE_CITY_HALLS, "warehouse", "supply_dump"]:
                buildings_storage.food = buildings_storage.food + BUILDINGS[building].storage_capacity.food * qty
                buildings_storage.ore = buildings_storage.ore + BUILDINGS[building].storage_capacity.ore * qty
                buildings_storage.wood = buildings_storage.wood + BUILDINGS[building].storage_capacity.wood * qty
        
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
    
    
    def __post_init__(self) -> None:
        self.resource_potentials = self._get_rss_potentials()
        self.geo_features = self._get_geo_features()
        
        #* Validate city
        self._validate_unknown_buildings()
        self._validate_halls()
        self._validate_number_of_buildings()
        
        #* Effects
        self.city_effects = self._get_city_effects()
        self.building_effects = self._calculate_building_effects()
        self.worker_effects = self._calculate_worker_effects()
        self.total_effects = self._calculate_total_effects()
        
        #* Production
        self.base_production = self._calculate_base_production()
        self.productivity_bonuses = self._calculate_productivity_bonuses()
        self.total_production = self._calculate_total_production()
        self.maintenance_costs = self._calculate_maintenance_costs()
        self.balance = self._calculate_balance()
        
        #* Storage
        self.city_storage = self._calculate_city_storage()
        self.buildings_storage = self._calculate_buildings_storage()
        self.warehouse_storage = self._calculate_warehouse_storage()
        self.supply_dump_storage = self._calculate_supply_dump_storage()
        self.total_storage = self._calculate_total_storage_capacity()
        
        #* Defenses
        self.garrison = self._get_garrison()
        self.squadrons = self._calculate_garrison_size()
        self.squadron_size = self._calculate_squadron_size()
    
    
    #* Display results
    def _build_city_information(self) -> Text:
        city_information: Text = Text(
            text = f" {self.campaign} --- {self.name} ",
            style = "bold black on white",
            justify = "center",
        )
        return city_information
    
    def _build_city_buildings_list(self) -> Table:
        city_buildings_text: Text = Text()
        
        for building, qty in self.buildings.items():
            city_buildings_text.append(text = f"  - {BUILDINGS[building].name} ({qty})\n")
        
        city_buildings_table: Table = Table(title = "Buildings", show_header = False, box = None, padding = (0, 1))
        city_buildings_table.add_column()
        city_buildings_table.add_row()
        city_buildings_table.add_row(city_buildings_text)
        
        return city_buildings_table
    
    def _build_city_production_table(self) -> Table:
        table: Table = Table(title = "Production")
        
        table.add_column(header = "Resource", header_style = "bold", justify = "left")
        table.add_column(header = "Rss. pot.", header_style = "bold", justify = "right")
        table.add_column(header = "Base prod.", header_style = "bold", justify = "right")
        table.add_column(header = "Prod. bonus", header_style = "bold", justify = "right")
        table.add_column(header = "Total prod", header_style = "bold", justify = "right")
        table.add_column(header = "Maintenance", header_style = "bold", justify = "right")
        table.add_column(header = "Balance", header_style = "bold", justify = "right")
        
        table.add_row(
            f"Food",
            f"{self.resource_potentials.food}",
            f"{self.base_production.food}",
            f"{self.productivity_bonuses.food}",
            f"{self.total_production.food}",
            f"{-1 * self.maintenance_costs.food}",
            f"{self.balance.food}",
        )
        table.add_row(
            f"Ore",
            f"{self.resource_potentials.ore}",
            f"{self.base_production.ore}",
            f"{self.productivity_bonuses.ore}",
            f"{self.total_production.ore}",
            f"{-1 * self.maintenance_costs.ore}",
            f"{self.balance.ore}",
        )
        table.add_row(
            f"Wood",
            f"{self.resource_potentials.wood}",
            f"{self.base_production.wood}",
            f"{self.productivity_bonuses.wood}",
            f"{self.total_production.wood}",
            f"{-1 * self.maintenance_costs.wood}",
            f"{self.balance.wood}",
        )
        
        return table
    
    def _build_city_effects_table(self) -> Table:
        table: Table = Table(title = "Effects")
        
        table.add_column(header = "Effect", header_style = "bold", justify = "center")
        table.add_column(header = "City", header_style = "bold", justify = "right")
        table.add_column(header = "Buildings", header_style = "bold", justify = "right")
        table.add_column(header = "Workers", header_style = "bold", justify = "right")
        table.add_column(header = "Total", header_style = "bold", justify = "right")
        
        table.add_row(
            "Troop training",
            f"{self.city_effects.troop_training}",
            f"{self.building_effects.troop_training}",
            f"{self.worker_effects.troop_training}",
            f"{self.total_effects.troop_training}",
        )
        table.add_row(
            "Pop. growth",
            f"{self.city_effects.population_growth}",
            f"{self.building_effects.population_growth}",
            f"{self.worker_effects.population_growth}",
            f"{self.total_effects.population_growth}",
        )
        table.add_row(
            "Intelligence",
            f"{self.city_effects.intelligence}",
            f"{self.building_effects.intelligence}",
            f"{self.worker_effects.intelligence}",
            f"{self.total_effects.intelligence}",
        )
        
        return table
    
    def _build_city_storage_table(self) -> Table:
        table: Table = Table(title = "Storage capacity")
        
        table.add_column(header = "Resource", header_style = "bold", justify = "left")
        table.add_column(header = "City", header_style = "bold", justify = "right")
        table.add_column(header = "Buildings", header_style = "bold", justify = "right")
        table.add_column(header = "Warehouse", header_style = "bold", justify = "right")
        table.add_column(header = "Supply dump", header_style = "bold", justify = "right")
        table.add_column(header = "Total", header_style = "bold", justify = "right")
        
        table.add_row(
            "Food",
            f"{self.city_storage.food}",
            f"{self.buildings_storage.food}",
            f"{self.warehouse_storage.food}",
            f"{self.supply_dump_storage.food}",
            f"{self.total_storage.food}",
        )
        table.add_row(
            "Ore",
            f"{self.city_storage.ore}",
            f"{self.buildings_storage.ore}",
            f"{self.warehouse_storage.ore}",
            f"{self.supply_dump_storage.ore}",
            f"{self.total_storage.ore}",
        )
        table.add_row(
            "Wood",
            f"{self.city_storage.wood}",
            f"{self.buildings_storage.wood}",
            f"{self.warehouse_storage.wood}",
            f"{self.supply_dump_storage.wood}",
            f"{self.total_storage.wood}",
        )
        
        return table
    
    def _build_defenses_table(self) -> Table:
        table: Table = Table(title = "Defenses")
        
        table.add_column(header = "Garrison", header_style = "bold", justify = "center")
        table.add_column(header = "Squadrons", header_style = "bold", justify = "center")
        table.add_column(header = "Squadron size", header_style = "bold", justify = "center")
        
        table.add_row(
            f"{self.garrison}",
            f"{self.squadrons}",
            f"{self.squadron_size}",
        )
        
        return table
    
    def _build_results_display(self) -> Panel:
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
        layout: Layout = Layout()
        
        header_height: int = 2
        buildings_and_effects_height: int = 10
        production_height: int = 8
        storage_height: int = 8
        defenses_height: int = 9
        main_height: int = buildings_and_effects_height + production_height + storage_height + defenses_height
        
        total_layout_height: int = header_height + main_height
        total_layout_width: int = 98
        
        layout.split(
            Layout(name = "header", size = header_height),
            Layout(name = "main", size = main_height),
        )
        
        layout["header"].update(
            renderable = Align(renderable = self._build_city_information(), align = "center"),
        )
        
        layout["main"].split(
            Layout(name = "buildings_and_effects", size = buildings_and_effects_height),
            Layout(name = "production", size = production_height),
            Layout(name = "storage_capacity", size = storage_height),
            Layout(name = "defenses", size = defenses_height),
        )
        
        layout["buildings_and_effects"].split_row(
            Layout(name = "buildings", ratio = 1),
            Layout(name = "effects", ratio = 2),
        )
        
        layout["buildings"].update(
            renderable = Layout(renderable = Align(renderable = self._build_city_buildings_list(), align = "center")),
        )
        
        layout["effects"].update(
            renderable = Layout(renderable = Align(renderable = self._build_city_effects_table(), align = "center")),
        )
        
        layout["production"].update(
            renderable = Layout(renderable = Align(renderable = self._build_city_production_table(), align = "center")),
        )
        
        layout["storage_capacity"].update(
            renderable = Layout(renderable = Align(renderable = self._build_city_storage_table(), align = "center")),
        )
        
        layout["defenses"].update(
            renderable = Layout(renderable = Align(renderable = self._build_defenses_table(), align = "center")),
        )
        
        return Panel(renderable = layout, width = total_layout_width, height = total_layout_height)
    
    def display_results(self) -> None:
        console: Console = Console()
        console.print(self._build_results_display())
