from math import floor


from modules.city import City, CityBuildings
from modules.scenario import Scenario

scenario_1: City = City(
    campaign = "Italica",
    name = "Roma",
    resource_potentials = {
        "food": 125,
        "ore": 0,
        "wood": 50,
    },
    buildings = CityBuildings(
        buildings = {
            "farm": 6,
            "basilica": 1,
            "farmers_guild": 1,
        },
    ),
)
