"""
Module for managing Kingdoms.

This module provides the `Kingdom` class for managing a collection of player-controlled cities in the same campaign. It
supports sorting cities by resource focus, calculating aggregated production and storage, and generating Rich terminal
output with tables for campaign, production, and storage.

The Kingdom class validates that the cities are not duplicated and that they all belong to the same campaign.

Public API:
    Kingdom (dataclass): Represents a collection of cities under a single campaign, tracking and displaying their
    production, storage capacity, and other aggregated statistics.
"""

from collections import Counter
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

from .city import City, CityDict, CITIES
from .resources import ResourceCollection, Resource


__all__: list[str] = ["Kingdom"]


@dataclass
class Kingdom:
    """
    Represents a collection of cities under a single campaign, tracking and displaying their production, storage
    capacity, and other aggregated statistics.
    
    A `Kingdom` contains multiple `City` objects from the same campaign. It can sort its cities by resource focus,
    validate campaign integrity, and calculate aggregated resource production and storage values (including a base
    storage capacity that is independent of cities). The class also supports generating rich terminal output with
    campaign, production, and storage tables.
    
    Attributes:
        cities (list[City]): list of `City` instances belonging to the kingdom.
        sort_order (list[str | None] | None): optional resource sort order for cities. Defaults to `["food", "ore",
            "wood", None]`). If not provided, a default order is used. Accept partial orders, e.g. `["ore"]` means
            "show ore first". For all resources not specified in the list the default will be used.
        campaign (str): the campaign name shared by all cities in the kingdom. Automatically set during initialization.
        number_of_cities_in_campaign (int): total number of cities in the campaign (including those not owned by the
            player). Calculated during initialization.
        kingdom_total_production (ResourceCollection): aggregated net production of all resources across the player's
            kingdom.
        kingdom_total_storage (ResourceCollection): aggregated total storage capacity across the player's kingdom,
            including the base storage.
        
    Class Attributes:
        BASE_KINGDOM_STORAGE (int): fixed storage amount (per resource) granted to the player, independent of any
            cities or buildings.
    
    Methods:
        sort_cities_by_focus(cities, order):
            Sorts a list of cities by resource focus according to the given order.
        from_list(data, sort_order):
            Creates a `Kingdom` from a list of city dictionaries.
        display_kingdom_results():
            Prints a formatted representation of the kingdom, including campaign info, production, and storage tables.
    
    Raises:
        ValueError: if there are duplicate city names or cities from multiple campaigns.
    """
    cities: list[City]
    sort_order: list[str | None] | None = field(default = None)
    
    
    # Post init values
    campaign: str = field(init = False)
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
        Sort cities by their primary resource focus in a specified order.
        
        If a resource is not listed in `order`, it will be appended to the end of the sorting order automatically.
        Cities with no focus (`None`) will also be placed at the end unless explicitly positioned.
        
        Args:
            cities (list[City]): list of `City` instances to sort.
            order (list[str | None]): desired sort order of resources, where each entry is a resource name (e.g.,
                "food") or `None` for cities without production.
        
        Returns:
            list[City]: a new list of cities sorted according to the specified order.
        
        Example:
            >>> sorted_cities = Kingdom.sort_cities_by_focus(cities, ["food", "ore"])
            # Orders cities producing food first, then ore, then wood, then None.
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
    
    def _sort_cities_by_focus_inplace(
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
        """
        Create a `Kingdom` instance from a list of raw city data dictionaries.
        
        Args:
            data (list[CityDict]): list of city data dictionaries. Each dictionary must contain valid keys for
                initializing a `City` instance.
            sort_order (list[str | None] | None): optional sort order for resources when arranging the cities. If
                `None`, the default order is used.
        
        Returns:
            Kingdom: a new `Kingdom` instance populated with the provided cities.
        
        Example:
            >>> raw_data = [{"name": "CityA", "campaign": "Alpha", "buildings": {"city_hall: 1, "farm": 4}}, ...]
            >>> kingdom = Kingdom.from_list(raw_data, ["ore", "wood"])
        """
        cities: list[City] = [City.from_buildings_count(**city) for city in data]
        return cls(cities, sort_order)
    
    
    #* Validate Kingdom
    def _validate_all_cities_are_unique(self) -> None:
        all_cities: list[str] = [city.name for city in self.cities]
        city_counts: Counter = Counter(all_cities)
        for city, count in city_counts.items():
            if count > 1:
                raise ValueError(f"Found duplicated city: {city}")
    
    def _validate_all_cities_are_from_the_same_campaign(self) -> None:
        all_campaigns: list[str] = [city.campaign for city in self.cities]
        campaign_counts: Counter = Counter(all_campaigns)
        if len(campaign_counts) > 1:
            raise ValueError(
                f"All cities must belong to the same campaign. "
                f"Found cities from: {" and ".join(campaign_counts.keys())}"
            )
    
    def _get_campaign(self) -> str:
        return self.cities[0].campaign
    
    def _get_number_of_cities_in_campaign(self) -> int:
        number_of_cities_in_campaign: int = 0
        
        for city in CITIES:
            if city.get("campaign") == self.campaign:
                number_of_cities_in_campaign += 1
        
        return number_of_cities_in_campaign
    
    
    #* Kingdom calculations
    def _calculate_total_production(self) -> ResourceCollection:
        total_production: ResourceCollection = ResourceCollection()
        
        for city in self.cities:
            total_production.food = total_production.food + city.production.balance.food
            total_production.ore = total_production.ore + city.production.balance.ore
            total_production.wood = total_production.wood + city.production.balance.wood
        
        return total_production
    
    def _calculate_total_storage(self) -> ResourceCollection:
        total_storage: ResourceCollection = ResourceCollection(
            food = self.BASE_KINGDOM_STORAGE,
            ore = self.BASE_KINGDOM_STORAGE,
            wood = self.BASE_KINGDOM_STORAGE,
        )
        
        for city in self.cities:
            total_storage.food += city.storage.total.food
            total_storage.ore += city.storage.total.ore
            total_storage.wood += city.storage.total.wood
        
        return total_storage
    
    
    def __post_init__(self) -> None:
        #* Kingdom validations
        self._validate_all_cities_are_unique()
        self._validate_all_cities_are_from_the_same_campaign()
        self._sort_cities_by_focus_inplace(order = self.sort_order)
        
        self.campaign = self._get_campaign()
        self.number_of_cities_in_campaign = self._get_number_of_cities_in_campaign()
        
        self.kingdom_total_production = self._calculate_total_production()
        self.kingdom_total_storage = self._calculate_total_storage()
    
    
    #* Kingdom display
    @staticmethod
    def _calculate_indentations(
            cell_value: int,
            width: int,
        ) -> int:
        CHARS_PER_THOUSAND_SEPARATOR: int = 3
        
        digits_in_number: int = len(str(cell_value))
        n_of_dashes: int = (digits_in_number - 1) // CHARS_PER_THOUSAND_SEPARATOR
        n_chars_in_number: int = digits_in_number + n_of_dashes
        
        if width <= n_chars_in_number:
            return 0
        
        return width - n_chars_in_number
    
    def _build_kingdom_information(self) -> Text:
        city_information: Text = Text(
            text = f" {self.campaign} ",
            style = "bold black on white",
            justify = "center",
        )
        return city_information
    
    def _build_campaign_table(self) -> Table:
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
                indentation_rss_potential: int = Kingdom._calculate_indentations(cell_value = rss_potential, width = 3)
                rss_potential_cell_value: str = f"{" " * indentation_rss_potential}[dim]({rss_potential})[/dim]"
                
                rss_balance: int = city.production.balance.get(key = rss)
                indentation_rss_balance: int = Kingdom._calculate_indentations(cell_value = rss_balance, width = 3)
                rss_balance_color: str = production_color if getattr(city.focus, "value", None) == rss else "white"
                rss_balance_color: str = production_color if Resource(value = rss) == city.focus else "white"
                rss_balance_cell_value: str = f"{" " * (indentation_rss_balance)}{f"[{rss_balance_color}]"}{rss_balance:_}{f"[/{rss_balance_color}]"}"
                
                row_element: str = f"{rss_potential_cell_value}{" " * 2}{rss_balance_cell_value}"
                row_elements.append(row_element)
            
            table.add_row(*row_elements)
        
        table.add_section()
        
        i_t_food: int = Kingdom._calculate_indentations(cell_value = self.kingdom_total_production.food, width = 10)
        i_t_ore: int = Kingdom._calculate_indentations(cell_value = self.kingdom_total_production.ore, width = 10)
        i_t_wood: int = Kingdom._calculate_indentations(cell_value = self.kingdom_total_production.wood, width = 10)
        
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
                
                rss_storage: int = city.storage.total.get(key = rss)
                indentation_rss_storage: int = Kingdom._calculate_indentations(cell_value = rss_storage, width = 6)
                rss_storage_color: str = storage_color if Resource(value = rss) == city.focus else "white"
                rss_storage_cell_value: str = f"{" " * (indentation_rss_storage)}{f"[{rss_storage_color}]"}{rss_storage:_}{f"[/{rss_storage_color}]"}"
                
                row_element: str = f"{rss_storage_cell_value}"
                row_elements.append(row_element)
            
            table.add_row(*row_elements)
        
        table.add_section()
        
        i_t_food: int = Kingdom._calculate_indentations(cell_value = self.kingdom_total_storage.food, width = 6)
        i_t_ore: int = Kingdom._calculate_indentations(cell_value = self.kingdom_total_storage.ore, width = 6)
        i_t_wood: int = Kingdom._calculate_indentations(cell_value = self.kingdom_total_storage.wood, width = 6)
        
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
    
    def display_kingdom(self) -> None:
        """
        Print a formatted table-based representation of the kingdom to the terminal.
        
        The display includes:
        
        1. Campaign name.
        2. Campaign summary (total cities in campaign, 40% threshold, cities owned).
        3. Production table (per city resource balance and potential).
        4. Storage table (per city resource storage capacity).
        
        Resource values for a city's primary focus are highlighted for quick reference. Production tables also include
        resource potential values in parentheses.
        """
        console: Console = Console()
        console.print(self._build_kingdom_display())
