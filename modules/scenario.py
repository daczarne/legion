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
        
        self.cities_display: list[CityDisplay] = self._build_cities_display()
        # self.configuration: DisplayConfiguration = self._build_configuration()
    
    @classmethod
    def from_list(
        cls,
        data: list[CityDict],
        configuration: DisplayConfiguration | None = None,
    ) -> "Scenario":
        cities: list[City] = [City(**city) for city in data]
        return cls(cities, configuration)
    
    def _get_max_buildings_length(self) -> int:
        building_lengths: list[int] = [len(city.buildings) + 2 for city in self.cities]
        return max(building_lengths)
    
    def _build_cities_display(self) -> list[CityDisplay]:
        cities_display: list[CityDisplay] = []
        
        for city in self.cities:
            city_display: CityDisplay = CityDisplay(
                city = city,
                configuration = {
                    "buildings": {
                        "height": self._get_max_buildings_length(),
                    },
                },
            )
            cities_display.append(city_display)
        
        return cities_display
    
    def _build_scenario_display(
            self,
        ) -> Layout:
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
