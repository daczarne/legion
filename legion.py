from modules.display import CityDisplay, DisplayConfiguration
from modules.city import City

city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "farmers_guild": 1,
        "large_farm": 5,
        "vineyard": 1,
    },
)

CityDisplay(city = city).display_city_results()
