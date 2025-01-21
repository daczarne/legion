
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


def create_scenario(pp: list[int], buildings: list[str]) -> dict[str, dict[str, int]]:
    
    scenario_results: dict[str, dict[str, int]] = {
        "food": {
            "prod_pot": pp[0],
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        },
        "ore": {
            "prod_pot": pp[1],
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        },
        "wood": {
            "prod_pot": pp[2],
            "prod_bonus": 0,
            "maintenance": 0,
            "total": 0
        }
    }
    
    if len(buildings) > 9:
        print()
        print("Warning! Too many buildings!")
        return scenario_results
    
    return scenario_results


scenario_1 = create_scenario(
    pp = [100, 150, 75],
    buildings = []
)

print_results(scenario_1)

print("#" * 60)

scenario_2 = create_scenario(
    pp = [115, 10, 0],
    buildings = "a" * 10
)

print_results(scenario_2)
