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

from .city import CITIES, City
from .resources import ResourceCollection, Resource
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
    def sort_cities_by_focus(
            cities: list[City],
            order: list[str | None],
        ) -> list[City]:
        """
        Sort cities by "focus" (rss with the highest production) and alphabetically within each type.
        """
        if "food" not in order:
            order.append("food")
        
        if "ore" not in order:
            order.append("ore")
        
        if "wood" not in order:
            order.append("wood")
        
        if None not in order:
            order.append(None)
        
        normalized_order: list[Resource | None] = [
            Resource(value = item) if isinstance(item, str) else None for item in order
        ]
        
        return sorted(cities, key = lambda city: (normalized_order.index(city.focus), city.name))
    
    def sort_cities_by_focus_inplace(
        self,
        order: list[str | None] | None = None,
    ) -> None:
        """
        Replace self.cities with the sorted list according to the provided order.
        """
        self.cities = Kingdom.sort_cities_by_focus(
            cities = self.cities,
            order = ["food", "ore", "wood", None] if order is None else order,
        )
    
    
    @classmethod
    def from_list(
        cls,
        data: list[CityDict],
        sort_order: list[str | None] | None = None,
    ) -> "Kingdom":
        cities: list[City] = [City(**city) for city in data]
        return cls(cities, sort_order)
        # return cls(cities)
    
    
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
        self.sort_cities_by_focus_inplace(order = self.sort_order)
        self.number_of_cities_in_campaign = self._get_number_of_cities_in_campaign()
        self.kingdom_total_production = self._calculate_total_production()
        self.kingdom_total_storage = self._calculate_total_storage()
    
    def _calculate_indentations(
            self,
            cell_value: int,
            width: int,
        ) -> int:
        CHARS_PER_THOUSAND_SEPARATOR: int = 3
        
        digits_in_number: int = len(str(cell_value))
        n_of_dashes: int = (digits_in_number - 1) // CHARS_PER_THOUSAND_SEPARATOR
        n_chars_in_number: int = digits_in_number + n_of_dashes
        
        return width - n_chars_in_number
    
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
        production_color: str = "#228b22"
        table_style: Style = Style(color = production_color)
        table: Table = Table(
            title = Text(text = "Production", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        city_column_header: str = "City"
        city_name_lengths: list[int] = [len(city.name) for city in self.cities]
        max_city_name_length: int = max(city_name_lengths)
        cell_length: int = max_city_name_length - len(city_column_header)
        left_side_justification: int = cell_length // 2
        
        table.add_column(header = f"{" " * left_side_justification}{city_column_header}", header_style = "bold")
        table.add_column(header = f"{" " * 3}Food", header_style = "bold", justify = "left")
        table.add_column(header = f"{" " * 3}Ore", header_style = "bold", justify = "left")
        table.add_column(header = f"{" " * 3}Wood", header_style = "bold", justify = "left")
        
        for city in self.cities:
            
            row_elements: list[str] = [f"{city.name}"]
            
            for rss in ["food", "ore", "wood"]:
                rss_potential: int = city.resource_potentials.get(key = rss)
                indentation_rss_potential: int = self._calculate_indentations(cell_value = rss_potential, width = 3)
                rss_potential_cell_value: str = f"{" " * indentation_rss_potential}[dim]({rss_potential})[/dim]"
                
                rss_balance: int = city.balance.get(key = rss)
                indentation_rss_balance: int = self._calculate_indentations(cell_value = rss_balance, width = 3)
                # rss_balance_color: str = production_color if city.focus.value == rss else "white"
                # rss_balance_cell_value: str = f"{" " * (indentation_rss_balance)}{f"[{rss_balance_color}]"}{rss_balance:_}{f"[/{rss_balance_color}]"}"
                rss_balance_cell_value: str = f"{" " * (indentation_rss_balance)}{rss_balance:_}"
                
                row_element: str = f"{rss_potential_cell_value}{" " * 2}{rss_balance_cell_value}"
                row_elements.append(row_element)
            
            table.add_row(*row_elements)
        
        table.add_section()
        
        i_t_food: int = self._calculate_indentations(cell_value = self.kingdom_total_production.food, width = 10)
        i_t_ore: int = self._calculate_indentations(cell_value = self.kingdom_total_production.ore, width = 10)
        i_t_wood: int = self._calculate_indentations(cell_value = self.kingdom_total_production.wood, width = 10)
        
        table.add_row(
            f"Total",
            f"{" " * i_t_food}{self.kingdom_total_production.food:_}",
            f"{" " * i_t_ore}{self.kingdom_total_production.ore:_}",
            f"{" " * i_t_wood}{self.kingdom_total_production.wood:_}",
            style = table_style + Style(bold = True),
        )
        
        return table
    
    def _build_kingdom_storage_table(self) -> Table:
        storage_color: str = "purple"
        table_style: Style = Style(color = storage_color)
        table: Table = Table(
            title = Text(text = "Storage", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        city_column_header: str = "City"
        city_name_lengths: list[int] = [len(city.name) for city in self.cities]
        max_city_name_length: int = max(city_name_lengths)
        cell_length: int = max_city_name_length - len(city_column_header)
        left_side_justification: int = cell_length // 2
        
        table.add_column(header = f"{" " * left_side_justification}{city_column_header}", header_style = "bold")
        table.add_column(header = f"{" " * 1}Food", header_style = "bold", justify = "left")
        table.add_column(header = f"{" " * 2}Ore", header_style = "bold", justify = "left")
        table.add_column(header = f"{" " * 1}Wood", header_style = "bold", justify = "left")
        
        for city in self.cities:
            
            row_elements: list[str] = [f"{city.name}"]
            
            for rss in ["food", "ore", "wood"]:
                
                rss_storage: int = city.total_storage.get(key = rss)
                indentation_rss_storage: int = self._calculate_indentations(cell_value = rss_storage, width = 6)
                # rss_storage_color: str = storage_color if city.focus.value == rss else "white"
                # rss_storage_cell_value: str = f"{" " * (indentation_rss_storage)}{f"[{rss_storage_color}]"}{rss_storage:_}{f"[/{rss_storage_color}]"}"
                rss_storage_cell_value: str = f"{" " * (indentation_rss_storage)}{rss_storage:_}"
                
                row_element: str = f"{rss_storage_cell_value}"
                row_elements.append(row_element)
            
            table.add_row(*row_elements)
        
        table.add_section()
        
        i_t_food: int = self._calculate_indentations(cell_value = self.kingdom_total_storage.food, width = 6)
        i_t_ore: int = self._calculate_indentations(cell_value = self.kingdom_total_storage.ore, width = 6)
        i_t_wood: int = self._calculate_indentations(cell_value = self.kingdom_total_storage.wood, width = 6)
        
        table.add_row(
            f"Total",
            f"{" " * i_t_food}{self.kingdom_total_storage.food:_}",
            f"{" " * i_t_ore}{self.kingdom_total_storage.ore:_}",
            f"{" " * i_t_wood}{self.kingdom_total_storage.wood:_}",
            style = table_style + Style(bold = True),
        )
        
        return table
    
    def _build_kingdom_display(self) -> Panel:
        header_height: int = 2
        campaign_height: int = 7
        production_and_storage_height: int = len(self.cities) + 9
        main_height: int = campaign_height + production_and_storage_height
        total_height: int = header_height + main_height
        
        layout: Layout = Layout()
        
        layout.split(
            Layout(
                name = "header",
                size = header_height,
                ratio = 0,
            ),
            Layout(
                name = "main",
                size = main_height,
                ratio = 0,
            ),
        )
        
        layout["header"].update(
            renderable = Align(renderable = self._build_kingdom_information(), align = "center"),
        )
        
        layout["main"].split(
            Layout(
                name = "campaign",
                size = campaign_height,
                ratio = 0,
            ),
            Layout(
                name = "production_and_storage",
                size = production_and_storage_height,
                ratio = 0,
            ),
        )
        
        layout["campaign"].update(
            renderable = Align(renderable = self._build_campaign_table(), align = "center"),
        )
        
        layout["production_and_storage"].split_row(
            Layout(name = "production", ratio = 4),
            Layout(name = "storage_capacity", ratio = 3),
        )
        
        layout["production"].update(
            renderable = Align(renderable = self._build_kingdom_production_table(), align = "center"),
        )
        
        layout["storage_capacity"].update(
            renderable = Align(renderable = self._build_kingdom_storage_table(), align = "center"),
        )
        
        return Panel(
            renderable = layout,
            width = 110,
            height = total_height,
        )
    
    def display_kingdom_results(self) -> None:
        console: Console = Console()
        console.print(self._build_kingdom_display())
