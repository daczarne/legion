from modules.scenario import Scenario


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
            "name": "Roma",
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
            "name": "Roma",
            "buildings": {
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
        },
        {
            "campaign": "Unification of Italy",
            "name": "Caudini",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "large_mine": 1,
                "outcrop_mine": 1,
                "farm": 1,
                "lumber_mill": 1,
                "large_fort": 1,
                "stables": 1,
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

scenario.display_scenario_results()
