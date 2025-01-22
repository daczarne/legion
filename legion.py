from math import floor

BUILDINGS: dict[str, dict[str, dict[str, int] | int]] = {
    "city_hall": {
        "maintenance_cost": {
            "food": 1,
            "ore": 1,
            "wood": 1
        },
        "productivity_bonus": {
            "food": 25,
            "ore": 25,
            "wood": 25
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 10,
            "ore": 10,
            "wood": 10
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 50,
            "ore": 50,
            "wood": 50
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
            "food": 50,
            "ore": 0,
            "wood": 0
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
            "food": 0,
            "ore": 50,
            "wood": 0
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
            "food": 0,
            "ore": 0,
            "wood": 50
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
            "food": 10,
            "ore": 10,
            "wood": 10
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
            "food": 10,
            "ore": 10,
            "wood": 10
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 10,
            "ore": 10,
            "wood": 10
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 0,
            "ore": 0,
            "wood": 0
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
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "production_per_worker": {
            "food": 0,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 3
    }
}

MAX_BUILDINGS_PER_CITY: int = 9


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


def calculate_base_city_production(
        city_buildings:  dict[str, int],
        production_potentials: list[int],
        scenario_results: dict[str, dict[str, int]],
    ) -> dict[str, dict[str, int]]:
    
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
    
    return scenario_results


def calculate_city_production_bonus(
        city_buildings:  dict[str, int],
        scenario_results: dict[str, dict[str, int]],
    ) -> dict[str, dict[str, int]]:
    
    for key, value in city_buildings.items():
        building: str = key
        
        # Calculate production bonus (`prod_bonus`)
        building_info: dict[str, dict[str, int] | int] = BUILDINGS.get(building, {}).get("productivity_bonus", {})
        
        city_prod_bonus_food, city_prod_bonus_ore, city_prod_bonus_worker_wood = [value for value in building_info.values()]
        
        # Store results in scenario results
        scenario_results["food"]["prod_bonus"] = scenario_results["food"]["prod_bonus"] + city_prod_bonus_food
        scenario_results["ore"]["prod_bonus"] = scenario_results["ore"]["prod_bonus"] + city_prod_bonus_ore
        scenario_results["wood"]["prod_bonus"] = scenario_results["wood"]["prod_bonus"] + city_prod_bonus_worker_wood
    
    return scenario_results


def calculate_city_maintenance_costs(
        city_buildings:  dict[str, int],
        scenario_results: dict[str, dict[str, int]],
    ) -> dict[str, dict[str, int]]:
    
    for key, value in city_buildings.items():
        building: str = key
        
        # Calculate production bonus (`prod_bonus`)
        building_info: dict[str, dict[str, int] | int] = BUILDINGS.get(building, {}).get("maintenance_cost", {})
        
        maintenance_cost_food, maintenance_cost_ore, maintenance_cost_worker_wood = [value for value in building_info.values()]
        
        # Store results in scenario results
        scenario_results["food"]["maintenance"] = scenario_results["food"]["maintenance"] + maintenance_cost_food
        scenario_results["ore"]["maintenance"] = scenario_results["ore"]["maintenance"] + maintenance_cost_ore
        scenario_results["wood"]["maintenance"] = scenario_results["wood"]["maintenance"] + maintenance_cost_worker_wood
    
    return scenario_results


def calculate_totals(
        scenario_results: dict[str, dict[str, int]]
    ) -> dict[str, dict[str, int]]:
    
    for rss, rss_results in scenario_results.items():
        base_production: int = rss_results.get("base_prod", 0)
        production_bonus: int = rss_results.get("prod_bonus", 0)
        maintenance_costs: int = rss_results.get("maintenance", 0)
        total_production: int = int(floor(base_production * (1 + production_bonus / 100) - maintenance_costs))
        scenario_results[rss]["total"] = total_production
    
    return scenario_results


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
    
    scenario_results = calculate_base_city_production(
        city_buildings = city_buildings,
        production_potentials = production_potentials,
        scenario_results = scenario_results
    )
    
    scenario_results = calculate_city_production_bonus(
        city_buildings = city_buildings,
        scenario_results = scenario_results
    )
    
    scenario_results = calculate_city_maintenance_costs(
        city_buildings = city_buildings,
        scenario_results = scenario_results
    )
    
    scenario_results = calculate_totals(
        scenario_results = scenario_results
    )
    
    return scenario_results


def display_city_buildings(city_buildings: list[str]) -> None:
    print(f"City buildings: {city_buildings}")


def calculate_scenario(
        scenario: dict[str, list[int] | dict[str, int]]
    ) -> None:
    
    print()
    
    #* Validate city buildings
    # The total number must not exceed MAX_BUILDINGS_PER_CITY
    # City Hall must be included in the buildings
    city_buildings: dict[str, int] = scenario.get("city_buildings")
    city_buildings: dict[str, int] = {key: value for key, value in city_buildings.items() if value > 0}
    
    if "city_hall" not in city_buildings.keys():
        city_buildings = {**{"city_hall": 1}, **city_buildings}
    
    if sum(city_buildings.values()) > MAX_BUILDINGS_PER_CITY:
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


city_production_potentials: list[int] = [100, 100, 100]

calculate_scenario(
    scenario = {
        "production_potentials": city_production_potentials,
        "city_buildings": {
            "city_hall": 1,
            "farm": 5,
            "vineyard": 1,
            "fishing_village": 0,
            "farmers_guild": 1,
            "mine": 0,
            "outcrop_mine": 0,
            "mountain_mine": 0,
            "miners_guild": 0,
            "lumber_mill": 0,
            "carpenters_guild": 0,
            "basilica": 1,
            "gladiator_school": 0,
            "imperial_residence": 0,
        }
    }
)

print("#" * 63)

calculate_scenario(
    scenario = {
        "production_potentials": city_production_potentials,
        "city_buildings": {
            "city_hall": 1,
            "farm": 6,
            "vineyard": 0,
            "fishing_village": 0,
            "farmers_guild": 1,
            "mine": 0,
            "outcrop_mine": 0,
            "mountain_mine": 0,
            "miners_guild": 0,
            "lumber_mill": 0,
            "carpenters_guild": 0,
            "basilica": 1,
            "gladiator_school": 0,
            "imperial_residence": 0,
        }
    }
)
