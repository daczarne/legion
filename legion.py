from modules.city import City, CityBuildings


scenario_1: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = CityBuildings(
        buildings = {
            "large_farm": 5,
            "vineyard": 1,
            "basilica": 1,
            "farmers_guild": 1,
        },
    ),
)

scenario_1.display_results()


scenario_2: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = CityBuildings(
        buildings = {
            "training_ground": 1,
            "gladiator_school": 1,
            "stables": 1,
            "bordello": 1,
            "basilica": 1,
            "hospital": 1,
            "large_fort": 1,
            "quartermaster": 1,
        },
    ),
)

scenario_2.display_results()
