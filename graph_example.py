from modules.city import City, _CityBuildingNode, _CityBuildingsGraph
from modules.building import Building, _BUILDINGS

city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = [
        Building(id = "village_hall"),
    ]
)

graph: _CityBuildingsGraph = _CityBuildingsGraph(city = city)
print(graph.city)
# print(graph.city.buildings)
for node_name, node in graph.nodes.items():
    print(node)
