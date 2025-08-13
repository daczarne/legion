from modules.city import City
from modules.scenario import Scenario
from modules.kingdom import Kingdom

scenario: Scenario = Scenario.from_list(
    data = [
        {
            "campaign": "Unification of Italy",
            "name": "Roma",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 5,
                "vineyard": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Latins",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "carpenters_guild": 1,
                "large_lumber_mill": 5,
                "warehouse": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Hernici",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "outcrop_mine": 1,
                "fishing_village": 1,
                "large_mine": 4,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Anxur",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 5,
                "vineyard": 1,
            },
        },
    ],
    configuration = {
        "city": {
            "include": True,
        },
        "defenses": {
            "include": False,
        },
        "storage": {
            "include": False,
        },
    },
)

# scenario.display_scenario_results()

kingdom: Kingdom = Kingdom.from_list(
    data = [
        {
            "campaign": "Unification of Italy",
            "name": "Roma",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 5,
                "vineyard": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Latins",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "carpenters_guild": 1,
                "large_lumber_mill": 5,
                "warehouse": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Hernici",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "outcrop_mine": 1,
                "fishing_village": 1,
                "large_mine": 4,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Anxur",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 5,
                "vineyard": 1,
            },
        },
    ],
    sort_order = [None, "ore", "food", "wood"]
)

kingdom.display_kingdom_results()

city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "farmers_guild": 1,
        "large_farm": 5,
        "vineyard": 1,
    },
)
