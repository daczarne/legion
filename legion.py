from modules.city import City


scenario = City(
    campaign = "Unification of Italy",
    name = "Lingones",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "forest": 1,
        "large_lumber_mill": 5,
    },
)

scenario.display_results()


scenario = City(
    campaign = "Unification of Italy",
    name = "Lingones",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 6,
    },
)

scenario.display_results()
