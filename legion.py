BUILDINGS: dict[dict, dict[str, int | float] | int] = {
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
            "ore": 0,
            "wood": 12
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
            "food": 13,
            "ore": 0,
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
            "food": 20,
            "ore": 0,
            "wood": 0
        },
        "max_workers": 1
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
    }
}


def print_results(results: dict[str, dict[str, int]]):
    col_headers: list[str] = [
        "Resource",
        "Prod. pot.",
        "Prod."
        "Bonus",
        "Maintenance",
        "Total"
    ]
    table_header: str = "| " + " | ".join(col_headers) + " |"
    horizontal_rule: str = "-" * len(table_header)
    
    print()
    print(horizontal_rule)
    print(table_header)
    print(horizontal_rule)
    prod_pot, prod_bonus, maintenance, total = results.get("food").values()
    print(
        f"| Food{' ' * 4} "
        f"| {' ' * (len(col_headers[1]) - len(str(prod_pot)))}{prod_pot} "
        f"| {' ' * (len(col_headers[2]) - len(str(prod_bonus)))}{prod_bonus} "
        f"| {' ' * (len(col_headers[3]) - len(str(maintenance)))}{maintenance} "
        f"| {' ' * (len(col_headers[4]) - len(str(total)))}{total} |"
    )
    prod_pot, prod_bonus, maintenance, total = results.get("ore").values()
    print(
        f"| Ore{' ' * 5} "
        f"| {' ' * (len(col_headers[1]) - len(str(prod_pot)))}{prod_pot} "
        f"| {' ' * (len(col_headers[2]) - len(str(prod_bonus)))}{prod_bonus} "
        f"| {' ' * (len(col_headers[3]) - len(str(maintenance)))}{maintenance} "
        f"| {' ' * (len(col_headers[4]) - len(str(total)))}{total} |"
    )
    prod_pot, prod_bonus, maintenance, total = results.get("ore").values()
    print(
        f"| Wood{' ' * 4} "
        f"| {' ' * (len(col_headers[1]) - len(str(prod_pot)))}{prod_pot} "
        f"| {' ' * (len(col_headers[2]) - len(str(prod_bonus)))}{prod_bonus} "
        f"| {' ' * (len(col_headers[3]) - len(str(maintenance)))}{maintenance} "
        f"| {' ' * (len(col_headers[4]) - len(str(total)))}{total} |"
    )
    print(horizontal_rule)
    print()


def create_scenario(production_potentials: list[int], city_buildings: list[str]) -> dict[str, dict[str, int]]:
    
    scenario_results: dict[str, dict[str, int]] = {
        "food": {
            "prod_pot": production_potentials[0],
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        },
        "ore": {
            "prod_pot": production_potentials[1],
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        },
        "wood": {
            "prod_pot": production_potentials[2],
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        }
    }
    
    if "city_hall" not in city_buildings:
        city_buildings.append("city_hall")
    
    if len(city_buildings) > 9:
        print()
        print("Warning! Too many buildings!")
        return scenario_results
    
    return scenario_results


scenario_1 = create_scenario(
    production_potentials = [100, 150, 75],
    city_buildings = []
)

print_results(scenario_1)

print("#" * 60)

scenario_2 = create_scenario(
    production_potentials = [115, 10, 0],
    city_buildings = []
)

print_results(scenario_2)
