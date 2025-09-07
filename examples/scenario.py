from modules.scenario import Scenario


scenario: Scenario = Scenario.from_list(
    data = [
        {
            "campaign": "Unification of Italy",
            "name": "Reate",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 2,
                "large_mine": 4,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Reate",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "mountain_mine": 2,
                "large_mine": 5,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Reate",
            "buildings": {
                "city_hall": 1,
                "miners_guild": 1,
                "mountain_mine": 2,
                "large_mine": 5,
            },
        },
    ],
    configuration = {
        "storage": {
            "include": False,
        },
        "defenses": {
            "include": False,
        },
    },
)

scenario.display_scenario()
print()

scenario: Scenario = Scenario.from_list(
    data = [
        {
            "campaign": "Unification of Italy",
            "name": "Hernici",
            "buildings": {
                "town_hall": 1,
                "temple": 1,
                "outcrop_mine": 1,
                "fishing_village": 1,
                "hunters_lodge": 3,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Hernici",
            "buildings": {
                "town_hall": 1,
                "outcrop_mine": 1,
                "fishing_village": 1,
                "hunters_lodge": 4,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Hernici",
            "buildings": {
                "town_hall": 1,
                "temple": 1,
                "outcrop_mine": 1,
                "fishing_village": 1,
                "large_mine": 3,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Hernici",
            "buildings": {
                "town_hall": 1,
                "outcrop_mine": 1,
                "fishing_village": 1,
                "large_mine": 4,
            },
        },
    ],
    configuration = {
        "storage": {
            "include": False,
        },
        "defenses": {
            "include": False,
        },
    },
)

scenario.display_scenario()
print()

scenario: Scenario = Scenario.from_list(
    data = [
        {
            "campaign": "Conquest of Britain",
            "name": "Anderitum",
            "buildings": {
                "town_hall": 1,
                "supply_dump": 1,
                "temple": 1,
                "hunters_lodge": 4,
            },
        },
        {
            "campaign": "Conquest of Britain",
            "name": "Anderitum",
            "buildings": {
                "town_hall": 1,
                "supply_dump": 1,
                "hunters_lodge": 5,
            },
        },
        {
            "campaign": "Conquest of Britain",
            "name": "Anderitum",
            "buildings": {
                "town_hall": 1,
                "supply_dump": 1,
                "hunters_lodge": 4,
                "vineyard": 1,
            },
        },
        {
            "campaign": "Conquest of Britain",
            "name": "Anderitum",
            "buildings": {
                "town_hall": 1,
                "temple": 1,
                "supply_dump": 1,
                "large_farm": 2,
                "vineyard": 1,
            },
        },
    ],
    configuration = {
        "storage": {
            "include": False,
        },
        "defenses": {
            "include": False,
        },
    },
)

scenario.display_scenario()
print()
