from typing import TypedDict, TypeAlias


class BuildingResources(TypedDict):
    food: int
    ore: int
    wood: int


class Building(TypedDict):
    maintenance_cost: BuildingResources
    productivity_bonus: BuildingResources
    production_per_worker: BuildingResources
    # capability_bonus: dict[str, int]
    max_workers: int


BuildingsCount: TypeAlias = dict[str, int]

#! Deprecated
MAX_BUILDINGS_PER_CITY: int = 9


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
        "max_workers": 3,
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
        "max_workers": 1,
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
        "max_workers": 3,
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
        # capability_bonus
        # Having it in the city => +0 population growth
        # Manning it => +50 pop growth
        "max_workers": 1,
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
        "max_workers": 0,
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
        "max_workers": 0,
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
        # capability_bonus
        # +10 intelligence (all fort sizes)
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
        "max_workers": 0,
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
        # capability_bonus
        # Having it in the city => +20 troop training
        # Manning it => +5 troop training
        "max_workers": 0,
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
        # capability_bonus
        # Having it in the city => +10 troop training
        "max_workers": 0,
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
        # capability_bonus
        # Having it in the city => +100 pop growth (+50 for baths)
        # Manning it => +40 pop growth per worker (+25 for baths)
        "max_workers": 3,
    },
}

# Market
# Intelligence +10 for having it in the city
# Large Market
# Intelligence +15 for having it in the city
