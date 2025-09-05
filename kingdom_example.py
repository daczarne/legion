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

campaign: str = "Conquest of Britain"

kingdom: Kingdom = Kingdom.from_list(
    data = [
        {
            "campaign": campaign,
            "name": "Anderitum",
            "buildings": {
                "city_hall": 1,
                "supply_dump": 1,
                "basilica": 1,
                "miners_guild": 1,
                "large_mine": 5,
            },
        },
        {
            "campaign": campaign,
            "name": "Noviomagus",
            "buildings": {
                "city_hall": 1,
                "supply_dump": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "vineyard": 1,
                "large_farm": 4,
            },
        },
        {
            "campaign": campaign,
            "name": "Durovern",
            "buildings": wood_producer,
        },
        {
            "campaign": campaign,
            "name": "Durobrivae",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "fishing_village": 1,
                "vineyard": 1,
                "large_farm": 4,
            },
        },
        {
            "campaign": campaign,
            "name": "Yule",
            "buildings": food_producer,
        },
        {
            "campaign": campaign,
            "name": "Calleva",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Venta",
            "buildings": food_producer,
        },
        {
            "campaign": campaign,
            "name": "Sorviodun",
            "buildings": food_producer,
        },
        {
            "campaign": campaign,
            "name": "Maidun",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Londun",
            "buildings": food_producer,
        },
        {
            "campaign": campaign,
            "name": "Ischalis",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Lindinis",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Isca",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Tamara",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "outcrop_mine": 1,
                "large_mine": 5,
            },
        },
        {
            "campaign": campaign,
            "name": "Uxella",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 1,
                "large_mine": 5,
            },
        },
        {
            "campaign": campaign,
            "name": "Durocornovion",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Dor",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Bagendun",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Verulam",
            "buildings": wood_producer,
        },
        {
            "campaign": campaign,
            "name": "Vertis",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Alauna",
            "buildings": military,
        },
        {
            "campaign": campaign,
            "name": "Duroliponte",
            "buildings": wood_producer,
        },
        {
            "campaign": campaign,
            "name": "Camulodun",
            "buildings": food_producer,
        },
    ],
)

kingdom.display_kingdom()
