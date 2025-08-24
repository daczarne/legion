import yaml

from collections.abc import Generator
from pytest import fixture
from typing import Literal

from modules.building import _BuildingData
from modules.city import _CityData


@fixture(scope = "function")
def _errors() -> Generator[list]:
    """
    Creates the _errors array.
    """
    yield []


@fixture(scope = "session")
def _cities() -> Generator[list[_CityData]]:
    """
    Loads the cities.yaml file.
    """
    with open(file = "./data/cities.yaml", mode = "r") as file:
        cities_data: dict[Literal["cities"], list[_CityData]] = yaml.safe_load(stream = file)
    
    yield cities_data["cities"]


@fixture(scope = "session")
def _buildings() -> Generator[list[_BuildingData]]:
    """
    Loads the buildings.yaml file.
    """
    with open(file = "./data/buildings.yaml", mode = "r") as file:
        buildings_data: dict[Literal["buildings"], list[_BuildingData]] = yaml.safe_load(stream = file)
    
    yield buildings_data["buildings"]
