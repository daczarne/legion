import yaml

from collections.abc import Generator
from pytest import fixture
from typing import Literal

from modules.building import _BuildingData, BuildingsCount, Building
from modules.city import _CityData, City


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


@fixture(scope = "function")
def _roman_military_buildings() -> Generator[BuildingsCount]:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "hospital": 1,
        "training_ground": 1,
        "gladiator_school": 1,
        "stables": 1,
        "bordello": 1,
        "quartermaster": 1,
        "large_fort": 1,
    }
    yield city_buildings


@fixture(scope = "function")
def _roman_military_city(_roman_military_buildings: BuildingsCount) -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Roma",
        buildings = _roman_military_buildings,
    )
    yield city


@fixture(scope = "function")
def _roman_food_producer_with_warehouse_buildings() -> Generator[BuildingsCount]:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "warehouse": 1,
        "farmers_guild": 1,
        "vineyard": 1,
        "large_farm": 4,
    }
    yield city_buildings


@fixture(scope = "function")
def _roman_food_producer_buildings() -> Generator[BuildingsCount]:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "farmers_guild": 1,
        "vineyard": 1,
        "large_farm": 5,
    }
    yield city_buildings


@fixture(scope = "function")
def _roman_food_producer_city(_roman_food_producer_buildings: BuildingsCount) -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Roma",
        buildings = _roman_food_producer_buildings,
    )
    yield city


@fixture(scope = "function")
def _roman_ore_producer_buildings() -> Generator[BuildingsCount]:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "miners_guild": 1,
        "large_mine": 6,
    }
    yield city_buildings


@fixture(scope = "function")
def _roman_ore_producer_city(_roman_ore_producer_buildings: BuildingsCount) -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Pentri",
        buildings = _roman_ore_producer_buildings,
    )
    yield city


@fixture(scope = "function")
def _roman_wood_producer_with_warehouse_buildings() -> Generator[BuildingsCount]:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "warehouse": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 5,
    }
    yield city_buildings


@fixture(scope = "function")
def _roman_wood_producer_buildings() -> Generator[BuildingsCount]:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 6,
    }
    yield city_buildings


@fixture(scope = "function")
def _roman_city_with_fishing_village() -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Faesula",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "farmers_guild": 1,
            "fishing_village": 1,
            "vineyard": 1,
            "large_farm": 4,
        },
    )
    yield city


@fixture(scope = "function")
def _roman_city_with_fishing_village_and_outcrop_mine() -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Falerii",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "farmers_guild": 1,
            "vineyard": 1,
            "outcrop_mine": 1,
            "large_farm": 4,
        },
    )
    yield city


@fixture(scope = "function")
def _roman_city_with_outcrop_and_mountain_mine() -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Caercini",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "miners_guild": 1,
            "outcrop_mine": 1,
            "mountain_mine": 1,
            "large_mine": 4,
        },
    )
    yield city


@fixture(scope = "function")
def _roman_city_with_outcrop_mine() -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Caercini",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "miners_guild": 1,
            "outcrop_mine": 1,
            "mountain_mine": 1,
            "large_mine": 4,
        },
    )
    yield city


@fixture(scope = "function")
def _roman_city_with_mountain_mines() -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Reate",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "miners_guild": 1,
            "mountain_mine": 2,
            "large_mine": 4,
        },
    )
    yield city


@fixture(scope = "function")
def _roman_city_with_mountain_mine() -> Generator[City]:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Hirpini",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "miners_guild": 1,
            "mountain_mine": 1,
            "large_mine": 5,
        },
    )
    yield city
