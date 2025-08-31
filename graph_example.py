from modules.city import City, _CityBuildingNode
from modules.building import Building

node: _CityBuildingNode = _CityBuildingNode(
    building = Building(id = "city_hall"),
)


print(node)
