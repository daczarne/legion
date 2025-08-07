from modules.scenario import Scenario


Scenario(
    campaign = "Unification of Italy",
    city = "Lingones",
    buildings_a = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "forest": 1,
        "large_lumber_mill": 5,
    },
    buildings_b = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 6,
    },
).display_results()
