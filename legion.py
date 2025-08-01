from modules.city import City, CityBuildings, ResourcesPotential
from modules.scenario import Scenario


scenario_1: City = City(
    campaign = "Italy",
    name = "Roma",
    resource_potentials = ResourcesPotential(
        food = 125,
        ore = 0,
        wood = 50,
    ),
    buildings = CityBuildings(
        buildings = {
            "farm": 6,
            "basilica": 1,
            "farmers_guild": 1,
        },
    ),
)

scenario_1.display_results(include_city_information=True)

print()
print(scenario_1._calculate_base_production())
print()
print(scenario_1.base_production)
