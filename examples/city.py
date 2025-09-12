from modules.building import Building, BuildingsCount
from modules.city import City


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

city: City = City.from_buildings_count(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = military,
    staffing_strategy = "effects_first",
)

city.display_city()
print()

food_producer: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "farmers_guild": 1,
    "vineyard": 1,
    "large_farm": 5,
}

city: City = City.from_buildings_count(
    campaign = "Unification of Italy",
    name = "Populonia",
    buildings = food_producer,
    staffing_strategy = "production_first",
)

city.display_city()
print()

city: City = City.from_buildings_count(
    campaign = "Conquest of Britain",
    name = "Moridun",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "miners_guild": 1,
        "mountain_mine": 1,
        "large_mine": 5,
    },
    staffing_strategy = "production_first",
)

city.display_city()
print()

city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = [
        Building(id = "city_hall", workers = 0),
        Building(id = "basilica", workers = 1),
        Building(id = "vineyard", workers = 3),
        Building(id = "large_farm", workers = 3),
        Building(id = "large_farm", workers = 0),
        Building(id = "large_farm", workers = 0),
        Building(id = "large_farm", workers = 0),
        Building(id = "large_farm", workers = 0),
        Building(id = "large_farm", workers = 0),
    ],
    staffing_strategy = "production_first",
)

city.display_city(
    configuration = {
        "storage": {"include": False},
        "defenses": {"include": False},
    }
)

for building in city.buildings:
    print(f"{building.name} - {building.workers} of {building.max_workers}")

print("-" * 25)
print(f"Available workers: {city.available_workers}")
print(f"Assigned workers: {city.assigned_workers}")
