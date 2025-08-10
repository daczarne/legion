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
    
    def _build_scenario_display(
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
        
        layout["city_a"].update(
            renderable = Align(
                renderable = self.city_a.build_city_display(
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
                renderable = self.city_b.build_city_display(
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
    
    def display_scenario_results(
            self,
            city: DisplayConfiguration | None = None,
            buildings: DisplayConfiguration | None = None,
            effects: DisplayConfiguration | None = None,
            production: DisplayConfiguration | None = None,
            storage: DisplayConfiguration | None = None,
            defenses: DisplayConfiguration | None = None,
        ) -> None:
        _city: DisplayConfiguration = city if city else {"include": True}
        _buildings: DisplayConfiguration = buildings if buildings else {"include": True}
        _effects: DisplayConfiguration = effects if effects else {"include": True}
        _production: DisplayConfiguration = production if production else {"include": True}
        _storage: DisplayConfiguration = storage if storage else {"include": True}
        _defenses: DisplayConfiguration = defenses if defenses else {"include": True}
        
        #* Include booleans
        include_city: bool = _city.get("include", True)
        include_buildings: bool = _buildings.get("include", True)
        include_effects: bool = _effects.get("include", True)
        include_production: bool = _production.get("include", True)
        include_storage: bool = _storage.get("include", True)
        include_defenses: bool = _defenses.get("include", True)
        
        #* Height calculations
        header_height: int = 2 if include_city else 0
        
        # A city can have a maximum of 9 buildings (len(self.buildings) = 9). The table needs two more rows for the
        # title (Buildings) and the space after the title. But if the city has less than 6 different buildings, the
        # space assigned for Buildings and Effects needs to be the height needed for the effects table (8).
        buildings_height_city_a: int = len(self.city_a.buildings) + 2 if include_buildings else 0
        buildings_height_city_b: int = len(self.city_b.buildings) + 2 if include_buildings else 0
        buildings_height: int = max(buildings_height_city_a, buildings_height_city_b)
        effects_height: int = 8 if include_effects else 0
        buildings_and_effects_height: int = max(buildings_height, effects_height)
        
        production_height: int = 8 if include_production else 0
        storage_height: int = 8 if include_storage else 0
        defenses_height: int = 6 if include_defenses else 0
        
        main_height: int = buildings_and_effects_height + production_height + storage_height + defenses_height
        
        total_height: int = (
            header_height
            + main_height
            + 2
        )
        total_width: int = 192
        
        console: Console = Console(height = total_height, width = total_width)
        console.print(
            self._build_scenario_display(
                city = {**_city, "height": header_height},
                buildings = {**_buildings, "height": buildings_height},
                effects = {**_effects, "height": effects_height},
                production = {**_production, "height": production_height},
                storage = {**_storage, "height": storage_height},
                defenses = {**_defenses, "height": defenses_height},
            ),
        )
