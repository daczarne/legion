from math import floor

from modules.buildings import BUILDINGS, BuildingsCount
from modules.scenario import Scenario

MAX_BUILDINGS_PER_CITY: int = 9

def display_production_table(production_table: dict[str, dict[str, int]]) -> None:
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
    prod_pot, base_prod, prod_bonus, maintenance, total = production_table.get("food", {}).values()
    print(
        f"| Food{' ' * 4} "
        f"| {' ' * (len(col_headers[1]) - len(str(prod_pot)))}{prod_pot} "
        f"| {' ' * (len(col_headers[2]) - len(str(base_prod)))}{base_prod} "
        f"| {' ' * (len(col_headers[3]) - len(str(prod_bonus)))}{prod_bonus} "
        f"| {' ' * (len(col_headers[4]) - len(str(maintenance)))}{maintenance} "
        f"| {' ' * (len(col_headers[5]) - len(str(total)))}{total} |"
    )
    
    #* Ore row
    prod_pot, base_prod, prod_bonus, maintenance, total = production_table.get("ore", {}).values()
    print(
        f"| Ore{' ' * 5} "
        f"| {' ' * (len(col_headers[1]) - len(str(prod_pot)))}{prod_pot} "
        f"| {' ' * (len(col_headers[2]) - len(str(base_prod)))}{base_prod} "
        f"| {' ' * (len(col_headers[3]) - len(str(prod_bonus)))}{prod_bonus} "
        f"| {' ' * (len(col_headers[4]) - len(str(maintenance)))}{maintenance} "
        f"| {' ' * (len(col_headers[5]) - len(str(total)))}{total} |"
    )
    
    #* Wood row
    prod_pot, base_prod, prod_bonus, maintenance, total = production_table.get("wood", {}).values()
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
        city_buildings: BuildingsCount,
        production_potentials: list[int],
        scenario_results,
    ):
    
    city_prod_potential_food, city_prod_potential_ore, city_prod_potential_wood = production_potentials
    
    for building, qty_buildings in city_buildings.items():
        
        # prod_per_worker = floor(prod_potential * prod_per_worker / 100)
        city_prod_per_worker_food = int(floor(city_prod_potential_food * BUILDINGS[building]["productivity_per_worker"].food / 100.0))
        city_prod_per_worker_ore = int(floor(city_prod_potential_ore * BUILDINGS[building]["productivity_per_worker"].ore / 100.0))
        city_prod_per_worker_wood = int(floor(city_prod_potential_wood * BUILDINGS[building]["productivity_per_worker"].wood / 100.0))
        
        # base_prod = qty_buildings * prod_per_worker * max_workers
        city_base_production_food: int = qty_buildings * city_prod_per_worker_food * BUILDINGS[building]["max_workers"]
        city_base_production_ore: int = qty_buildings * city_prod_per_worker_ore * BUILDINGS[building]["max_workers"]
        city_base_production_wood: int = qty_buildings * city_prod_per_worker_wood * BUILDINGS[building]["max_workers"]
        
        # Store results in scenario results
        scenario_results["food"]["base_prod"] = scenario_results["food"]["base_prod"] + city_base_production_food
        scenario_results["ore"]["base_prod"] = scenario_results["ore"]["base_prod"] + city_base_production_ore
        scenario_results["wood"]["base_prod"] = scenario_results["wood"]["base_prod"] + city_base_production_wood
    
    return scenario_results


def calculate_city_production_bonus(
        city_buildings,
        scenario_results,
    ):
    
    for building in city_buildings:
        scenario_results["food"]["prod_bonus"] = scenario_results["food"]["prod_bonus"] + BUILDINGS[building]["productivity_bonus"].food
        scenario_results["ore"]["prod_bonus"] = scenario_results["ore"]["prod_bonus"] + BUILDINGS[building]["productivity_bonus"].ore
        scenario_results["wood"]["prod_bonus"] = scenario_results["wood"]["prod_bonus"] + BUILDINGS[building]["productivity_bonus"].wood
    
    return scenario_results


def calculate_city_maintenance_costs(
        city_buildings,
        scenario_results,
    ):
    
    for building in city_buildings:
        # Store results in scenario results
        scenario_results["food"]["maintenance"] = scenario_results["food"]["maintenance"] + BUILDINGS[building]["maintenance_cost"].food
        scenario_results["ore"]["maintenance"] = scenario_results["ore"]["maintenance"] + BUILDINGS[building]["maintenance_cost"].ore
        scenario_results["wood"]["maintenance"] = scenario_results["wood"]["maintenance"] + BUILDINGS[building]["maintenance_cost"].wood
    
    return scenario_results


def calculate_totals(scenario_results: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    
    for rss, rss_results in scenario_results.items():
        base_production: int = rss_results.get("base_prod", 0)
        production_bonus: int = rss_results.get("prod_bonus", 0)
        maintenance_costs: int = rss_results.get("maintenance", 0)
        total_production: int = int(floor(base_production * (1 + production_bonus / 100) - maintenance_costs))
        scenario_results[rss]["total"] = total_production
    
    return scenario_results


def build_production_table(
        production_potentials: list[int],
        city_buildings: dict[str, int],
    ) -> dict[str, dict[str, int]]:
    
    scenario_results: dict[str, dict[str, int]] = {
        "food": {
            "prod_pot": production_potentials[0],
            "base_prod": 0,
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0,
        },
        "ore": {
            "prod_pot": production_potentials[1],
            "base_prod": 0,
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0,
        },
        "wood": {
            "prod_pot": production_potentials[2],
            "base_prod": 0,
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0,
        },
    }
    
    scenario_results = calculate_base_city_production(
        city_buildings = city_buildings,
        production_potentials = production_potentials,
        scenario_results = scenario_results,
    )
    
    scenario_results = calculate_city_production_bonus(
        city_buildings = city_buildings,
        scenario_results = scenario_results,
    )
    
    scenario_results = calculate_city_maintenance_costs(
        city_buildings = city_buildings,
        scenario_results = scenario_results,
    )
    
    scenario_results = calculate_totals(scenario_results = scenario_results)
    
    return scenario_results


#! migrated
def display_city_buildings(city_buildings: BuildingsCount) -> None:
    print(f"City buildings")
    print(f"--------------")
    
    for building, qty in city_buildings.items():
        print(f"  - {building.replace('_', ' ').capitalize()} ({qty})")


def calculate_scenario(scenario: Scenario) -> None:
    
    print()
    
    #* Validate city buildings
    # The total number must not exceed MAX_BUILDINGS_PER_CITY
    # City Hall must be included in the buildings
    city_buildings: BuildingsCount = {key: value for key, value in scenario.get("city_buildings").items() if value > 0}
    
    if "city_hall" not in city_buildings.keys():
        city_buildings = {**{"city_hall": 1}, **city_buildings}
    
    if sum(city_buildings.values()) > MAX_BUILDINGS_PER_CITY:
        print("Warning! Too many buildings!")
        print()
        print("The maximum number of buildings is 9 and must include `city_hall`.")
        print()
        return
    
    display_city_buildings(city_buildings = city_buildings)
    print()
    
    city_production_table: dict[str, dict[str, int]] = build_production_table(
        production_potentials = scenario.get("production_potentials"),
        city_buildings = city_buildings,
    )
    
    display_production_table(production_table = city_production_table)
    print()


city_production_potentials: list[int] = [100, 80, 0]

scenario: Scenario = {
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
        "quartermaster": 0,
        "large_fort": 0,
    },
}
calculate_scenario(scenario = scenario)

print("#" * 63)

scenario: Scenario = {
    "production_potentials": city_production_potentials,
    "city_buildings": {
        "city_hall": 1,
        "farm": 0,
        "vineyard": 0,
        "fishing_village": 0,
        "farmers_guild": 0,
        "mine": 6,
        "outcrop_mine": 0,
        "mountain_mine": 0,
        "miners_guild": 1,
        "lumber_mill": 0,
        "carpenters_guild": 0,
        "basilica": 1,
        "gladiator_school": 0,
        "imperial_residence": 0,
        "quartermaster": 0,
        "large_fort": 0,
    },
}
calculate_scenario(scenario = scenario)
