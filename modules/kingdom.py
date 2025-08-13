from dataclasses import dataclass, field

from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

from .resources import ResourceCollection
from .city import City
from .scenario import CityDict


@dataclass
class Kingdom:
    cities: list[City]
    
    kingdom_totals: ResourceCollection = field(init = False)
    
    def _calculate_totals(self) -> ResourceCollection:
        kingdom_totals: ResourceCollection = ResourceCollection()
        
        for city in self.cities:
            kingdom_totals.food = kingdom_totals.food + city.balance.food
            kingdom_totals.ore = kingdom_totals.ore + city.balance.ore
            kingdom_totals.wood = kingdom_totals.wood + city.balance.wood
        
        return kingdom_totals
    
    @classmethod
    def from_list(
        cls,
        data: list[CityDict],
    ) -> "Kingdom":
        cities: list[City] = [City(**city) for city in data]
        return cls(cities)
    
    def __post_init__(self) -> None:
        self.kingdom_totals = self._calculate_totals()
    
    def _build_kingdom_production_table(self) -> Table:
        table: Table = Table(
            title = Text(text = "Production"),
            box = box.HEAVY
        )
        
        table.add_column(header = "City", header_style = "bold")
        table.add_column(header = "Food", header_style = "bold", justify = "right")
        table.add_column(header = "Ore", header_style = "bold", justify = "right")
        table.add_column(header = "Wood", header_style = "bold", justify = "right")
        
        for city in self.cities:
            table.add_row(
                f"{city.name}",
                f"{city.balance.food}",
                f"{city.balance.ore}",
                f"{city.balance.wood}",
            )
        
        table.add_row(
            f"Total",
            f"{self.kingdom_totals.food:_}",
            f"{self.kingdom_totals.ore:_}",
            f"{self.kingdom_totals.wood:_}",
        )
        
        return table
    
    def display_kingdom_results(self) -> None:
        console: Console = Console()
        console.print(self._build_kingdom_production_table())
