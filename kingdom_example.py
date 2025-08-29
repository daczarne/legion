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
                "miners_guild": 1,
                "large_mine": 5,
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
            "buildings": ore_producer,
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
            "name": "Aliso",
            "buildings": ore_producer,
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
        {
            "campaign": "Germania",
            "name": "Tuisto",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Marsii",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Tencterii",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Adgandestrius",
            "buildings": military,
        },
        {
            "campaign": "Germania",
            "name": "Atamaci",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Nehalennia",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Gadgaesus",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Bueci",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Dructeri",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Cherusci",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Chasuari",
            "buildings": food_producer,
        },
        {
            "campaign": "Germania",
            "name": "Gambrivi",
            "buildings": food_producer,
        },
        {
            "campaign": "Germania",
            "name": "Chatii",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Radaci",
            "buildings": food_producer,
        },
        {
            "campaign": "Germania",
            "name": "Soci",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Namenones",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Dubraci",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Matagarci",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Brini",
            "buildings": food_producer,
        },
        {
            "campaign": "Germania",
            "name": "Chacirici",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Tuder",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Langobardii",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Matiaci",
            "buildings": food_producer,
        },
        {
            "campaign": "Germania",
            "name": "Nementes",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Sturi",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Salassi",
            "buildings": wood_producer,
        },
        {
            "campaign": "Germania",
            "name": "Sugambrii",
            "buildings": military,
        },
        {
            "campaign": "Germania",
            "name": "Abdagaesus",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Varini",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Libici",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Valeda II",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Osi",
            "buildings": ore_producer,
        },
        {
            "campaign": "Germania",
            "name": "Suebii",
            "buildings": ore_producer,
        },
    ],
)

kingdom.display_kingdom()
