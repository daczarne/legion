from modules.city import City, _CityBuildingsGraph
from modules.building import Building

city: City = City(
    campaign = "Hispania",
    name = "Biskargis",
    buildings = [
        Building(id = "town_hall"),
        Building(id = "training_ground"),
    ]
)
graph: _CityBuildingsGraph = _CityBuildingsGraph(city = city)

for building in city.buildings:
    graph.traverse_and_add(building_id = building.id)
    print(f"Graph: {graph.nodes[building.id]}")

print()
print(graph.nodes["town_hall"])
