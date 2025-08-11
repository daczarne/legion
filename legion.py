from modules.city import City
from modules.display import CityDisplay
from modules.scenario import Scenario

city: CityDisplay = CityDisplay(
    city = City(
        campaign = "Unification of Italy",
        name = "Caudini",
        buildings = {
            "city_hall": 1,
            "basilica": 1,
            "miners_guild": 1,
            "large_mine": 1,
            "outcrop_mine": 1,
            "farm": 1,
            "lumber_mill": 1,
            "large_fort": 1,
            "stables": 1,
        },
    ),
    configuration = {
        "defenses": {
            "include": True,
        },
    },
)

# city.display_city_results()


scenario: Scenario = Scenario.from_list(
    data = [
        {
            "campaign": "Unification of Italy",
            "name": "Hernici",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "fishing_village": 1,
                "outcrop_mine": 1,
                "miners_guild": 1,
                "large_mine": 4,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Hernici",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "fishing_village": 1,
                "outcrop_mine": 1,
                "large_mine": 5,
            },
        },
    ]
)

scenario.display_scenario_results()
