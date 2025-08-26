"""
Module for building Rich displays.

This module provides classes and types for building display configurations. These are used in City, Scenario, and
Kingdom to control how information is displayed.

Public API:
    - DisplaySection: Enum representing different display sections.
    - DisplayConfiguration: TypedDict for configuring the display of city sections.
    - DisplaySectionConfiguration: TypedDict for configuring individual sections.
    - DEFAULT_SECTION_COLORS: Default colors for sections.

Internal objects:
    - _DisplaySectionColors: Mapping of section names to their default colors.
"""

from enum import Enum
from typing import TypeAlias, TypedDict

__all__: list[str] = ["DisplayConfiguration"]


_DisplaySectionColors: TypeAlias = dict[str, str]


class DisplaySection(Enum):
    """
    Enum representing the different sections that can be displayed for a `_CityDisplayBuilder`.
    
    Values:
        CITY: City header with campaign and name.
        BUILDINGS: List of city buildings and their counts.
        EFFECTS: Effects table showing city, building, worker, and total bonuses.
        PRODUCTION: Production table including resource potentials, base, bonuses, total, maintenance, and balance.
        STORAGE: Storage capacities for city, buildings, warehouse, supply dump, and total.
        DEFENSES: Defense information including garrison, squadrons, and squadron size.
    """
    CITY = "city"
    BUILDINGS = "buildings"
    EFFECTS = "effects"
    PRODUCTION = "production"
    STORAGE = "storage"
    DEFENSES = "defenses"


class DisplaySectionConfiguration(TypedDict, total = False):
    """
    Configuration for an individual display section in `_CityDisplayBuilder`.
    
    Keys:
        include (bool): Whether to display this section.
        height (int): Height of the section in rows.
        color (str): Color for the section text, as a Rich color string or HEX value.
    """
    include: bool
    height: int
    color: str


class DisplayConfiguration(TypedDict, total = False):
    """
    Full display configuration for a `_CityDisplayBuilder`, mapping each section to its configuration.
    
    Keys:
        city (DisplaySectionConfiguration): Configuration for the city header.
        buildings (DisplaySectionConfiguration): Configuration for the buildings list.
        effects (DisplaySectionConfiguration): Configuration for the effects table.
        production (DisplaySectionConfiguration): Configuration for the production table.
        storage (DisplaySectionConfiguration): Configuration for the storage table.
        defenses (DisplaySectionConfiguration): Configuration for the defenses table.
    """
    city: DisplaySectionConfiguration
    buildings: DisplaySectionConfiguration
    effects: DisplaySectionConfiguration
    production: DisplaySectionConfiguration
    storage: DisplaySectionConfiguration
    defenses: DisplaySectionConfiguration


DEFAULT_SECTION_COLORS: _DisplaySectionColors = {
    "effects": "#5f5fff",
    "production": "#228b22",
    "storage": "purple",
    "defenses": "red",
}
