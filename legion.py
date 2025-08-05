from modules.city import City, CityBuildings


scenario: City = City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = CityBuildings(
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "hidden_grove": 1,
            "large_mine": 6,
        },
    ),
)

scenario.display_results()


scenario: City = City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = CityBuildings(
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "miners_guild": 1,
            "large_mine": 6,
        },
    ),
)

scenario.display_results()


scenario: City = City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = CityBuildings(
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "hidden_grove": 1,
            "miners_guild": 1,
            "large_mine": 5,
        },
    ),
)

scenario.display_results()
