from pytest import fixture
import yaml
from typing import Any, Generator

from modules.city_data import CitiesData, CityData

@fixture(scope = "session")
def _cities() -> Generator[list[CityData]]:
    """
    Loads the buildings.yaml file.
    """
    with open(file = "./data/buildings.yaml", mode = "r") as file:
        cities_data: CitiesData = yaml.safe_load(stream = file)
    
    yield cities_data["cities"]
