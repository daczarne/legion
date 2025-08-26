from modules.building import Building
from modules.city import City


city: City = City.from_buildings_count(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "farmers_guild": 1,
        "large_farm": 5,
        "vineyard": 1,
    }
)

city.display_city()

print()

city: City = City(
    campaign = "Unification of Italy",
    name = "Anxur",
    buildings = [
        Building(id = "city_hall"),
        Building(id = "basilica"),
        Building(id = "hospital"),
        Building(id = "training_ground"),
        Building(id = "gladiator_school"),
        Building(id = "stables"),
        Building(id = "bordello"),
        Building(id = "quartermaster"),
        Building(id = "large_fort"),
    ]
)

city.display_city()

print()

city: City = City.from_buildings_count(
    campaign = "Conquest of Britain",
    name = "Anderitum",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "supply_dump": 1,
        "farmers_guild": 1,
        "vineyard": 1,
        "large_farm": 4,
    },
)

city.display_city()

print()

city: City = City.from_buildings_count(
    campaign = "Germania",
    name = "Rogomagnum",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "hospital": 1,
        "training_ground": 1,
        "gladiator_school": 1,
        "supply_dump": 1,
        "bordello": 1,
        "quartermaster": 1,
        "large_fort": 1,
    },
)

city.display_city()
