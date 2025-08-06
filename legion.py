from modules.city import City


scenario = City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "hospital": 1,
        "training_ground": 1,
        "gladiator_school": 1,
        "stables": 1,
        "bordello": 1,
        "quartermaster": 1,
        "large_fort": 1,
    },
)

scenario.display_results()


scenario = City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = {
        "town_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 3,
    },
)

scenario.display_results()
