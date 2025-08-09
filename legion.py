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
        "basilica": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 6,
    },
)

scenario.display_scenario_results()


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
#         "include": True,
#     },
#     buildings = {
#         "include": True,
#         "height": 11,
#     },
#     effects = {
#         "include": True,
#     },
#     production = {
#         "include": True,
#     },
#     storage = {
#         "include": True,
#     },
#     defenses = {
#         "include": True,
#     },
# )
