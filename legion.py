from modules.city import City, CityBuildings


City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = CityBuildings(
        city_hall = 1,
        basilica = 1,
        hidden_grove = 1,
        large_mine = 6,
    ),
).display_results()


City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = CityBuildings(
        city_hall = 1,
        basilica = 1,
        miners_guild = 1,
        large_mine = 6,
    ),
).display_results()
