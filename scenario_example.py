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
            "name": "Caercini",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 1,
                "outcrop_mine": 1,
                "large_mine": 4,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Caercini",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "mountain_mine": 1,
                "outcrop_mine": 1,
                "large_mine": 5,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Caercini",
            "buildings": {
                "city_hall": 1,
                "miners_guild": 1,
                "mountain_mine": 1,
                "outcrop_mine": 1,
                "large_mine": 5,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Caercini",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 1,
                "outcrop_mine": 1,
                "large_mine": 3,
                "vineyard": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Caercini",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 1,
                "outcrop_mine": 1,
                "large_mine": 2,
                "vineyard": 1,
                "gladiator_school": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Caercini",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 1,
                "outcrop_mine": 1,
                "large_mine": 1,
                "vineyard": 1,
                "gladiator_school": 1,
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
            "name": "Latins",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "carpenters_guild": 1,
                "large_lumber_mill": 6,
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
                "large_lumber_mill": 4,
                "vineyard": 1,
                "gladiator_school": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Latins",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "carpenters_guild": 1,
                "large_lumber_mill": 3,
                "vineyard": 1,
                "gladiator_school": 1,
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
