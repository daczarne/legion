import yaml
from dataclasses import dataclass, field
from typing import ClassVar, TypedDict, Literal

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.table import Table
from rich.text import Text

from .building import BuildingsCount, BUILDINGS
from .effects import EffectBonuses, EffectBonusesData
from .geo_features import GeoFeatures, GeoFeaturesData
from .resources import ResourceCollection, ResourceCollectionData


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
    base_production: ResourceCollection = field(init = False)
    productivity_bonuses: ResourceCollection = field(init = False)
    total_production: ResourceCollection = field(init = False)
    maintenance_costs: ResourceCollection = field(init = False)
    balance: ResourceCollection = field(init = False)
    
    # Class variables
    MAX_WORKERS: ClassVar[int] = 18
    POSSIBLE_SETTLEMENT_HALLS: ClassVar[set[str]] = {"village_hall", "town_hall", "city_hall"}
    MAX_BUILDINGS_PER_SETTLEMENT: ClassVar[dict[str, int]] = {
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
    
    def _get_base_effects(self) -> EffectBonuses:
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
        halls: dict[str, int] = {k: v for k, v in self.buildings.items() if k in self.POSSIBLE_SETTLEMENT_HALLS}
        
        if not halls:
            raise ValueError(f"Settlement must include a hall (village, town, or city)")
        
        if len(halls) > 1:
            raise ValueError(f"Too many halls for this city")
        
        if list(halls.values())[0] != 1:
            raise ValueError(f"Too many halls for this city")
    
    def _get_settlement_hall(self) -> str:
        halls: dict[str, int] = {k: v for k, v in self.buildings.items() if k in self.POSSIBLE_SETTLEMENT_HALLS}
        return list(halls.keys())[0]
    
    def _validate_number_of_buildings(self) -> None:
        number_of_declared_buildings: int = sum(self.buildings.values())
        max_number_of_buildings_in_settlement: int = self.MAX_BUILDINGS_PER_SETTLEMENT[self._get_settlement_hall()]
        
        if number_of_declared_buildings > max_number_of_buildings_in_settlement + 1:
            raise ValueError(
                f"Too many buildings for this settlement: "
                f"{number_of_declared_buildings} provided, "
                f"max of {max_number_of_buildings_in_settlement + 1} possible ({max_number_of_buildings_in_settlement} + hall)"
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
    
    #* Production calculations
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
    
    
    #* Effects calculations
    def _calculate_city_effects(self) -> EffectBonuses:
        """
        Calculate the total city effects (base + given by buildings).
        """
        city_effects: EffectBonuses = self._get_base_effects()
        
        for building in self.buildings:
            city_effects.troop_training = city_effects.troop_training + BUILDINGS[building].effect_bonuses.troop_training
            city_effects.population_growth = city_effects.population_growth + BUILDINGS[building].effect_bonuses.population_growth
            city_effects.intelligence = city_effects.intelligence + BUILDINGS[building].effect_bonuses.intelligence
        
        return city_effects
    
    
    def __post_init__(self) -> None:
        self._validate_unknown_buildings()
        self._validate_halls()
        self._validate_number_of_buildings()
        self.resource_potentials = self._get_rss_potentials()
        self.geo_features = self._get_geo_features()
        self.city_effects = self._calculate_city_effects()
        self.base_production = self._calculate_base_production()
        self.productivity_bonuses = self._calculate_productivity_bonuses()
        self.total_production = self._calculate_total_production()
        self.maintenance_costs = self._calculate_maintenance_costs()
        self.balance = self._calculate_balance()
    
    
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
            city_buildings_text.append(text = f"  - {building.replace("_", " ").capitalize()} ({qty})\n")
        
        city_buildings_table: Table = Table(title = "Buildings", show_header = False, box = None, padding=(0, 1))
        city_buildings_table.add_column()
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
        table.add_column(header = "Total", header_style = "bold", justify = "right")
        
        table.add_row("Troop training", f"{str(self.city_effects.troop_training)}")
        table.add_row("Population growth", f"{str(self.city_effects.population_growth)}")
        table.add_row("Intelligence", f"{str(self.city_effects.intelligence)}")
        
        return table
    
    def display_results(self) -> None:
        console: Console = Console()
        layout: Layout = Layout()
        
        layout.split(
            Layout(name = "header", size = 2),
            Layout(name = "main", ratio = 1),
        )
        
        layout["main"].split(
            Layout(name = "top", size = 8),
            Layout(name = "bottom", size = 8),
        )
        
        layout["top"].split_row(
            Layout(
                renderable = Align(renderable = self._build_city_buildings_list(), align = "center"),
                name = "left"
            ),
            Layout(
                renderable = Align(renderable = self._build_city_effects_table(), align = "center"),
                name = "right"
            )
        )
        layout["header"].update(renderable = Align(renderable = self._build_city_information(), align = "center"))
        layout["bottom"].update(renderable = self._build_city_production_table())
        
        panel: Panel = Panel(renderable = layout, width = 92, height = 20)
        console.print(panel)
