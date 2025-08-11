from typing import TypedDict

from rich.align import Align
from rich.console import Console
from rich.layout import Layout

from .building import BuildingsCount
from .city import City
from .display import CityDisplay, DisplayConfiguration, DisplaySection, DisplaySectionConfiguration, DEFAULT_SECTION_COLORS


class CityDict(TypedDict):
    name: str
    campaign: str
    buildings: BuildingsCount


class Scenario:
    
    def __init__(
            self,
            cities: list[City],
            configuration: DisplayConfiguration | None = None,
        ) -> None:
        self.cities: list[City] = cities
        self._user_configuration: DisplayConfiguration = configuration or {}
        self.configuration: DisplayConfiguration = self._build_configuration()
        
        self.cities_display: list[CityDisplay] = self._build_cities_display()
    
    @classmethod
    def from_list(
        cls,
        data: list[CityDict],
        configuration: DisplayConfiguration | None = None,
    ) -> "Scenario":
        cities: list[City] = [City(**city) for city in data]
        return cls(cities, configuration)
    
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
                return self._get_max_buildings_length()
            case "effects":
                return 8
            case "production":
                return 8
            case "storage":
                return 8
            case "defenses":
                return 6
        
        return 0
    
    def _get_max_buildings_length(self) -> int:
        building_lengths: list[int] = [len(city.buildings) + 2 for city in self.cities]
        return max(building_lengths)
    
    def _build_configuration(self) -> DisplayConfiguration:
        
        display_configuration: DisplayConfiguration = self._build_default_configuration()
        
        for section in display_configuration:
            section_config: DisplaySectionConfiguration = display_configuration[section]
            if section in self._user_configuration:
                display_configuration[section] = {**section_config, **self._user_configuration[section]}
        
        return display_configuration
    
    def _build_cities_display(self) -> list[CityDisplay]:
        cities_display: list[CityDisplay] = []
        
        for city in self.cities:
            city_display: CityDisplay = CityDisplay(
                city = city,
                configuration = self.configuration,
            )
            cities_display.append(city_display)
        
        return cities_display
    
    def _build_scenario_display(self) -> Layout:
        main_layout: Layout = Layout()
        row_layouts: list[Layout] = []
        
        for i in range(0, len(self.cities), 2):
            row: Layout = Layout(name = f"row_{i//2}")
            
            row.split_row(
                Layout(name = f"left_{i // 2}", ratio = 1),
                Layout(name = f"right_{i // 2}", ratio = 1),
            )
            
            row[f"left_{i // 2}"].update(
                renderable = Align(renderable = self.cities_display[i].build_city_display())
            )
            
            if i + 1 < len(self.cities):
                row[f"right_{i // 2}"].update(
                    renderable = Align(renderable = self.cities_display[i + 1].build_city_display())
                )
            else:
                row[f"right_{i // 2}"].update(
                    renderable = Align(renderable = "")
                )
            
            row_layouts.append(row)
        
        main_layout.split(*row_layouts)
        return main_layout
    
    def _calculate_console_height(self) -> int:
        from math import ceil
        qty_cities: int = len(self.cities)
        qty_display_rows: int = ceil(qty_cities / 2)
        
        # Height starts at 2 because of some strange thing rich does. There's always 2 lines missing otherwise.
        console_height: int = 2
        
        for section in self.configuration:
            if section not in [DisplaySection.EFFECTS.value, DisplaySection.BUILDINGS.value]:
                section_config: DisplaySectionConfiguration = self.configuration[section]
                console_height += section_config.get("height", 0) if section_config.get("include", False) else 0
        
        buildings: DisplaySectionConfiguration = self.configuration.get("buildings", {})
        include_buildings: bool = buildings.get("include", False)
        buildings_height: int = buildings.get("height", 0) if include_buildings else 0
        
        effects: DisplaySectionConfiguration = self.configuration.get("effects", {})
        include_effects: bool = effects.get("include", False)
        effects_height: int = effects.get("height", 0) if include_effects else 0
        
        buildings_and_effects_height: int = max(buildings_height, effects_height)
        
        return (console_height + buildings_and_effects_height) * qty_display_rows
    
    def display_scenario_results(self) -> None:
        console: Console = Console(width = 192, height = self._calculate_console_height())
        console.print(self._build_scenario_display())
