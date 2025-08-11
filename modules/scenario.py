from typing import TypedDict

from rich.align import Align
from rich.console import Console
from rich.layout import Layout

from .building import BuildingsCount
from .city import City
from .display import CityDisplay


class CityDict(TypedDict):
    name: str
    campaign: str
    buildings: BuildingsCount


class Scenario:
    
    def __init__(
            self,
            cities: list[City],
        ) -> None:
        self.cities: list[City] = cities
        self.cities_display: list[CityDisplay] = [CityDisplay(city = city) for city in self.cities]
    
    @classmethod
    def from_list(
        cls,
        data: list[CityDict],
    ) -> "Scenario":
        cities: list[City] = [City(**city) for city in data]
        return cls(cities)
    
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
