from modules.scenario import Scenario
from modules.city import City

scenario: Scenario = Scenario(
    campaign = "Unification of Italy",
    city = "Hernici",
    buildings_a = {
        "city_hall": 1,
        "basilica": 1,
        "fishing_village": 1,
        "outcrop_mine": 1,
        "miners_guild": 1,
        "large_mine": 4,
    },
    buildings_b = {
        "city_hall": 1,
        "basilica": 1,
        "fishing_village": 0,
        "outcrop_mine": 1,
        "large_mine": 5,
    },
)

# scenario.display_scenario_results(
#     city = {
#         "include": True,
#     },
#     buildings = {
#         "include": True,
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


city: City = City(
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

city.display_city_results(
    city = {
        "include": True,
    },
    buildings = {
        "include": True,
    },
    effects = {
        "include": True,
    },
    production = {
        "include": True,
    },
    storage = {
        "include": True,
    },
    defenses = {
        "include": True,
    },
)
