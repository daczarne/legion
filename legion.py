from modules.scenario import Scenario
from modules.city import City

Scenario(
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
).display_results()


# City(
#     campaign = "Hispania",
#     name = "Numantia",
#     buildings = {
#         "city_hall": 1,
#         "basilica": 1,
#         "hospital": 1,
#         "training_ground": 1,
#         "gladiator_school": 1,
#         "stables": 1,
#         "bordello": 1,
#         "quartermaster": 1,
#         "large_fort": 1,
#     },
# ).display_results(
#     include_city = True,
#     include_production = True,
#     include_storage = True,
#     include_defenses = False,
# )
