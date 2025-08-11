from typing import TypedDict

from rich.align import Align
from rich.console import Console
from rich.layout import Layout

from .building import BuildingsCount
from .city import City
from .display import DisplayConfiguration


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
    
    @classmethod
    def from_list(
        cls,
        data: list[CityDict],
    ) -> "Scenario":
        cities: list[City] = [City(**city) for city in data]
        return cls(cities)
