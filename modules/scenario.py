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
    
    def _build_results_display(self) -> Layout:
        layout: Layout = Layout()
        
        layout.split_row(
            Layout(name = "city_a", ratio = 1),
            Layout(name = "city_b", ratio = 1),
        )
        
        layout["city_a"].update(
            renderable = Align(
                renderable = self.city_a.build_results_display(
                    include_city = False,
                    include_production = True,
                    include_storage = True,
                    include_defenses = True,
                ),
                align = "center"
            ),
        )
        
        layout["city_b"].update(
            renderable = Align(
                renderable = self.city_b.build_results_display(
                    include_city = False,
                    include_production = True,
                    include_storage = True,
                    include_defenses = False,
                ),
                align = "center"
            ),
        )
        
        return layout
        # return Panel(
        #     renderable = layout,
        #     height = 39,
        #     box = box.HEAVY_EDGE,
        # )
    
    def display_results(self) -> None:
        console: Console = Console()
        console.print(self._build_results_display())
