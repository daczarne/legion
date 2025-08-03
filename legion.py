from modules.city import City, CityBuildings


scenario: City = City(
    campaign = "Unification of Italy",
    name = "Canusium",
    buildings = CityBuildings(
        buildings = {
            "large_mine": 6,
            "basilica": 1,
            "miners_guild": 1,
        },
    ),
)

scenario.display_results()


scenario: City = City(
    campaign = "Unification of Italy",
    name = "Canusium",
    buildings = CityBuildings(
        buildings = {
            "large_mine": 5,
            "warehouse": 1,
            "basilica": 1,
            "miners_guild": 1,
        },
    ),
)

scenario.display_results()


scenario: City = City(
    campaign = "Unification of Italy",
    name = "Canusium",
    buildings = CityBuildings(
        buildings = {
            "large_mine": 6,
            "warehouse": 1,
            "basilica": 1,
        },
    ),
)

scenario.display_results()
