from modules.city import City, CityBuildings, RssCollection


scenario_1: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    resource_potentials = RssCollection(
        food = 100,
        ore = 80,
        wood = 0,
    ),
    buildings = CityBuildings(
        buildings = {
            "mine": 5,
            "outcrop_mine": 1,
            "basilica": 1,
            "miners_guild": 1,
        },
    ),
)

scenario_1.display_results()


scenario_2: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    resource_potentials = RssCollection(
        food = 100,
        ore = 80,
        wood = 0,
    ),
    buildings = CityBuildings(
        buildings = {
            "farm": 4,
            "vineyard": 1,
            "outcrop_mine": 1,
            "basilica": 1,
            "farmers_guild": 1,
        },
    ),
)

scenario_2.display_results()
