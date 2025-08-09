from rich.align import Align
from rich.console import Console
from rich.layout import Layout

from .building import BuildingsCount
from .city import City
from .display import DisplayConfiguration

class Scenario:
    def __init__(
            self,
            campaign: str,
            city: str,
            buildings_a: BuildingsCount,
            buildings_b: BuildingsCount,
        ) -> None:
        self.campaign: str = campaign
        self.city: str = city
        self.buildings_a: BuildingsCount = buildings_a
        self.buildings_b: BuildingsCount = buildings_b
        
        self.city_a: City = City(
            campaign = self.campaign,
            name = self.city,
            buildings = self.buildings_a,
        )
        
        self.city_b: City = City(
            campaign = self.campaign,
            name = self.city,
            buildings = self.buildings_b,
        )
    
    def _build_results_display(
            self,
            city: DisplayConfiguration,
            buildings: DisplayConfiguration,
            effects: DisplayConfiguration,
            production: DisplayConfiguration,
            storage: DisplayConfiguration,
            defenses: DisplayConfiguration,
        ) -> Layout:
        layout: Layout = Layout()
        
        layout.split_row(
            Layout(name = "city_a", ratio = 1),
            Layout(name = "city_b", ratio = 1),
        )
        
        include_buildings: bool = buildings.get("include", True)
        buildings_height_city_a: int = len(self.city_a.buildings) + 2 if include_buildings else 0
        buildings_height_city_b: int = len(self.city_b.buildings) + 2 if include_buildings else 0
        buildings_height: int = max(buildings_height_city_a, buildings_height_city_b)
        
        layout["city_a"].update(
            renderable = Align(
                renderable = self.city_a.build_results_display(
                    city = city,
                    buildings = {**buildings, "height": buildings_height},
                    effects = effects,
                    production = production,
                    storage = storage,
                    defenses = defenses,
                ),
                align = "center",
            ),
        )
        
        layout["city_b"].update(
            renderable = Align(
                renderable = self.city_b.build_results_display(
                    city = city,
                    buildings = {**buildings, "height": buildings_height},
                    effects = effects,
                    production = production,
                    storage = storage,
                    defenses = defenses,
                ),
                align = "center",
            ),
        )
        
        return layout
    
    def display_results(
            self,
            city: DisplayConfiguration | None = None,
            buildings: DisplayConfiguration | None = None,
            effects: DisplayConfiguration | None = None,
            production: DisplayConfiguration | None = None,
            storage: DisplayConfiguration | None = None,
            defenses: DisplayConfiguration | None = None,
        ) -> None:
        console: Console = Console()
        console.print(
            self._build_results_display(
                city = city if city else {"include": False},
                buildings = buildings if buildings else {},
                effects = effects if effects else {},
                production = production if production else {},
                storage = storage if storage else {},
                defenses = defenses if defenses else {},
            ),
        )
