from modules.city import City
from modules.building import BuildingsCount, Building

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

food_producer: BuildingsCount = {
    "city_hall": 1,
    "basilica": 1,
    "farmers_guild": 1,
    "large_farm": 5,
    "vineyard": 1,
}

city: City = City.from_buildings_count(
    campaign = "Unification of Italy",
    name = "Populonia",
    buildings = food_producer,
    staffing_strategy = "effects_first",
)

city.display_city()


user_selected_strategy: str = "production"

#################################
#################################
#################################


for building in city.buildings:
    print(f"{building.name} - Workers: {building.workers} of {building.max_workers}")

print("-" * 40)
print(f"Total workers: {city.assigned_workers} of {city.available_workers}")
