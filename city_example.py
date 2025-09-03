from modules.building import Building
from modules.city import City


city: City = City.from_buildings_count(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = {
        "city_hall": 1,
    }
)

city.display_city()
