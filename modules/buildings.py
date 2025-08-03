from typing import TypedDict, Any
from dataclasses import dataclass
from enum import Enum


class GeoFeature(Enum):
    LAKE = "lake"
    OUTCROP_ROCK = "outcrop_rock"
    MOUNTAIN = "mountain"
    FOREST = "forest"


@dataclass
class EffectBonuses:
    troop_training: int = 0
    population_growth: int = 0
    intelligence: int = 0


@dataclass
class RssCollection:
    food: int = 0
    ore: int = 0
    wood: int = 0


@dataclass
class Building:
    id: str
    name: str
    building_cost: RssCollection
    maintenance_cost: RssCollection
    productivity_bonuses: RssCollection
    productivity_per_worker: RssCollection
    effect_bonuses: EffectBonuses
    effect_bonuses_per_worker: EffectBonuses
    storage_capacity: RssCollection
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: GeoFeature | None


class Building2(TypedDict):
    name: str
    maintenance_cost: RssCollection
    productivity_bonuses: RssCollection
    productivity_per_worker: RssCollection
    effect_bonuses: EffectBonuses
    max_workers: int


BUILDINGS: dict[str, Building2] = {
    "city_hall": {
        "name": "City hall",
        "maintenance_cost": RssCollection(food = 1, ore = 1, wood = 1),
        "productivity_bonuses": RssCollection(food = 25, ore = 25, wood = 25),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "hunters_lodge": {
        "name": "Hunters' lodge",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(food = 2, ore = 2, wood = 2),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 3,
    },
    "large_farm": {
        "name": "Large farm",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(food = 12),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 3,
    },
    "vineyard": {
        "name": "Vineyard",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(food = 10, ore = 10, wood = 10),
        "productivity_per_worker": RssCollection(food = 10),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 3,
    },
    "fishing_village": {
        "name": "Fishing village",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(food = 9),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 3,
    },
    "farmers_guild": {
        "name": "Farmers' guild",
        "maintenance_cost": RssCollection(food = 10),
        "productivity_bonuses": RssCollection(food = 50),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "stables": {
        "name": "Stables",
        "maintenance_cost": RssCollection(food = 5),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "large_mine": {
        "name": "Large mine",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(ore = 12),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 3,
    },
    "outcrop_mine": {
        "name": "Outcrop mine",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(ore = 13),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 2,
    },
    "mountain_mine": {
        "name": "Mountain mine",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(ore = 20),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 1,
    },
    "miners_guild": {
        "name": "Miners' guild",
        "maintenance_cost": RssCollection(ore = 10),
        "productivity_bonuses": RssCollection(ore = 50),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "blacksmith": {
        "name": "Blacksmith",
        "maintenance_cost": RssCollection(ore = 5),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "large_lumber_mill": {
        "name": "Large lumber mill",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(wood = 12),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 3,
    },
    "carpenters_guild": {
        "name": "Carpenters' guild",
        "maintenance_cost": RssCollection(wood = 10),
        "productivity_bonuses": RssCollection(wood = 50),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "fletcher": {
        "name": "Fletcher",
        "maintenance_cost": RssCollection(wood = 5),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "basilica": {
        "name": "Basilica",
        "maintenance_cost": RssCollection(food = 3, ore = 3, wood = 3),
        "productivity_bonuses": RssCollection(food = 50, ore = 50, wood = 50),
        "productivity_per_worker": RssCollection(),
        # Having it in the city => +0 population growth
        # Manning it => +50 pop growth
        "effect_bonuses": EffectBonuses(population_growth = 50),
        "max_workers": 1,
    },
    "temple": {
        "name": "Temple",
        "maintenance_cost": RssCollection(food = 2, ore = 2, wood = 2),
        "productivity_bonuses": RssCollection(food = 25, ore = 25, wood = 25),
        "productivity_per_worker": RssCollection(),
        # Having it in the city => +0 population growth
        # Manning it => +40 pop growth (+25 for the shrine)
        "effect_bonuses": EffectBonuses(population_growth = 40),
        "max_workers": 1,
    },
    "hidden_grove": {
        # Requires a forest to be present in the city. If the forest is
        # destroyed, it cannot be built any more.
        "name": "Hidden grove",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(food = 15, ore = 15, wood = 15),
        "productivity_per_worker": RssCollection(),
        # Having it in the city => +50 population growth
        # Manning it => +50 pop growth per worker
        "effect_bonuses": EffectBonuses(population_growth = 200),
        "max_workers": 3,
    },
    "apothecary": {
        "name": "Apothecary",
        "maintenance_cost": RssCollection(food = 5),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        # Having it in the city => +50 pop growth
        # Manning it => +20 pop growth per worker
        "effect_bonuses": EffectBonuses(population_growth = 90),
        "max_workers": 2,
    },
    "hospital": {
        "name": "Hospital",
        "maintenance_cost": RssCollection(food = 8),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        # Having it in the city => +100 pop growth (+50 for baths)
        # Manning it => +40 pop growth per worker (+25 for baths)
        "effect_bonuses": EffectBonuses(population_growth = 220),
        "max_workers": 3,
    },
    "training_ground": {
        "name": "Training ground",
        "maintenance_cost": RssCollection(food = 10, wood = 10),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        # Having it in the city => +20 troop training
        # Manning it => +5 troop training
        "effect_bonuses": EffectBonuses(troop_training = 25),
        "max_workers": 1,
    },
    "bordello": {
        "name": "Bordello",
        "maintenance_cost": RssCollection(food = 8, ore = 4, wood = 8),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        # Having it in the city => +10 troop training
        "effect_bonuses": EffectBonuses(troop_training = 10),
        "max_workers": 0,
    },
    "gladiator_school": {
        "name": "Gladiator school",
        "maintenance_cost": RssCollection(ore = 8),
        "productivity_bonuses": RssCollection(food = 10, ore = 10, wood = 10),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "imperial_residence": {
        "name": "Imperial residence",
        "maintenance_cost": RssCollection(food = 8, ore = 8, wood = 8),
        "productivity_bonuses": RssCollection(food = 10, ore = 10, wood = 10),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "quartermaster": {
        "name": "Quartermaster",
        "maintenance_cost": RssCollection(food = 12, ore = 8, wood = 8),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "large_fort": {
        "name": "Large fort",
        "maintenance_cost": RssCollection(food = 15, wood = 15),
        "productivity_bonuses": RssCollection(food = 10, ore = 10, wood = 10),
        "productivity_per_worker": RssCollection(),
        # +10 intelligence (all fort sizes)
        "effect_bonuses": EffectBonuses(intelligence = 10),
        "max_workers": 0,
    },
    "large_market": {
        "name": "Large market",
        "maintenance_cost": RssCollection(food = -5, ore = -5, wood = -5),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        # Intelligence +15 for having it in the city (+10 for the small market)
        "effect_bonuses": EffectBonuses(intelligence = 15),
        "max_workers": 0,
    },
    "watch_tower": {
        "name": "Watch tower",
        "maintenance_cost": RssCollection(food = 8, wood = 4),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        # Intelligence +20 for having it in the city
        # Intelligence +15 per each worker
        "effect_bonuses": EffectBonuses(intelligence = 50),
        "max_workers": 2,
    },
    "warehouse": {
        "name": "Warehouse",
        "maintenance_cost": RssCollection(),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(),
        "max_workers": 0,
    },
    "supply_dump": {
        "name": "Supply dump",
        "maintenance_cost": RssCollection(food = -10, ore = -10, wood = -10),
        "productivity_bonuses": RssCollection(),
        "productivity_per_worker": RssCollection(),
        "effect_bonuses": EffectBonuses(population_growth = 100),
        "max_workers": 0,
    },
}
