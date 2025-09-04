"""
Module for defining game buildings.

This module loads building definitions from a YAML file and provides typed access to their properties. It exposes the
public API for working with buildings in a city, including building instances, their attributes, and worker assignments.

Public API:
- BuildingsCount (TypeAlias): Mapping of building identifiers to their counts in a city. Keys are building IDs (e.g.,
    "farm", "mine"), values are integers representing how many of that building should be created in the city.
- Building (dataclass): Represents a specific building instance, with runtime attributes such as costs, bonuses,
    storage capacity, worker assignment, and construction requirements.

Internal objects (not part of the public API):
- _BUILDINGS: Dictionary of all building definitions loaded from `./data/buildings.yaml`.
- _BuildingData (TypedDict): Helper for type annotations when reading building data from YAML/JSON files.
"""

import yaml

from dataclasses import dataclass, field
from typing import ClassVar, Literal, TypeAlias, TypedDict

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from .effects import EffectBonusesData, EffectBonuses
from .exceptions import (
    InsufficientNumberOfWorkersError,
    NegativeNumberOfWorkersError,
    TooManyWorkersError,
    UnknownBuildingError,
)
from .geo_features import GeoFeature
from .resources import Resource, ResourceCollectionData, ResourceCollection


__all__: list[str] = ["BuildingsCount", "Building"]


"""
Mapping of building identifiers to their counts in a city.

Keys are building IDs (e.g., "farm", "mine"). Values are integers representing how many of that building exist.
"""
BuildingsCount: TypeAlias = dict[str, int]


# * ************** * #
# * BUILDINGS DATA * #
# * ************** * #

class _BuildingData(TypedDict):
    """
    This is a helper class meant to be used when reading building data from YAML or JSON files. Its only purpose is to
    provide good type annotations and hints.
    """
    id: str
    name: str
    building_cost: ResourceCollectionData
    maintenance_cost: ResourceCollectionData
    productivity_bonuses: ResourceCollectionData
    productivity_per_worker: ResourceCollectionData
    effect_bonuses: EffectBonusesData
    effect_bonuses_per_worker: EffectBonusesData
    storage_capacity: ResourceCollectionData
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: str | None
    required_rss: list[str]
    required_building: list[str]
    replaces: str | None

with open(file = "./data/buildings.yaml", mode = "r") as file:
    _buildings_data: dict[Literal["buildings"], list[_BuildingData]] = yaml.safe_load(stream = file)

_BUILDINGS: dict[str, _BuildingData] = {building["id"]: building for building in _buildings_data["buildings"]}


# * ******** * #
# * BUILDING * #
# * ******** * #

@dataclass(match_args = False, kw_only = True)
class Building:
    """
    Represents a building in the game.
    
    To create a building simply supply the building identifier for the desired building. The class will look-up all
    other properties for the building such as costs, bonuses, worker capacity, and requirements. Buildings may depend
    on other buildings, resources, or geographic features to be constructed. They can also replace other buildings when
    built (for example, the Temple replaces the Shrine).
    
    If a nonexistent building ID is supplied and exception will be raised.
    
    Attributes:
        id (str): Unique identifier of the building. This is unique amongst all buildings, not amongst all building
            instances in a city. For example, if 2 Farms are built in a city, both of them will have `id = "farm"`.
        workers (int): Current number of assigned workers.
        name (str): Display name of the building.
        building_cost (ResourceCollection): Resources required to build.
        maintenance_cost (ResourceCollection): Ongoing resource costs.
        productivity_bonuses (ResourceCollection): Productivity bonuses gained by having this building in the city.
        productivity_per_worker (ResourceCollection): Productivity per worker. Only relevant for resource-producing
            buildings.
        effect_bonuses (EffectBonuses): Effect bonuses produced by having the building in the city. There are three
            bonuses in the game
                - Troop training: the experience new troops have when trained in the city.
                - Population growth: multipliers for how fast the population grows.
                - Intelligence: spying ability.
        effect_bonuses_per_worker (EffectBonuses): Effect bonuses produced by staffing the buildings of the city. For
            example, having a Basilica given +50 Population growth if the Basilica is staffed.
        storage_capacity (ResourceCollection): Storage space provided by the building.
        max_workers (int): Maximum assignable workers.
        is_buildable (bool): Whether the building can be constructed. Some buildings, e.g. Supply dump, cannot be built
            by the player. THey are either present in the city at the start or they are not.
        is_deletable (bool): Whether the building can be removed. Some buildings cannot be removed once built. For
            example, halls, mountain mines, fishing villages, etc.
        is_upgradeable (bool): Whether the building can be upgraded.
        required_geo (GeoFeature | None): Required geographic feature, if any. For example, building a Mountain mine
            requires that the city where it is being built has a mountain.
        required_rss list[Resource]: Required resource, if any. For example, building Farms requires that the city
            has production potential for food production.
        required_building (list[str]): List of possible pre-requisite buildings (OR condition).
        replaces (str | None): Identifier of the building this one replaces.
    """
    id: str = field(init = True, repr = True, compare = True, hash = True)
    workers: int = field(init = True, default = 0, repr = False, compare = False, hash = False)
    
    name: str = field(init = False, repr = False, compare = False, hash = False)
    building_cost: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    maintenance_cost: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    productivity_bonuses: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    productivity_per_worker: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    effect_bonuses: EffectBonuses = field(init = False, repr = False, compare = False, hash = False)
    effect_bonuses_per_worker: EffectBonuses = field(init = False, repr = False, compare = False, hash = False)
    storage_capacity: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    max_workers: int = field(init = False, repr = False, compare = False, hash = False)
    is_buildable: bool = field(init = False, repr = False, compare = False, hash = False)
    is_deletable: bool = field(init = False, repr = False, compare = False, hash = False)
    is_upgradeable: bool = field(init = False, repr = False, compare = False, hash = False)
    required_geo: GeoFeature | None = field(init = False, default = None, repr = False, compare = False, hash = False)
    required_rss: list[Resource] = field(init = False, default_factory = list, repr = False, compare = False, hash = False)
    # Dependencies here need to be interpreted as an OR. Either of the listed buildings unblocks the building. For
    # example, a Stable requires either a Farm, or a Large Farm, or a Vineyard, or a Fishing Village. If the city has
    # any one for them it can build a Stable. Similarly, a Blacksmith requires either a Mine, or a Large Mine, or a
    # Mountain Mine, or an Outcrop Mine. If a building has no dependencies the list will be empty.
    required_building: list[tuple[str, ...]] = field(init = False, default_factory = list, repr = False, compare = False, hash = False)
    replaces: str | None = field(init = False, default = None, repr = False, compare = False, hash = False)
    
    
    __match_args__: ClassVar[str] = ("id")
    
    
    def _validate_building_exists(self) -> None:
        if self.id not in _BUILDINGS:
            raise UnknownBuildingError(f"Building {self.id} does not exist.")
    
    def _validate_initial_number_of_workers(self) -> None:
        if self.workers > self.max_workers:
            raise TooManyWorkersError(f"Too many workers. Max is {self.max_workers} for {self.name}.")
    
    def _unpack_required_buildings(self) -> list[tuple[str, ...]]:
        required_buildings_list_of_strings: list[str] = _BUILDINGS[self.id]["required_building"]
        required_buildings: list[tuple[str, ...]] = []
        
        for requirement in required_buildings_list_of_strings:
            required_buildings.append(tuple(requirement.split(sep = ", ")))
        
        return required_buildings
    
    
    def __post_init__(self) -> None:
        self._validate_building_exists()
        
        self.name = _BUILDINGS[self.id]["name"]
        self.building_cost = ResourceCollection(**_BUILDINGS[self.id]["building_cost"])
        self.maintenance_cost = ResourceCollection(**_BUILDINGS[self.id]["maintenance_cost"])
        self.productivity_bonuses = ResourceCollection(**_BUILDINGS[self.id]["productivity_bonuses"])
        self.productivity_per_worker = ResourceCollection(**_BUILDINGS[self.id]["productivity_per_worker"])
        self.effect_bonuses = EffectBonuses(**_BUILDINGS[self.id]["effect_bonuses"])
        self.effect_bonuses_per_worker = EffectBonuses(**_BUILDINGS[self.id]["effect_bonuses_per_worker"])
        self.storage_capacity = ResourceCollection(**_BUILDINGS[self.id]["storage_capacity"])
        self.max_workers = _BUILDINGS[self.id]["max_workers"]
        self.is_buildable = _BUILDINGS[self.id]["is_buildable"]
        self.is_deletable = _BUILDINGS[self.id]["is_deletable"]
        self.is_upgradeable = _BUILDINGS[self.id]["is_upgradeable"]
        self.required_geo = GeoFeature(value = _BUILDINGS[self.id]["required_geo"]) if _BUILDINGS[self.id]["required_geo"] else None
        self.required_rss = [Resource(value = rss) for rss in _BUILDINGS[self.id]["required_rss"]]
        self.required_building = self._unpack_required_buildings()
        self.replaces = _BUILDINGS[self.id]["replaces"]
        
        self._validate_initial_number_of_workers()
    
    
    def add_workers(self, qty: int) -> None:
        """
        Assigns additional workers to the building.
        
        Args:
            qty (int): Number of workers to add.
        
        Raises:
            TooManyWorkersError: If the new total (current + the qty to be added) exceeds the maximum worker capacity.
            NegativeNumberOfWorkersError: If the supplied quantity (`qty`) is negative.
        """
        if qty < 0:
            raise NegativeNumberOfWorkersError("Cannot add a negative number of workers.")
        
        if self.workers + qty > self.max_workers:
            raise TooManyWorkersError(f"Too many workers. Max is {self.max_workers} for {self.name}.")
        
        self.workers += qty
    
    def remove_workers(self, qty: int) -> None:
        """
        Removes workers from the building.
        
        Args:
            qty (int): Number of workers to remove.
        
        Raises:
            InsufficientNumberOfWorkersError: If the operation results in fewer than zero workers.
            NegativeNumberOfWorkersError: If the supplied quantity (`qty`) is negative.
        """
        if qty < 0:
            raise NegativeNumberOfWorkersError("Cannot remove a negative number of workers.")
        
        if self.workers - qty < 0:
            raise InsufficientNumberOfWorkersError(f"Can not remove {qty} workers. Building currently has {self.workers}.")
        
        self.workers -= qty
    
    def set_workers(self, qty: int) -> None:
        """
        Sets the exact number of workers for the building.
        
        Args:
            qty (int): Number of workers to assign.
        
        Raises:
            TooManyWorkersError: If the value exceeds the maximum number of workers the building can have.
            NegativeNumberOfWorkersError: If the supplied quantity (`qty`) is negative.
        """
        if qty < 0:
            raise NegativeNumberOfWorkersError("Cannot set a negative number of workers.")
        
        if qty > self.max_workers:
            raise TooManyWorkersError(f"{self.name} cannot allocate {qty} workers. Max is {self.max_workers}.")
        
        self.workers = qty
    
    
    #* Formatters
    @staticmethod
    def _format_building(text: str) -> str:
        return f"[italic bold bright_cyan]Building[/italic bold bright_cyan](" \
            f"[italic dim]id = [/italic dim][yellow]\"{text}\"[/yellow])"
    
    @staticmethod
    def _format_string(text: str) -> str:
        return f"[yellow]{text}[/yellow]"
    
    @staticmethod
    def _format_rss(text: str) -> str:
        return f"[italic bold bright_cyan]Resource[/italic bold bright_cyan].{text}"
    
    @staticmethod
    def _format_geo(text: str) -> str:
        return f"[italic bold bright_cyan]GeoFeature[/italic bold bright_cyan].{text}"
    
    @staticmethod
    def _format_resource_collection(collection: ResourceCollection) -> str:
        text: str = f"[italic bold bright_cyan]ResourceCollection[/italic bold bright_cyan](" \
            f"[italic dim]food = [/italic dim]{collection.food}, " \
            f"[italic dim]ore = [/italic dim]{collection.ore}, " \
            f"[italic dim]wood = [/italic dim]{collection.wood}" \
            f")"
        return text
    
    @staticmethod
    def _format_effect_bonuses(bonuses: EffectBonuses) -> str:
        text: str = f"[italic bold bright_cyan]EffectBonuses[/italic bold bright_cyan](" \
            f"[italic dim]troop_training = [/italic dim]{bonuses.troop_training}, " \
            f"[italic dim]population_growth = [/italic dim]{bonuses.population_growth}, " \
            f"[italic dim]intelligence = [/italic dim]{bonuses.intelligence}" \
            f")"
        return text
    
    @staticmethod
    def _format_scalar(scalar: int | float | bool) -> str:
        return f"[dark_magenta]{scalar}[/dark_magenta]"
    
    @staticmethod
    def _format_none() -> str:
        return f"[italic dim dark_magenta]None[/italic dim dark_magenta]"
    
    
    #* Display building
    def _building_information(self) -> Text:
        text: Text = Text(
            text = f" Building(id = \"{self.id}\") ",
            style = "bold black on white",
            justify = "center",
        )
        return text
    
    def _building_name(self) -> str:
        return f"[bold]Name:[/bold] {Building._format_string(text = self.name)}"
    
    def _building_building_costs(self) -> str:
        return f"[bold]Building costs:[/bold] " \
            f"{Building._format_resource_collection(collection = self.building_cost)}"
    
    def _building_maintenance_costs(self) -> str:
        return f"[bold]Maintenance costs:[/bold] " \
            f"{Building._format_resource_collection(collection = self.maintenance_cost)}"
    
    def _building_productivity_bonuses(self) -> str:
        return f"[bold]Productivity bonuses:[/bold] " \
            f"{Building._format_resource_collection(collection = self.productivity_bonuses)}"
    
    def _building_productivity_per_worker(self) -> str:
        return f"[bold]Productivity per worker:[/bold] " \
            f"{Building._format_resource_collection(collection = self.productivity_per_worker)}"
    
    def _building_effect_bonuses(self) -> str:
        return f"[bold]Effect bonuses:[/bold] " \
            f"{Building._format_effect_bonuses(self.effect_bonuses)}"
    
    def _building_effect_bonuses_per_worker(self) -> str:
        return f"[bold]Effect bonuses per worker:[/bold] " \
            f"{Building._format_effect_bonuses(self.effect_bonuses_per_worker)}"
    
    def _building_storage_capacity(self) -> str:
        return f"[bold]Storage capacity:[/bold] " \
            f"{Building._format_resource_collection(collection = self.storage_capacity)}"
    
    def _building_max_workers(self) -> str:
        return f"[bold]Max. workers:[/bold] {Building._format_scalar(scalar = self.max_workers)}"
    
    def _building_current_workers(self) -> str:
        return f"[bold]Current workers:[/bold] {Building._format_scalar(scalar = self.workers)}"
    
    def _building_is_buildable(self) -> str:
        return f"[bold]Is buildable:[/bold] {Building._format_scalar(scalar = self.is_buildable)}"
    
    def _building_is_deletable(self) -> str:
        return f"[bold]Is deletable:[/bold] {Building._format_scalar(scalar = self.is_deletable)}"
    
    def _building_is_upgradeable(self) -> str:
        return f"[bold]Is upgradeable:[/bold] {Building._format_scalar(scalar = self.is_upgradeable)}"
    
    def _building_required_geo(self) -> str:
        text: str = f"[bold]Required geo. feature:[/bold] "
        
        if self.required_geo:
            text += f"{Building._format_geo(self.required_geo.name)}"
        else:
            text += Building._format_none()
        
        return text
    
    def _building_required_rss(self) -> str:
        text: str = f"[bold]Required resource:[/bold] "
        
        if len(self.required_rss) == 0:
            return text + Building._format_none()
        
        lines: list[str] = []
        
        for idx, rss in enumerate(self.required_rss):
            transformed: str = Building._format_rss(text = rss.name)
            line: str = transformed if idx == 0 else f"[italic dim]AND[/italic dim] {transformed}"
            lines.append(line)
        
        text += " ".join(lines)
        
        return text
    
    def _building_required_building(self) -> str:
        text: str = f"[bold]Required building:[/bold] "
        
        if len(self.required_building) == 0:
            return text + Building._format_none()
        
        lines: list[str] = []
        
        for idx, group in enumerate(self.required_building):
            prefix: str = "" if idx == 0 else "               [italic dim]OR:[/italic dim] "
            transformed: list[str] = [Building._format_building(text = element) for element in group]
            line: str = prefix + " [italic dim]AND[/italic dim] ".join(transformed)
            lines.append(line)
        
        text += "\n".join(lines)
        
        return text
    
    def _building_replaces(self) -> str:
        text: str = f"[bold]Replaces:[/bold] "
        return text + (Building._format_building(text = self.replaces) if self.replaces else Building._format_none())
    
    def _build_building_display(self) -> Panel:
        #* Heights
        padding: int = 2
        title_height: int = 2
        
        required_building_height: int = max(len(self.required_building), 1)
        number_of_other_properties_to_print: int = 16
        main_height: int = number_of_other_properties_to_print + required_building_height
        
        total_height: int = title_height + main_height
        
        #* Layout building
        layout: Layout = Layout()
        
        layout.split(
            Layout(
                name = "header",
                size = title_height,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "main",
                size = main_height,
                ratio = 0,
                visible = True,
            ),
        )
        
        layout["header"].update(
            renderable = Align(renderable = self._building_information(), align = "center")
        )
        
        layout["main"].split(
            Layout(
                name = "building_name",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "building_costs",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "maintenance_cost",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "productivity_bonuses",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "productivity_per_worker",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "effect_bonuses",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "effect_bonuses_per_worker",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "storage_capacity",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "max_workers",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "current_workers",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "is_buildable",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "is_deletable",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "is_upgradeable",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "required_geo",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "required_rss",
                size = 1,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "required_building",
                size = required_building_height,
                ratio = 0,
                visible = True,
            ),
            Layout(
                name = "replaces",
                size = 1,
                ratio = 0,
                visible = True,
            ),
        )
        
        layout["building_name"].update(
            renderable = Align(renderable = self._building_name(), align = "left")
        )
        
        layout["building_costs"].update(
            renderable = Align(renderable = self._building_building_costs(), align = "left")
        )
        
        layout["maintenance_cost"].update(
            renderable = Align(renderable = self._building_maintenance_costs(), align = "left")
        )
        
        layout["productivity_bonuses"].update(
            renderable = Align(renderable = self._building_productivity_bonuses(), align = "left")
        )
        
        layout["productivity_per_worker"].update(
            renderable = Align(renderable = self._building_productivity_per_worker(), align = "left")
        )
        
        layout["effect_bonuses"].update(
            renderable = Align(renderable = self._building_effect_bonuses(), align = "left")
        )
        
        layout["effect_bonuses_per_worker"].update(
            renderable = Align(renderable = self._building_effect_bonuses_per_worker(), align = "left")
        )
        
        layout["storage_capacity"].update(
            renderable = Align(renderable = self._building_storage_capacity(), align = "left")
        )
        
        layout["max_workers"].update(
            renderable = Align(renderable = self._building_max_workers(), align = "left")
        )
        
        layout["current_workers"].update(
            renderable = Align(renderable = self._building_current_workers(), align = "left")
        )
        
        layout["is_buildable"].update(
            renderable = Align(renderable = self._building_is_buildable(), align = "left")
        )
        
        layout["is_deletable"].update(
            renderable = Align(renderable = self._building_is_deletable(), align = "left")
        )
        
        layout["is_upgradeable"].update(
            renderable = Align(renderable = self._building_is_upgradeable(), align = "left")
        )
        
        layout["required_geo"].update(
            renderable = Align(renderable = self._building_required_geo(), align = "left")
        )
        
        layout["required_rss"].update(
            renderable = Align(renderable = self._building_required_rss(), align = "left")
        )
        
        layout["required_building"].update(
            renderable = Align(renderable = self._building_required_building(), align = "left")
        )
        
        layout["replaces"].update(
            renderable = Align(renderable = self._building_replaces(), align = "left")
        )
        
        return Panel(
            renderable = layout,
            height = total_height + padding,
            width = 105,
        )
    
    def display_building(self) -> None:
        """
        Render the building's information and current state to the console using the Rich library.
        """
        console: Console = Console()
        console.print(self._build_building_display())
