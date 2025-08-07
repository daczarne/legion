from modules.scenario import Scenario


Scenario(
    campaign = "Hispania",
    city = "Numantia",
    buildings_a = {
        "city_hall": 1,
        "basilica": 1,
        "miners_guild": 1,
        "large_mine": 6,
    },
    buildings_b = {
        "city_hall": 1,
        "basilica": 1,
        "hidden_grove": 1,
        "large_mine": 6,
    },
).display_results()
