from modules.city import City, _CityBuldingNode
from modules.building import Building

node: _CityBuldingNode = _CityBuldingNode(
    building = Building(id = "city_hall"),
)


print(node)
