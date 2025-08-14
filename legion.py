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

display_configuration: DisplayConfiguration = {
    "production": {
        "color": "yellow"
    },
    "defenses": {
        "include": False,
    },
}

CityDisplay(city = city, configuration = display_configuration).display_city_results()
