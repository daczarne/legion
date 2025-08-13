from rich import box
from rich.table import Table
from rich.text import Text

from .resources import ResourceCollection
from .city import City


class Kingdom:
    def __init__(
            self,
            cities: list[City],
        ) -> None:
        self.cities: list[City] = cities
    
    def _calculate_totals(self) -> ResourceCollection:
        kingdom_totals: ResourceCollection = ResourceCollection()
        
        for city in self.cities:
            kingdom_totals.food = kingdom_totals.food + city.balance.food
            kingdom_totals.ore = kingdom_totals.ore + city.balance.ore
            kingdom_totals.wood = kingdom_totals.wood + city.balance.wood
        
        return kingdom_totals
    
    def _build_kingdom_table(self) -> Table:
        table: Table = Table(
            title = Text(text = "Cities"),
            box = box.HEAVY
        )
        
        table.add_column(header = "City", header_style = "bold")
        table.add_column(header = "Food", header_style = "bold")
        table.add_column(header = "Ore", header_style = "bold")
        table.add_column(header = "Wood", header_style = "bold")
        
        for city in self.cities:
            table.add_row(
                f"{city.name}",
                f"{city.balance.food}",
                f"{city.balance.ore}",
                f"{city.balance.wood}",
            )
        return table
