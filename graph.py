from modules.city import City
from modules.building import Building


possible_city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = [
        Building(id = "city_hall"),
        Building(id = "large_farm"),
        Building(id = "farmers_guild"),
    ]
)

impossible_city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = [
        Building(id = "village_hall"),
        Building(id = "large_farm"),
        Building(id = "farmers_guild"),
    ]
)

from dataclasses import dataclass

@dataclass
class CityValidator:
    city: City
    
    def validate_city(self) -> bool:
        ...
