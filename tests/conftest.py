from pytest import fixture
import yaml
from collections.abc import Generator
from typing import Literal, Any

from modules.city import CityData


@fixture(scope = "function")
def _errors() -> Generator[list]:
    """
    Creates the _errors array.
    """
    yield []


@fixture(scope = "session")
def _cities() -> Generator[list[CityData]]:
    """
    Loads the cities.yaml file.
    """
    with open(file = "./data/cities.yaml", mode = "r") as file:
        cities_data: dict[Literal["cities"], list[CityData]] = yaml.safe_load(stream = file)
    
    yield cities_data["cities"]


@fixture(scope = "session")
def _buildings() -> Generator[list]:
    """
    Loads the buildings.yaml file.
    """
    with open(file = "./data/buildings.yaml", mode = "r") as file:
        buildings_data: dict[Literal["buildings"], list[dict[str, Any]]] = yaml.safe_load(stream = file)
    
    yield buildings_data["buildings"]
