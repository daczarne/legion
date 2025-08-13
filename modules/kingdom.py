from dataclasses import dataclass, field
from typing import ClassVar

from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .city import CITIES, City, CityFocus
from .resources import ResourceCollection
from .scenario import CityDict


@dataclass
class Kingdom:
    cities: list[City]
    sort_order: list[str | None] | None = field(default = None)
    
    
    # Post init values
    number_of_cities_in_campaign: int = field(init = False)
    kingdom_total_production: ResourceCollection = field(init = False)
    kingdom_total_storage: ResourceCollection = field(init = False)
    
    
    # The player gets a 300 storage or each rss which does not depend on any city or buildings.
    BASE_KINGDOM_STORAGE: ClassVar[int] = 300
    
    
    @staticmethod
    def sort_cities_by_production_type(
        cities: list[City], 
        order: list[str | None] | None = None,
    ) -> list[City]:
        """
        Sort cities by main resource according to user-defined order. Within each resource type, sort alphabetically
        by city name. If the user does not supply an order, the order will be FOOD -> ORE -> WOOD -> NONE.
        """
        if order is None:
            order = ["food", "ore", "wood", None]
        
        # Validate order contains only allowed strings or None
        allowed: set[str | None] = {"food", "ore", "wood", None}
        if any(item not in allowed for item in order):
            raise ValueError(f"Invalid order: {order}. Allowed: {allowed}")
        
        # Map resource name to CityFocus enum for sorting
        resource_name_to_enum: dict[str | None, CityFocus] = {
            "food": CityFocus.FOOD,
            "ore": CityFocus.ORE,
            "wood": CityFocus.WOOD,
            None: CityFocus.NONE,
        }
        
        enum_order: list[CityFocus] = [resource_name_to_enum[r] for r in order]
        
        # Sort function: first by enum order, then alphabetically by name
        def sort_key(city: City) -> tuple[int, str]:
            try:
                primary_index: int = enum_order.index(city.focus)
            except ValueError:
                primary_index: int = len(enum_order) # push unknown to the end
            return (primary_index, city.name.lower())
        
        return sorted(cities, key = sort_key)
    
    def sort_cities_by_production_type_inplace(
        self,
        order: list[str | None] | None = None,
    ) -> None:
        """
        Replace self.cities with the sorted list according to the provided order.
        """
        self.cities = Kingdom.sort_cities_by_production_type(cities = self.cities, order = order)
    
    
    @classmethod
    def from_list(
        cls,
        data: list[CityDict],
        sort_order: list[str | None] | None = None,
    ) -> "Kingdom":
        cities: list[City] = [City(**city) for city in data]
        return cls(cities, sort_order)
    
    
    def _calculate_total_production(self) -> ResourceCollection:
        total_production: ResourceCollection = ResourceCollection()
        
        for city in self.cities:
            total_production.food = total_production.food + city.balance.food
            total_production.ore = total_production.ore + city.balance.ore
            total_production.wood = total_production.wood + city.balance.wood
        
        return total_production
    
    def _calculate_total_storage(self) -> ResourceCollection:
        total_storage: ResourceCollection = ResourceCollection(
            food = self.BASE_KINGDOM_STORAGE,
            ore = self.BASE_KINGDOM_STORAGE,
            wood = self.BASE_KINGDOM_STORAGE,
        )
        
        for city in self.cities:
            total_storage.food = total_storage.food + city.total_storage.food
            total_storage.ore = total_storage.ore + city.total_storage.ore
            total_storage.wood = total_storage.wood + city.total_storage.wood
        
        return total_storage
    
    def _get_number_of_cities_in_campaign(self) -> int:
        number_of_cities_in_campaign: int = 0
        
        for city in CITIES:
            if city.get("campaign") == self.cities[0].campaign:
                number_of_cities_in_campaign += 1
        
        return number_of_cities_in_campaign
    
    
    def __post_init__(self) -> None:
        self.sort_cities_by_production_type_inplace(self.sort_order)
        self.number_of_cities_in_campaign = self._get_number_of_cities_in_campaign()
        self.kingdom_total_production = self._calculate_total_production()
        self.kingdom_total_storage = self._calculate_total_storage()
    
    
    def _build_kingdom_information(self) -> Text:
        city_information: Text = Text(
            text = f" {self.cities[0].campaign} ",
            style = "bold black on white",
            justify = "center",
        )
        return city_information
    
    def _build_campaign_table(self) -> Table:
        # table_style: Style = Style(color = self.configuration.get("production", {}).get("color", "#228b22"))
        table_style: Style = Style(color = "cyan")
        table: Table = Table(
            title = Text(text = "Campaign", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Total cities", header_style = "bold", justify = "center")
        table.add_column(header = "40% threshold", header_style = "bold", justify = "center")
        table.add_column(header = "Player cities", header_style = "bold", justify = "center")
        from math import ceil
        table.add_row(
            f"{self.number_of_cities_in_campaign}",
            f"{ceil(self.number_of_cities_in_campaign * 0.4)}",
            f"{len(self.cities)}",
        )
        
        return table
    
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
                name = "campaign",
                # size = production_height,
                # ratio = 0,
                # visible = include_production,
            ),
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
        
        layout["campaign"].update(
            renderable = Align(renderable = self._build_campaign_table(), align = "center"),
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
            height = len(self.cities) * 7,
        )
    
    def display_kingdom_results(self) -> None:
        console: Console = Console()
        console.print(self._build_kingdom_display())
