from dataclasses import dataclass, field

@dataclass
class CityHall:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 1, "ore": 1, "wood": 1}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.25, "ore": 0.25, "wood": 0.25}
    )
    
    max_workers: int = 0


@dataclass
class Farm:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 12, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.0, "ore": 0.0, "wood": 0.0}
    )
    
    max_workers: int = 3


@dataclass
class Vineyard:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 10, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.10, "ore": 0.10, "wood": 0.10}
    )
    
    max_workers: int = 3


@dataclass
class FishingVillage:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 8, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.0, "ore": 0.0, "wood": 0.0}
    )
    
    max_workers: int = 3


@dataclass
class Mine:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 12, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.0, "ore": 0.0, "wood": 0.0}
    )
    
    max_workers: int = 3


@dataclass
class OutcropMine:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 13, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.0, "ore": 0.0, "wood": 0.0}
    )
    
    max_workers: int = 2


@dataclass
class MountainMine:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 20, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.0, "ore": 0.0, "wood": 0.0}
    )
    
    max_workers: int = 2


@dataclass
class Basilica:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 3, "ore": 3, "wood": 3}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.50, "ore": 0.50, "wood": 0.50}
    )
    
    max_workers: int = 1


@dataclass
class FarmersGuild:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 10, "ore": 0, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.50, "ore": 0.0, "wood": 0.0}
    )
    
    max_workers: int = 0


@dataclass
class MinersGuild:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 10, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.0, "ore": 0.50, "wood": 0.0}
    )
    
    max_workers: int = 0


@dataclass
class CarpentersGuild:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 10}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.0, "ore": 0.0, "wood": 0.50}
    )
    
    max_workers: int = 0


@dataclass
class GladiatorSchool:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 8, "wood": 0}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.10, "ore": 0.10, "wood": 0.10}
    )
    
    max_workers: int = 0


@dataclass
class ImperialResidence:
    maintenance_cost: dict[str, int] = field(
        default_factory = lambda: {"food": 8, "ore": 8, "wood": 8}
    )
    
    base_productivity: dict[str, int] = field(
        default_factory = lambda: {"food": 0, "ore": 0, "wood": 0}
    )
    
    productivity_bonus: dict[str, float] = field(
        default_factory = lambda: {"food": 0.10, "ore": 0.10, "wood": 0.10}
    )
    
    max_workers: int = 0



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


city_hall: CityHall = CityHall()
print(city_hall.maintenance_cost.get("food"))

# scenario_1 = create_scenario(
#     pp = [100, 150, 75],
#     buildings = []
# )

# print_results(scenario_1)

# print("#" * 60)

# scenario_2 = create_scenario(
#     pp = [115, 10, 0],
#     buildings = "a" * 10
# )

# print_results(scenario_2)
