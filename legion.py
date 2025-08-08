from math import prod
from modules.scenario import Scenario
from modules.city import City

scenario: Scenario = Scenario(
    campaign = "Hispania",
    city = "Numantia",
    buildings_a = {
        "city_hall": 1,
        "basilica": 1,
        "hospital": 1,
        "training_ground": 1,
        "gladiator_school": 1,
        "stables": 1,
        "bordello": 1,
        "quartermaster": 1,
        "large_fort": 1,
    },
    buildings_b = {
        "city_hall": 1,
        # "basilica": 1,
        # "hospital": 1,
        # "training_ground": 1,
        # "gladiator_school": 1,
        # "stables": 1,
        # "bordello": 1,
        # "quartermaster": 1,
        # "large_fort": 1,
    },
)

scenario.display_results()


city: City = City(
    campaign = "Hispania",
    name = "Numantia",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "hospital": 1,
        "training_ground": 1,
        "gladiator_school": 1,
        "stables": 1,
        "bordello": 1,
        "quartermaster": 1,
        "large_fort": 1,
    },
)

# city.display_results(
#     city = {
#         "include": False,
#     },
#     production = {
#         "include": False,
#     },
# )
