from typing import Any

from rich.align import Align
from rich.console import Console
from rich.layout import Layout

from modules.building import BuildingsCount
from modules.city import City

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
            city: dict[str, Any],
            buildings: dict[str, Any],
            effects: dict[str, Any],
            production: dict[str, Any],
            storage: dict[str, Any],
            defenses: dict[str, Any],
        ) -> Layout:
        layout: Layout = Layout()
        
        layout.split_row(
            Layout(name = "city_a", ratio = 1),
            Layout(name = "city_b", ratio = 1),
        )
        
        layout["city_a"].update(
            renderable = Align(
                renderable = self.city_a.build_results_display(
                    city = city,
                    buildings = buildings,
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
                    buildings = buildings,
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
            city: dict[str, Any] | None = None,
            buildings: dict[str, Any] | None = None,
            effects: dict[str, Any] | None = None,
            production: dict[str, Any] | None = None,
            storage: dict[str, Any] | None = None,
            defenses: dict[str, Any] | None = None,
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
