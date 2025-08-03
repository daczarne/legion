from modules.city import City, CityBuildings


scenario: City = City(
    campaign = "Unification of Italy",
    name = "Canusium",
    buildings = CityBuildings(
        buildings = {
            "large_farm": 5,
            "vineyard": 1,
            "village_hall": 1,
            "farmers_guild": 1,
            # "miners_guild": 1,
        },
    ),
)

scenario.display_results()
