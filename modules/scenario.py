from typing import TypedDict

from rich.align import Align
from rich.console import Console
from rich.layout import Layout

from .building import BuildingsCount
from .city import City
from .display import CityDisplay, DisplayConfiguration, DisplaySectionConfiguration, DEFAULT_SECTION_COLORS


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
        layout: Layout = Layout()
        
        layout.split_row(
            Layout(name = "city_a", ratio = 1),
            Layout(name = "city_b", ratio = 1),
        )
        
        layout["city_a"].update(
            renderable = Align(renderable = self.cities_display[0].build_city_display())
        )
        
        layout["city_b"].update(
            renderable = Align(renderable = self.cities_display[1].build_city_display())
        )
        
        return layout
    
    def display_scenario_results(self) -> None:
        console: Console = Console()
        console.print(self._build_scenario_display())
