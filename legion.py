from modules.city import BuildingsCount
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


food_producer: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "warehouse": 1,
    "farmers_guild": 1,
    "large_farm": 4,
    "vineyard": 1,
}

ore_producer: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "miners_guild": 1,
    "large_mine": 6,
}

wood_producer: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "warehouse": 1,
    "carpenters_guild": 1,
    "large_lumber_mill": 5,
}

militarty: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "hospital": 1,
    "training_ground": 1,
    "gladiator_school": 1,
    "stables": 1,
    "bordello": 1,
    "quartermaster": 1,
    "large_fort": 1,
}

kingdom: Kingdom = Kingdom.from_list(
    data = [
        {
            "campaign": "Unification of Italy",
            "name": "Roma",
            "buildings": militarty,
        },
        {
            "campaign": "Unification of Italy",
            "name": "Latins",
            "buildings": wood_producer,
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
            "name": "Caere",
            "buildings": wood_producer,
        },
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
            "name": "Anxur",
            "buildings": food_producer,
        },
        {
            "campaign": "Unification of Italy",
            "name": "Aurunci",
            "buildings": ore_producer,
        },
        {
            "campaign": "Unification of Italy",
            "name": "Falerii",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "outcrop_mine": 1,
                "large_mine": 5,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Volsinii",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "carpenters_guild": 1,
                "warehouse": 1,
                "fishing_village": 1,
                "large_lumber_mill": 4,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Populonia",
            "buildings": food_producer,
        },
        {
            "campaign": "Unification of Italy",
            "name": "Spoletium",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 1,
                "large_mine": 5,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Clusium",
            "buildings": ore_producer,
        },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Pisae",
        #     "buildings": wood_producer,
        # },
        {
            "campaign": "Unification of Italy",
            "name": "Sentinum",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "hospital": 1,
                "training_ground": 1,
                "gladiator_school": 1,
                "bordello": 1,
                "quartermaster": 1,
                "large_fort": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Faesula",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "fishing_village": 1,
                "large_mine": 5,
            },
        },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Apuani",
        #     "buildings": wood_producer,
        # },
        {
            "campaign": "Unification of Italy",
            "name": "Friniates",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "large_mine": 5,
                "outcrop_mine": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Sena",
            "buildings": food_producer,
        },
        {
            "campaign": "Unification of Italy",
            "name": "Ariminum",
            "buildings": ore_producer,
        },
        {
            "campaign": "Unification of Italy",
            "name": "Boii",
            "buildings": ore_producer,
        },
        {
            "campaign": "Unification of Italy",
            "name": "Asculum",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "warehouse": 1,
                "carpenters_guild": 1,
                "hidden_grove": 1,
                "large_lumber_mill": 4,
            },
        },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Lingones",
        #     "buildings": wood_producer,
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Marrucini",
        #     "buildings": ore_producer,
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Carsioli",
        #     "buildings": ore_producer,
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Paeligni",
        #     "buildings": food_producer,
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Marsi",
        #     "buildings": {
        #         "city_hall": 1,
        #         "basilica": 1,
        #         "miners_guild": 1,
        #         "large_mine": 5,
        #         "outcrop_mine": 1,
        #     },
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Caercini",
        #     "buildings": {
        #         "city_hall": 1,
        #         "basilica": 1,
        #         "miners_guild": 1,
        #         "outcrop_mine": 1,
        #         "mountain_mine": 1,
        #         "large_mine": 4,
        #     },
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Histonium",
        #     "buildings": {
        #         "city_hall": 1,
        #         "basilica": 1,
        #         "warehouse": 1,
        #         "farmers_guild": 1,
        #         "fishing_village": 1,
        #         "vineyard": 1,
        #         "large_farm": 3,
        #     },
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Apulians",
        #     "buildings": militarty,
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Pentri",
        #     "buildings": ore_producer,
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Neapolis",
        #     "buildings": food_producer,
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Capua",
        #     "buildings": ore_producer,
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Caudini",
        #     "buildings": {
        #         "city_hall": 1,
        #         "basilica": 1,
        #         "miners_guild": 1,
        #         "outcrop_mine": 1,
        #         "large_mine": 5,
        #     },
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Nuceria",
        #     "buildings": {
        #         "city_hall": 1,
        #         "basilica": 1,
        #         "miners_guild": 1,
        #         "fishing_village": 1,
        #         "large_mine": 5,
        #     },
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Hirpini",
        #     "buildings": {
        #         "city_hall": 1,
        #         "basilica": 1,
        #         "miners_guild": 1,
        #         "mountain_mine": 1,
        #         "large_mine": 5,
        #     },
        # },
        # {
        #     "campaign": "Unification of Italy",
        #     "name": "Arpi",
        #     "buildings": wood_producer,
        # },
    ],
)

kingdom.display_kingdom_results()
