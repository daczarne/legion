from math import floor

BUILDINGS: dict[str, dict[str, dict[str, int] | int]] = {
    "city_hall": {
        "maintenance_cost": {
            "food": 1,
            "ore": 1,
            "wood": 1
        },
        "productivity_bonus": {
            "food": 0.25,
            "ore": 0.25,
            "wood": 0.25
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 3
    },
    "farm": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 12,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 3
    },
    "vineyard": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.10,
            "ore": 0.10,
            "wood": 0.10
        },
        "production_per_worker": {
            "food": 10,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 3
    },
    "fishing_village": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 8,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 3
    },
    "mine": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 12,
            "wood": 0
        },
        "max_workers": 3
    },
    "outcrop_mine": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 13,
            "wood": 0
        },
        "max_workers": 2
    },
    "mountain_mine": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 20,
            "wood": 0
        },
        "max_workers": 1
    },
    "lumber_mill": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 12
        },
        "max_workers": 3
    },
    "basilica": {
        "maintenance_cost": {
            "food": 3,
            "ore": 3,
            "wood": 3
        },
        "productivity_bonus": {
            "food": 0.50,
            "ore": 0.50,
            "wood": 0.50
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 1
    },
    "farmers_guild": {
        "maintenance_cost": {
            "food": 10,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.50,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "miners_guild": {
        "maintenance_cost": {
            "food": 0,
            "ore": 10,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.50,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "carpenters_guild": {
        "maintenance_cost": {
            "food": 0,
            "ore": 0,
            "wood": 10
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.50
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "gladiator_school": {
        "maintenance_cost": {
            "food": 0,
            "ore": 8,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.10,
            "ore": 0.10,
            "wood": 0.10
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "imperial_residence": {
        "maintenance_cost": {
            "food": 8,
            "ore": 8,
            "wood": 8
        },
        "productivity_bonus": {
            "food": 0.10,
            "ore": 0.10,
            "wood": 0.10
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "quartermaster": {
        "maintenance_cost": {
            "food": 12,
            "ore": 8,
            "wood": 8
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "large_fort": {
        "maintenance_cost": {
            "food": 15,
            "ore": 0,
            "wood": 15
        },
        "productivity_bonus": {
            "food": 0.10,
            "ore": 0.10,
            "wood": 0.10
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "stables": {
        "maintenance_cost": {
            "food": 5,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "training_ground": {
        "maintenance_cost": {
            "food": 10,
            "ore": 0,
            "wood": 10
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "bordello": {
        "maintenance_cost": {
            "food": 8,
            "ore": 4,
            "wood": 8
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 0
    },
    "hospital": {
        "maintenance_cost": {
            "food": 8,
            "ore": 0,
            "wood": 0
        },
        "productivity_bonus": {
            "food": 0.0,
            "ore": 0.0,
            "wood": 0.0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 3
    }
}


def display_production_table(production_table: dict[str, dict[str, int]]):
    col_headers: list[str] = [
        "Resource",
        "Rss. pot.",
        "Prod.",
        "Bonus",
        "Maintenance",
        "Total"
    ]
    table_header: str = "| " + " | ".join(col_headers) + " |"
    horizontal_rule: str = "-" * len(table_header)
    
    #* Table header
    print(horizontal_rule)
    print(table_header)
    print(horizontal_rule)
    
    #* Food row
    prod_pot, base_prod, prod_bonus, maintenance, total = production_table.get("food").values()
    print(
        f"| Food{' ' * 4} "
        f"| {' ' * (len(col_headers[1]) - len(str(prod_pot)))}{prod_pot} "
        f"| {' ' * (len(col_headers[2]) - len(str(base_prod)))}{base_prod} "
        f"| {' ' * (len(col_headers[3]) - len(str(prod_bonus)))}{prod_bonus} "
        f"| {' ' * (len(col_headers[4]) - len(str(maintenance)))}{maintenance} "
        f"| {' ' * (len(col_headers[5]) - len(str(total)))}{total} |"
    )
    
    #* Ore row
    prod_pot, base_prod, prod_bonus, maintenance, total = production_table.get("ore").values()
    print(
        f"| Ore{' ' * 5} "
        f"| {' ' * (len(col_headers[1]) - len(str(prod_pot)))}{prod_pot} "
        f"| {' ' * (len(col_headers[2]) - len(str(base_prod)))}{base_prod} "
        f"| {' ' * (len(col_headers[3]) - len(str(prod_bonus)))}{prod_bonus} "
        f"| {' ' * (len(col_headers[4]) - len(str(maintenance)))}{maintenance} "
        f"| {' ' * (len(col_headers[5]) - len(str(total)))}{total} |"
    )
    
    #* Wood row
    prod_pot, base_prod, prod_bonus, maintenance, total = production_table.get("wood").values()
    print(
        f"| Wood{' ' * 4} "
        f"| {' ' * (len(col_headers[1]) - len(str(prod_pot)))}{prod_pot} "
        f"| {' ' * (len(col_headers[2]) - len(str(base_prod)))}{base_prod} "
        f"| {' ' * (len(col_headers[3]) - len(str(prod_bonus)))}{prod_bonus} "
        f"| {' ' * (len(col_headers[4]) - len(str(maintenance)))}{maintenance} "
        f"| {' ' * (len(col_headers[5]) - len(str(total)))}{total} |"
    )
    
    #* Bottom horizontal row
    print(horizontal_rule)


def build_production_table(
        production_potentials: list[int],
        city_buildings: dict[str, int]
    ) -> dict[str, dict[str, int]]:
    
    scenario_results: dict[str, dict[str, int]] = {
        "food": {
            "prod_pot": production_potentials[0],
            "base_prod": 0,
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        },
        "ore": {
            "prod_pot": production_potentials[1],
            "base_prod": 0,
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        },
        "wood": {
            "prod_pot": production_potentials[2],
            "base_prod": 0,
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        }
    }
    
    city_prod_potential_food, city_prod_potential_ore, city_prod_potential_wood = production_potentials
    
    for key, value in city_buildings.items():
        building: str = key
        qty_buildings: int = value
        
        # Calculate production (`base_prod`)
        building_info: dict[str, dict[str, int] | int] = BUILDINGS.get(building, {}).get("production_per_worker", {})
        max_workers: dict[str, dict[str, int] | int] = BUILDINGS.get(building, {}).get("max_workers", {})
        
        building_prod_per_worker_food, building_prod_per_worker_ore, building_prod_per_worker_wood = [value for value in building_info.values()]
        
        # prod_per_worker = floor(prod_potential * prod_per_worker / 100)
        city_prod_per_worker_food: int = int(floor(city_prod_potential_food * building_prod_per_worker_food / 100.0))
        city_prod_per_worker_ore: int = int(floor(city_prod_potential_ore * building_prod_per_worker_ore / 100.0))
        city_prod_per_worker_wood: int = int(floor(city_prod_potential_wood * building_prod_per_worker_wood / 100.0))
        
        # base_prod = qty_buildings * prod_per_worker * max_workers
        city_base_production_food: int = qty_buildings * city_prod_per_worker_food * max_workers
        city_base_production_ore: int = qty_buildings * city_prod_per_worker_ore * max_workers
        city_base_production_wood: int = qty_buildings * city_prod_per_worker_wood * max_workers
        
        # Store results in scenario results
        scenario_results["food"]["base_prod"] = scenario_results["food"]["base_prod"] + city_base_production_food
        scenario_results["ore"]["base_prod"] = scenario_results["ore"]["base_prod"] + city_base_production_ore
        scenario_results["wood"]["base_prod"] = scenario_results["wood"]["base_prod"] + city_base_production_wood
        
        print(
            f"{building}: "
            f"prod per worker: {city_prod_per_worker_food} - {city_prod_per_worker_ore} - {city_prod_per_worker_wood} | "
            f"production: {city_base_production_food} - {city_base_production_ore} - {city_base_production_wood}"
        )
    
    print()
    return scenario_results


def display_city_buildings(city_buildings: list[str]) -> None:
    print(f"City buildings: {city_buildings}")


def calculate_scenario(scenario: dict) -> None:
    
    print()
    
    #* Validate city buildings
    # The total number must not exceed 9
    # City Hall must be included in the buildings
    city_buildings: dict[str, int] = scenario.get("city_buildings")
    city_buildings: dict[str, int] = {key: value for key, value in city_buildings.items() if value > 0}
    
    if "city_hall" not in city_buildings.keys():
        city_buildings = {**{"city_hall": 1}, **city_buildings}
    
    if sum(city_buildings.values()) > 9:
        print("Warning! Too many buildings!")
        print()
        print("The maximum number of buildings is 9 and must include `city_hall`.")
        print()
        return False
    
    #* Display city buildings
    display_city_buildings(city_buildings = city_buildings)
    print()
    
    #* Build production table
    city_production_table: dict[str, dict[str, int]] = build_production_table(
        production_potentials = scenario.get("production_potentials"),
        city_buildings = city_buildings
    )
    
    #* Display production table
    display_production_table(city_production_table)
    print()


calculate_scenario(
    scenario = {
        "production_potentials": [100, 100, 200],
        "city_buildings": {
            "city_hall": 1,
            "farm": 1,
            "vineyard": 1,
            "fishing_village": 0,
            "farmers_guild": 0,
            "mine": 1,
            "outcrop_mine": 1,
            "mountain_mine": 1,
            "miners_guild": 0,
            "lumber_mill": 1,
            "carpenters_guild": 0,
            "basilica": 0,
            "gladiator_school": 0,
            "imperial_residence": 0,
        }
    }
)

print("#" * 63)

calculate_scenario(
    scenario = {
        "production_potentials": [115, 10, 50],
        "city_buildings": {
            "farm": 1,
            "lumber_mill": 1
        }
    }
)
