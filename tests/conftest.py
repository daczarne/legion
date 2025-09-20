from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal

import yaml

from modules.city import City

from pytest import fixture


if TYPE_CHECKING:
    from collections.abc import Generator
    
    from modules.building import BuildingsCount, _BuildingData
    from modules.city import _CityData


@fixture(scope = "function")
def _errors() -> list:
    # Creates the _errors array.
    return []


@fixture(scope = "session")
def _cities() -> Generator[list[_CityData]]:
    # Loads the cities.yaml file.
    
    with Path("./data/cities.yaml").open(mode = "r") as file:
        cities_data: dict[Literal["cities"], list[_CityData]] = yaml.safe_load(stream = file)
        yield cities_data["cities"]


@fixture(scope = "session")
def _buildings() -> Generator[list[_BuildingData]]:
    # Loads the buildings.yaml file.
    
    with Path("./data/buildings.yaml").open(mode = "r") as file:
        buildings_data: dict[Literal["buildings"], list[_BuildingData]] = yaml.safe_load(stream = file)
        yield buildings_data["buildings"]


@fixture(scope = "function")
def _roman_military_buildings() -> BuildingsCount:
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
    return city_buildings


@fixture(scope = "function")
def _roman_military_city(_roman_military_buildings: BuildingsCount) -> City:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Roma",
        buildings = _roman_military_buildings,
    )
    return city


@fixture(scope = "function")
def _roman_food_producer_with_warehouse_buildings() -> BuildingsCount:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "warehouse": 1,
        "farmers_guild": 1,
        "vineyard": 1,
        "large_farm": 4,
    }
    return city_buildings


@fixture(scope = "function")
def _roman_food_producer_buildings() -> BuildingsCount:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "farmers_guild": 1,
        "vineyard": 1,
        "large_farm": 5,
    }
    return city_buildings


@fixture(scope = "function")
def _roman_food_producer_city(_roman_food_producer_buildings: BuildingsCount) -> City:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Roma",
        buildings = _roman_food_producer_buildings,
    )
    return city


@fixture(scope = "function")
def _roman_ore_producer_buildings() -> BuildingsCount:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "miners_guild": 1,
        "large_mine": 6,
    }
    return city_buildings


@fixture(scope = "function")
def _roman_ore_producer_city(_roman_ore_producer_buildings: BuildingsCount) -> City:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Pentri",
        buildings = _roman_ore_producer_buildings,
    )
    return city


@fixture(scope = "function")
def _roman_wood_producer_with_warehouse_buildings() -> BuildingsCount:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "warehouse": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 5,
    }
    return city_buildings


@fixture(scope = "function")
def _roman_wood_producer_buildings() -> BuildingsCount:
    city_buildings: BuildingsCount = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 6,
    }
    return city_buildings


@fixture(scope = "function")
def _roman_wood_producer_city(_roman_wood_producer_buildings: BuildingsCount) -> City:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Lingones",
        buildings = _roman_wood_producer_buildings,
    )
    return city


@fixture(scope = "function")
def _roman_city_with_fishing_village() -> City:
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
    return city


@fixture(scope = "function")
def _roman_city_with_fishing_village_and_outcrop_mine() -> City:
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
    return city


@fixture(scope = "function")
def _roman_city_with_outcrop_and_mountain_mine() -> City:
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
    return city


@fixture(scope = "function")
def _roman_city_with_outcrop_mine() -> City:
    city: City = City.from_buildings_count(
        campaign = "Unification of Italy",
        name = "Caudini",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "miners_guild": 1,
            "outcrop_mine": 1,
            "large_mine": 5,
        },
    )
    return city


@fixture(scope = "function")
def _roman_city_with_mountain_mines() -> City:
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
    return city


@fixture(scope = "function")
def _roman_city_with_mountain_mine() -> City:
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
    return city


@fixture(scope = "function")
def _roman_fort() -> City:
    city: City = City.from_buildings_count(
        campaign = "Germania",
        name = "Vetera",
        buildings = {},
    )
    return city


@fixture(scope = "function")
def _roman_city_with_supply_dump() -> City:
    city: City = City.from_buildings_count(
        campaign = "Germania",
        name = "Rogomagnum",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "supply_dump": 1,
            "farmers_guild": 1,
            "vineyard": 1,
            "large_farm": 4,
        },
    )
    return city
