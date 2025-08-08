from rich.align import Align
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

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
            include_city: bool = False,
            include_buildings: bool = True,
            include_effects: bool = True,
            include_production: bool = True,
            include_storage: bool = True,
            include_defenses: bool = True,
        ) -> Layout:
        layout: Layout = Layout()
        
        layout.split_row(
            Layout(name = "city_a", ratio = 1),
            Layout(name = "city_b", ratio = 1),
        )
        
        layout["city_a"].update(
            renderable = Align(
                renderable = self.city_a.build_results_display(
                    include_city = include_city,
                    include_buildings = include_buildings,
                    include_effects = include_effects,
                    include_production = include_production,
                    include_storage = include_storage,
                    include_defenses = include_defenses,
                ),
                align = "center",
            ),
        )
        
        layout["city_b"].update(
            renderable = Align(
                renderable = self.city_b.build_results_display(
                    include_city = include_city,
                    include_buildings = include_buildings,
                    include_effects = include_effects,
                    include_production = include_production,
                    include_storage = include_storage,
                    include_defenses = include_defenses,
                ),
                align = "center",
            ),
        )
        
        return layout
    
    def display_results(
            self,
            include_city: bool = False,
            include_buildings: bool = True,
            include_effects: bool = True,
            include_production: bool = True,
            include_storage: bool = True,
            include_defenses: bool = True,
        ) -> None:
        console: Console = Console()
        console.print(
            self._build_results_display(
                include_city = include_city,
                include_buildings = include_buildings,
                include_effects = include_effects,
                include_production = include_production,
                include_storage = include_storage,
                include_defenses = include_defenses,
            ),
        )
