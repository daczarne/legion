
results: dict[str, dict[str, int]] = {
    "food": {
        "prod_pot": 100,
        "prod_bonus": 185,
        "maintenance": 24,
        "total": 600
    },
    "ore": {
        "prod_pot": 100,
        "prod_bonus": 185,
        "maintenance": 24,
        "total": 600
    },
    "wood": {
        "prod_pot": 100,
        "prod_bonus": 185,
        "maintenance": 24,
        "total": 600
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

print_results(results)
