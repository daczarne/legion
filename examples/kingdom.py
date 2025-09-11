from modules.building import BuildingsCount
from modules.kingdom import Kingdom


campaign: str = "Hispania"

food_producer: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "farmers_guild": 1,
    "vineyard": 1,
    "large_farm": 5,
}

food_producer_with_warehouse: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "farmers_guild": 1,
    "warehouse": 1,
    "vineyard": 1,
    "large_farm": 4,
}

ore_producer: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "miners_guild": 1,
    "large_mine": 6,
}

ore_producer_with_outcrop_mine: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "miners_guild": 1,
    "outcrop_mine": 1,
    "large_mine": 5,
}

ore_producer_with_mountain_mine: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "miners_guild": 1,
    "mountain_mine": 1,
    "large_mine": 5,
}

wood_producer: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "carpenters_guild": 1,
    "large_lumber_mill": 6,
}

wood_producer_with_warehouse: BuildingsCount = {
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
            "campaign": campaign,
            "name": "Biskargis",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Dertosa",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Tarrako",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Ilerda",
            "buildings": ore_producer_with_mountain_mine,
        },
        {
            "campaign": campaign,
            "name": "Oska",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Tolosa",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Vokata",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Tarbelles",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Ilumberis",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Torbelia",
            "buildings": ore_producer_with_outcrop_mine,
        },
        {
            "campaign": campaign,
            "name": "Oiasson",
            "buildings": ore_producer_with_outcrop_mine,
        },
        {
            "campaign": campaign,
            "name": "Blendion",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Diobriga",
            "buildings": ore_producer_with_mountain_mine,
        },
        {
            "campaign": campaign,
            "name": "Kontrebia",
            "buildings": food_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Segontia",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Kalagurris",
            "buildings": wood_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Karaka",
            "buildings": military,
        },
        {
            "campaign": campaign,
            "name": "Numantia",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Uxama",
            "buildings": ore_producer_with_mountain_mine,
        },
        {
            "campaign": campaign,
            "name": "Pallantia",
            "buildings": wood_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Kamarika",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Noega",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Kauka",
            "buildings": military,
        },
        {
            "campaign": campaign,
            "name": "Segovia",
            "buildings": ore_producer_with_outcrop_mine,
        },
        {
            "campaign": campaign,
            "name": "Toleton",
            "buildings": food_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Arbokala",
            "buildings": wood_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Argentiola",
            "buildings": ore_producer_with_mountain_mine,
        },
        {
            "campaign": campaign,
            "name": "Asturika",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Salmantika",
            "buildings": ore_producer_with_mountain_mine,
        },
        {
            "campaign": campaign,
            "name": "Karanikon",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Brigantion",
            "buildings": food_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Bergidon",
            "buildings": wood_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Kaliabriga",
            "buildings": ore_producer_with_outcrop_mine,
        },
        {
            "campaign": campaign,
            "name": "Brakara",
            "buildings": wood_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Aiminion",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Konsabura",
            "buildings": food_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Osikerda",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Arsa",
            "buildings": food_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Salika",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Igaiditania",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Turmogon",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "fishing_village": 1,
                "large_mine": 5,
            },
        },
        {
            "campaign": campaign,
            "name": "Ammaia",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Skallabis",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Libora",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Ebora",
            "buildings": wood_producer_with_warehouse,
        },
        {
            "campaign": campaign,
            "name": "Myrtilis",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Oreton",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Kaspiana",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Mirobriga",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Nertobriga",
            "buildings": military,
        },
        {
            "campaign": campaign,
            "name": "Helike",
            "buildings": ore_producer,
        },
        {
            "campaign": campaign,
            "name": "Ilorki",
            "buildings": ore_producer_with_mountain_mine,
        },
    ],
)

kingdom.display_kingdom()
