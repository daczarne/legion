from enum import Enum
from typing import TypeAlias, TypedDict

from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .building import BUILDINGS
from .city import City


DisplaySectionColors: TypeAlias = dict[str, str]


class DisplaySection(Enum):
    CITY = "city"
    BUILDINGS = "buildings"
    EFFECTS = "effects"
    PRODUCTION = "production"
    STORAGE = "storage"
    DEFENSES = "defenses"


class DisplaySectionConfiguration(TypedDict, total = False):
    include: bool
    height: int
    color: str


class DisplayConfiguration(TypedDict, total = False):
    city: DisplaySectionConfiguration
    buildings: DisplaySectionConfiguration
    effects: DisplaySectionConfiguration
    production: DisplaySectionConfiguration
    storage: DisplaySectionConfiguration
    defenses: DisplaySectionConfiguration


DEFAULT_SECTION_COLORS: DisplaySectionColors = {
    "effects": "#5f5fff",
    "production": "#228b22",
    "storage": "purple",
    "defenses": "red",
}


# * ************ * #
# * CITY DISPLAY * #
# * ************ * #

class CityDisplay:
    
    def __init__(
            self,
            city: City,
            configuration: DisplayConfiguration | None = None,
        ) -> None:
        self.city: City = city
        self._user_configuration: DisplayConfiguration = configuration or {}
        self.configuration: DisplayConfiguration = self._build_configuration()
    
    def _build_default_configuration(self) -> DisplayConfiguration:
        sections: list[str] = [
            "city",
            "buildings",
            "effects",
            "production",
            "storage",
            "defenses",
        ]
        
        default_configuration: DisplayConfiguration = {}
        for section in sections:
            default_configuration[section] = {
                "include": True,
                "height": self._calculate_default_section_height(section = section),
                "color": DEFAULT_SECTION_COLORS.get(section, "white"),
            }
        
        return default_configuration
    
    def _calculate_default_section_height(self, section) -> int:
        match section:
            case "city":
                return 2
            case "buildings":
                return len(self.city.buildings) + 2
            case "effects":
                return 8
            case "production":
                return 8
            case "storage":
                return 8
            case "defenses":
                return 6
        
        return 0
    
    def _build_configuration(self) -> DisplayConfiguration:
        
        display_configuration: DisplayConfiguration = self._build_default_configuration()
        
        for section in display_configuration:
            section_config: DisplaySectionConfiguration = display_configuration[section]
            if section in self._user_configuration:
                display_configuration[section] = {**section_config, **self._user_configuration[section]}
        
        return display_configuration
    
    #* Display results
    def _build_city_information(self) -> Text:
        city_information: Text = Text(
            text = f" {self.city.campaign} --- {self.city.name} ",
            style = "bold black on white",
            justify = "center",
        )
        return city_information
    
    def _build_city_buildings_list(self) -> Table:
        city_buildings_text: Text = Text()
        
        for building, qty in self.city.buildings.items():
            city_buildings_text.append(text = f"  - {BUILDINGS[building].name} ({qty})\n")
        
        city_buildings_table: Table = Table(title = "Buildings", show_header = False, box = None, padding = (0, 1))
        city_buildings_table.add_column()
        city_buildings_table.add_row()
        city_buildings_table.add_row(city_buildings_text)
        
        return city_buildings_table
    
    def _build_city_effects_table(self) -> Table:
        table_style: Style = Style(color = self.configuration.get("effects", {}).get("color", "#5f5fff"))
        table: Table = Table(
            title = Text(text = "Effects", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Effect", header_style = "bold", justify = "center")
        table.add_column(header = "City", header_style = "bold", justify = "right")
        table.add_column(header = "Buildings", header_style = "bold", justify = "right")
        table.add_column(header = "Workers", header_style = "bold", justify = "right")
        table.add_column(header = "Total", header_style = "bold", justify = "right")
        
        table.add_row(
            "Troop training",
            f"{self.city.city_effects.troop_training}",
            f"{self.city.building_effects.troop_training}",
            f"{self.city.worker_effects.troop_training}",
            Text(text = f"{self.city.total_effects.troop_training}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            "Pop. growth",
            f"{self.city.city_effects.population_growth}",
            f"{self.city.building_effects.population_growth}",
            f"{self.city.worker_effects.population_growth}",
            Text(text = f"{self.city.total_effects.population_growth}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            "Intelligence",
            f"{self.city.city_effects.intelligence}",
            f"{self.city.building_effects.intelligence}",
            f"{self.city.worker_effects.intelligence}",
            Text(text = f"{self.city.total_effects.intelligence}", style = table_style + Style(bold = True)),
        )
        
        return table
    
    def _build_city_production_table(self) -> Table:
        table_style: Style = Style(color = self.configuration.get("production", {}).get("color", "#228b22"))
        table: Table = Table(
            title = Text(text = "Production", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Resource", header_style = "bold", justify = "left")
        table.add_column(header = "Rss. pot.", header_style = "bold", justify = "right")
        table.add_column(header = "Base prod.", header_style = "bold", justify = "right")
        table.add_column(header = "Prod. bonus", header_style = "bold", justify = "right")
        table.add_column(header = "Total prod", header_style = "bold", justify = "right")
        table.add_column(header = "Maintenance", header_style = "bold", justify = "right")
        table.add_column(header = "Balance", header_style = "bold", justify = "right")
        
        table.add_row(
            f"Food",
            f"{self.city.resource_potentials.food}",
            f"{self.city.base_production.food}",
            f"{self.city.productivity_bonuses.food}",
            f"{self.city.total_production.food}",
            f"{-1 * self.city.maintenance_costs.food}",
            Text(text = f"{self.city.balance.food}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            f"Ore",
            f"{self.city.resource_potentials.ore}",
            f"{self.city.base_production.ore}",
            f"{self.city.productivity_bonuses.ore}",
            f"{self.city.total_production.ore}",
            f"{-1 * self.city.maintenance_costs.ore}",
            Text(text = f"{self.city.balance.ore}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            f"Wood",
            f"{self.city.resource_potentials.wood}",
            f"{self.city.base_production.wood}",
            f"{self.city.productivity_bonuses.wood}",
            f"{self.city.total_production.wood}",
            f"{-1 * self.city.maintenance_costs.wood}",
            Text(text = f"{self.city.balance.wood}", style = table_style + Style(bold = True)),
        )
        
        return table
    
    def _build_city_storage_table(self) -> Table:
        table_style: Style = Style(color = self.configuration.get("storage", {}).get("color", "purple"))
        table: Table = Table(
            title = Text(text = "Storage capacity", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Resource", header_style = "bold", justify = "left")
        table.add_column(header = "City", header_style = "bold", justify = "right")
        table.add_column(header = "Buildings", header_style = "bold", justify = "right")
        table.add_column(header = "Warehouse", header_style = "bold", justify = "right")
        table.add_column(header = "Supply dump", header_style = "bold", justify = "right")
        table.add_column(header = "Total", header_style = "bold", justify = "right")
        
        table.add_row(
            "Food",
            f"{self.city.city_storage.food}",
            f"{self.city.buildings_storage.food}",
            f"{self.city.warehouse_storage.food}",
            f"{self.city.supply_dump_storage.food}",
            Text(text = f"{self.city.total_storage.food}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            "Ore",
            f"{self.city.city_storage.ore}",
            f"{self.city.buildings_storage.ore}",
            f"{self.city.warehouse_storage.ore}",
            f"{self.city.supply_dump_storage.ore}",
            Text(text = f"{self.city.total_storage.ore}", style = table_style + Style(bold = True)),
        )
        table.add_row(
            "Wood",
            f"{self.city.city_storage.wood}",
            f"{self.city.buildings_storage.wood}",
            f"{self.city.warehouse_storage.wood}",
            f"{self.city.supply_dump_storage.wood}",
            Text(text = f"{self.city.total_storage.wood}", style = table_style + Style(bold = True)),
        )
        
        return table
    
    def _build_defenses_table(self) -> Table:
        table_style: Style = Style(color = self.configuration.get("defenses", {}).get("color", "red"))
        table: Table = Table(
            title = Text(text = "Defenses", style = table_style + Style(italic = True)),
            style = table_style,
            box = box.HEAVY,
        )
        
        table.add_column(header = "Garrison", header_style = "bold", justify = "center")
        table.add_column(header = "Squadrons", header_style = "bold", justify = "center")
        table.add_column(header = "Squadron size", header_style = "bold", justify = "center")
        
        table.add_row(
            f"{self.city.garrison}",
            f"{self.city.squadrons}",
            f"{self.city.squadron_size}",
        )
        
        return table
    
    def build_city_display(self) -> Panel:
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
        
        #* Include booleans
        include_city: bool = self.configuration.get("city", {}).get("include", True)
        include_buildings: bool = self.configuration.get("buildings", {}).get("include", True)
        include_effects: bool = self.configuration.get("effects", {}).get("include", True)
        include_production: bool = self.configuration.get("production", {}).get("include", True)
        include_storage: bool = self.configuration.get("storage", {}).get("include", True)
        include_defenses: bool = self.configuration.get("defenses", {}).get("include", True)
        
        #* Heights
        city_height: int = self.configuration.get("city", {}).get("height", 0) if include_city else 0
        buildings_height: int = self.configuration.get("buildings", {}).get("height", 0) if include_buildings else 0
        effects_height: int = self.configuration.get("effects", {}).get("height", 0) if include_effects else 0
        production_height: int = self.configuration.get("production", {}).get("height", 0) if include_production else 0
        storage_height: int = self.configuration.get("storage", {}).get("height", 0) if include_storage else 0
        defenses_height: int = self.configuration.get("defenses", {}).get("height", 0) if include_defenses else 0
        
        buildings_and_effects_height: int = max(buildings_height, effects_height)
        main_height: int = buildings_and_effects_height + production_height + storage_height + defenses_height
        
        total_layout_height: int = city_height + main_height + 2
        total_layout_width: int = 92
        
        #* Layout
        layout: Layout = Layout()
        
        layout.split(
            Layout(
                name = "header",
                size = city_height,
                ratio = 0,
                visible = include_city,
            ),
            Layout(
                name = "main",
                size = main_height,
                ratio = 0,
                visible = any([
                    include_buildings,
                    include_effects,
                    include_production,
                    include_storage,
                    include_defenses,
                ]),
            ),
        )
        
        layout["header"].update(
            renderable = Align(renderable = self._build_city_information(), align = "center"),
        )
        
        layout["main"].split(
            Layout(
                name = "buildings_and_effects",
                size = buildings_and_effects_height,
                ratio = 0,
                visible = any([include_buildings, include_effects]),
            ),
            Layout(
                name = "production",
                size = production_height,
                ratio = 0,
                visible = include_production,
            ),
            Layout(
                name = "storage_capacity",
                size = storage_height,
                ratio = 0,
                visible = include_storage,
            ),
            Layout(
                name = "defenses",
                size = defenses_height,
                ratio = 0,
                visible = include_defenses,
            ),
        )
        
        layout["buildings_and_effects"].split_row(
            Layout(name = "buildings", ratio = 1),
            Layout(name = "effects", ratio = 2),
        )
        
        if include_buildings:
            layout["buildings"].update(
                renderable = Align(renderable = self._build_city_buildings_list(), align = "center"),
            )
        else:
            layout["buildings"].update(
                renderable = Align(renderable = "", align = "center"),
            )
        
        if include_effects:
            layout["effects"].update(
                renderable = Align(renderable = self._build_city_effects_table(), align = "center"),
            )
        else:
            layout["effects"].update(
                renderable = Align(renderable = "", align = "center"),
            )
        
        layout["production"].update(
            renderable = Align(renderable = self._build_city_production_table(), align = "center"),
        )
        
        layout["storage_capacity"].update(
            renderable = Align(renderable = self._build_city_storage_table(), align = "center"),
        )
        
        layout["defenses"].update(
            renderable = Align(renderable = self._build_defenses_table(), align = "center"),
        )
        
        return Panel(
            renderable = layout,
            width = total_layout_width,
            height = total_layout_height,
        )
    
    def display_city_results(self) -> None:
        console: Console = Console()
        console.print(self.build_city_display())
