from modules.building import BuildingsCount
from modules.kingdom import Kingdom


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

military: BuildingsCount = {
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
            "campaign": "Germania",
            "name": "Novesium",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Rogomagnum",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "vineyard": 1,
                "large_farm": 4,
                "supply_dump": 1,
            },
        },
        {
            "campaign": "Germania",
            "name": "Peucini",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Oxiones",
            "buildings": military,
        },
        {
            "campaign": "Germania",
            "name": "Suarines",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Valeda",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Nerthus",
            "buildings": food_producer,
        },
        {
            "campaign": "Germania",
            "name": "Naristi",
            "buildings": food_producer,
        },
        {
            "campaign": "Germania",
            "name": "Tanfana",
            "buildings": ore_producer,
        },
    ],
)

kingdom.display_kingdom()
