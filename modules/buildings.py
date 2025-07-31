from typing import TypedDict, TypeAlias


class BuildingResources(TypedDict):
    food: int
    ore: int
    wood: int

class EffectBonuses(TypedDict):
    troop_training: int
    population_growth: int
    intelligence: int


class Building(TypedDict):
    maintenance_cost: BuildingResources
    productivity_bonus: BuildingResources
    production_per_worker: BuildingResources
    effect_bonuses: EffectBonuses
    max_workers: int


BuildingsCount: TypeAlias = dict[str, int]


BUILDINGS: dict[str, Building] = {
    "city_hall": {
        "maintenance_cost": {
            "food": 1,
            "ore": 1,
            "wood": 1,
        },
        "productivity_bonus": {
            "food": 25,
            "ore": 25,
            "wood": 25,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "hunters_lodge": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 2,
            "ore": 2,
            "wood": 2,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "farm": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 12,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "vineyard": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 10,
            "ore": 10,
            "wood": 10,
        },
        "production_per_worker": {
            "food": 10,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "fishing_village": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 9,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "farmers_guild": {
        "maintenance_cost": {
            "food": 10,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 50,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "stables": {
        "maintenance_cost": {
            "food": 5,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "mine": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 12,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "outcrop_mine": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 13,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 2,
    },
    "mountain_mine": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 20,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 1,
    },
    "miners_guild": {
        "maintenance_cost": {
            "food": 0,
            "ore": 10,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 50,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "blacksmith": {
        "maintenance_cost": {
            "food": 0,
            "ore": 5,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "lumber_mill": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 12,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "carpenters_guild": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 10,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 50,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "fletcher": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 5,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "basilica": {
        "maintenance_cost": {
            "food": 3,
            "ore": 3,
            "wood": 3,
        },
        "productivity_bonus": {
            "food": 50,
            "ore": 50,
            "wood": 50,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Having it in the city => +0 population growth
        # Manning it => +50 pop growth
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 50,
            "intelligence": 0,
        },
        "max_workers": 1,
    },
    "temple": {
        "maintenance_cost": {
            "food": 2,
            "ore": 2,
            "wood": 2,
        },
        "productivity_bonus": {
            "food": 25,
            "ore": 25,
            "wood": 25,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Having it in the city => +0 population growth
        # Manning it => +40 pop growth (+25 for the shrine)
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 40,
            "intelligence": 0,
        },
        "max_workers": 1,
    },
    "hidden_grove": {
        # Requires a forest to be present in the city. If the forest is
        # destroyed, it cannot be built any more.
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 15,
            "ore": 15,
            "wood": 15,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Having it in the city => +50 population growth
        # Manning it => +50 pop growth per worker
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 200,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "apothecary": {
        "maintenance_cost": {
            "food": 5,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Having it in the city => +50 pop growth
        # Manning it => +20 pop growth per worker
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 90,
            "intelligence": 0,
        },
        "max_workers": 2,
    },
    "hospital": {
        "maintenance_cost": {
            "food": 8,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Having it in the city => +100 pop growth (+50 for baths)
        # Manning it => +40 pop growth per worker (+25 for baths)
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 220,
            "intelligence": 0,
        },
        "max_workers": 3,
    },
    "training_ground": {
        "maintenance_cost": {
            "food": 10,
            "ore": 0,
            "wood": 10,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Having it in the city => +20 troop training
        # Manning it => +5 troop training
        "effect_bonuses": {
            "troop_training": 25,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 1,
    },
    "bordello": {
        "maintenance_cost": {
            "food": 8,
            "ore": 4,
            "wood": 8
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Having it in the city => +10 troop training
        "effect_bonuses": {
            "troop_training": 10,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "gladiator_school": {
        "maintenance_cost": {
            "food": 0,
            "ore": 8,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 10,
            "ore": 10,
            "wood": 10,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "imperial_residence": {
        "maintenance_cost": {
            "food": 8,
            "ore": 8,
            "wood": 8,
        },
        "productivity_bonus": {
            "food": 10,
            "ore": 10,
            "wood": 10,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "quartermaster": {
        "maintenance_cost": {
            "food": 12,
            "ore": 8,
            "wood": 8,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
    "large_fort": {
        "maintenance_cost": {
            "food": 15,
            "ore": 0,
            "wood": 15,
        },
        "productivity_bonus": {
            "food": 10,
            "ore": 10,
            "wood": 10,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # +10 intelligence (all fort sizes)
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 10,
        },
        "max_workers": 0,
    },
    "market": {
        "maintenance_cost": {
            "food": -5,
            "ore": -5,
            "wood": -5,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Intelligence +15 for having it in the city (+10 for the small market)
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 15,
        },
        "max_workers": 2,
    },
    "watch_tower": {
        "maintenance_cost": {
            "food": 8,
            "ore": 0,
            "wood": 4,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        # Intelligence +20 for having it in the city
        # Intelligence +15 per each worker
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 50,
        },
        "max_workers": 2,
    },
    "warehouse": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "productivity_bonus": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0,
        },
        "effect_bonuses": {
            "troop_training": 0,
            "population_growth": 0,
            "intelligence": 0,
        },
        "max_workers": 0,
    },
}
