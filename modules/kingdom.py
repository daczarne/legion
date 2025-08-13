from dataclasses import dataclass, field

from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .city import City
from .resources import ResourceCollection
from .scenario import CityDict


@dataclass
class Kingdom:
    cities: list[City]
    
    kingdom_total_production: ResourceCollection = field(init = False)
    kingdom_total_storage: ResourceCollection = field(init = False)
    
    def _calculate_total_production(self) -> ResourceCollection:
        total_production: ResourceCollection = ResourceCollection()
        
        for city in self.cities:
            total_production.food = total_production.food + city.balance.food
            total_production.ore = total_production.ore + city.balance.ore
            total_production.wood = total_production.wood + city.balance.wood
        
        return total_production
    
    def _calculate_total_storage(self) -> ResourceCollection:
        total_storage: ResourceCollection = ResourceCollection()
        
        for city in self.cities:
            total_storage.food = total_storage.food + city.total_storage.food
            total_storage.ore = total_storage.ore + city.total_storage.ore
            total_storage.wood = total_storage.wood + city.total_storage.wood
        
        return total_storage
    
    @classmethod
    def from_list(
        cls,
        data: list[CityDict],
    ) -> "Kingdom":
        cities: list[City] = [City(**city) for city in data]
        return cls(cities)
    
    def __post_init__(self) -> None:
        self.kingdom_total_production = self._calculate_total_production()
        self.kingdom_total_storage = self._calculate_total_storage()
    
    def _build_kingdom_information(self) -> Text:
        city_information: Text = Text(
            text = f" {self.cities[0].campaign} ",
            style = "bold black on white",
            justify = "center",
        )
        return city_information
    
    def _build_kingdom_production_table(self) -> Table:
        # table_style: Style = Style(color = self.configuration.get("production", {}).get("color", "#228b22"))
        table_style: Style = Style(color = "#228b22")
        table: Table = Table(
            title = Text(text = "Production", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
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
        
        table.add_section()
        
        table.add_row(
            f"Total ({len(self.cities)})",
            f"{self.kingdom_total_production.food:_}",
            f"{self.kingdom_total_production.ore:_}",
            f"{self.kingdom_total_production.wood:_}",
            style = table_style + Style(bold = True),
        )
        
        return table
    
    def _build_kingdom_storage_table(self) -> Table:
        table_style: Style = Style(color = "purple")
        table: Table = Table(
            title = Text(text = "Storage", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "City", header_style = "bold")
        table.add_column(header = "Food", header_style = "bold", justify = "right")
        table.add_column(header = "Ore", header_style = "bold", justify = "right")
        table.add_column(header = "Wood", header_style = "bold", justify = "right")
        
        for city in self.cities:
            table.add_row(
                f"{city.name}",
                f"{city.total_storage.food}",
                f"{city.total_storage.ore}",
                f"{city.total_storage.wood}",
            )
        
        table.add_section()
        
        table.add_row(
            f"Total ({len(self.cities)})",
            f"{self.kingdom_total_storage.food:_}",
            f"{self.kingdom_total_storage.ore:_}",
            f"{self.kingdom_total_storage.wood:_}",
            style = table_style + Style(bold = True),
        )
        
        return table
    
    def _build_kingdom_display(self) -> Panel:
        layout: Layout = Layout()
        layout.split(
            Layout(
                name = "header",
                size = 2,
                # ratio = 0,
                # visible = include_city,
            ),
            Layout(
                name = "main",
                # size = main_height,
                # ratio = 0,
                # visible = any([
                #     include_buildings,
                #     include_effects,
                #     include_production,
                #     include_storage,
                #     include_defenses,
                # ]),
            ),
        )
        
        layout["header"].update(
            renderable = Align(renderable = self._build_kingdom_information(), align = "center"),
        )
        
        layout["main"].split(
            Layout(
                name = "production",
                # size = production_height,
                # ratio = 0,
                # visible = include_production,
            ),
            Layout(
                name = "storage_capacity",
                # size = storage_height,
                # ratio = 0,
                # visible = include_storage,
            ),
        )
        
        layout["production"].update(
            renderable = Align(renderable = self._build_kingdom_production_table(), align = "center"),
        )
        
        layout["storage_capacity"].update(
            renderable = Align(renderable = self._build_kingdom_storage_table(), align = "center"),
        )
        
        return Panel(
            renderable = layout,
            # width = total_layout_width,
            # height = total_layout_height,
        )
    
    def display_kingdom_results(self) -> None:
        console: Console = Console()
        console.print(self._build_kingdom_display())
