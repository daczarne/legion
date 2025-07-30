from typing import TypedDict

class Scenario(TypedDict):
    production_potentials: list[int]
    city_buildings: dict[str, int]
