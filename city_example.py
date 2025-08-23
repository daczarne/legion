from  modules.building import Building
from modules.city import City
from modules.display import CityDisplay

# city: City = City(
#     campaign = "Unification of Italy",
#     name = "Roma",
#     buildings = {
#         "city_hall": 1,
#         "basilica": 1,
#         "farmers_guild": 1,
#         "large_farm": 5,
#         "vineyard": 1,
#     }
# )

city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
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

CityDisplay(city = city).display_city_results()
print()

city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = [
        Building(id = "city_hall"),
        Building(id = "basilica"),
        Building(id = "farmers_guild"),
        Building(id = "vineyard"),
        Building(id = "large_farm"),
        Building(id = "large_farm"),
        Building(id = "large_farm"),
        Building(id = "large_farm"),
        Building(id = "large_farm"),
    ]
)

CityDisplay(city = city).display_city_results()
print()
