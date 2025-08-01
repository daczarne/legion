from modules.city import City, CityBuildings, RssCollection
from modules.scenario import Scenario


scenario_1: City = City(
    campaign = "Italy",
    name = "Roma",
    resource_potentials = RssCollection(
        food = 100,
        ore = 0,
        wood = 50,
    ),
    buildings = CityBuildings(
        buildings = {
            "farm": 5,
            "vineyard": 1,
            "basilica": 1,
            "farmers_guild": 1,
        },
    ),
)

scenario_1.display_results(include_city_information = True)

print()
print(f"Base production: {scenario_1.base_production}")
print(f"Productivity bonuses: {scenario_1.productivity_bonuses}")
print(f"Total production: {scenario_1.total_production}")
print(f"Maintenance costs: {scenario_1.maintenance_costs}")
print()
