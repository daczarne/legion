from pytest import mark, raises

from modules.building import BuildingsCount
from modules.city import City
from modules.exceptions import CitiesFromMultipleCampaignsError, DuplicatedCityError
from modules.kingdom import Kingdom


@mark.kingdom
class TestKingdom:
    
    def test_kingdom(self) -> None:
        kingdom: Kingdom = Kingdom(
            cities = [
                City.from_buildings_count(
                    campaign = "Unification of Italy",
                    name = "Roma",
                    buildings = {"village_hall": 1},
                ),
            ],
        )
        
        assert kingdom.campaign == "Unification of Italy"
        assert kingdom.number_of_cities_in_campaign == 45
        
        assert kingdom.kingdom_total_production.food == 5
        assert kingdom.kingdom_total_production.ore == 5
        assert kingdom.kingdom_total_production.wood == 5
        
        assert kingdom.kingdom_total_storage.food == 350
        assert kingdom.kingdom_total_storage.ore == 350
        assert kingdom.kingdom_total_storage.wood == 350
    
    def test_kingdom_from_list(
            self,
            _roman_military_buildings: BuildingsCount,
            _roman_food_producer_with_warehouse_buildings: BuildingsCount,
            _roman_ore_producer_buildings: BuildingsCount,
            _roman_wood_producer_with_warehouse_buildings: BuildingsCount,
        ) -> None:
        kingdom: Kingdom = Kingdom.from_list(
            data = [
                {
                    "campaign": "Unification of Italy",
                    "name": "Roma",
                    "buildings": _roman_military_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Latins",
                    "buildings": _roman_wood_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Hernici",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "outcrop_mine": 1,
                        "fishing_village": 1,
                        "large_mine": 4,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Caere",
                    "buildings": _roman_wood_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Reate",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "mountain_mine": 2,
                        "large_mine": 4,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Anxur",
                    "buildings": _roman_food_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Aurunci",
                    "buildings": _roman_ore_producer_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Falerii",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "outcrop_mine": 1,
                        "large_mine": 5,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Volsinii",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "carpenters_guild": 1,
                        "warehouse": 1,
                        "fishing_village": 1,
                        "large_lumber_mill": 4,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Populonia",
                    "buildings": _roman_food_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Spoletium",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "mountain_mine": 1,
                        "large_mine": 5,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Clusium",
                    "buildings": _roman_ore_producer_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Pisae",
                    "buildings": _roman_wood_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Sentinum",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "hospital": 1,
                        "training_ground": 1,
                        "gladiator_school": 1,
                        "bordello": 1,
                        "quartermaster": 1,
                        "large_fort": 1,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Faesula",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "fishing_village": 1,
                        "large_mine": 5,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Apuani",
                    "buildings": _roman_wood_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Friniates",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "large_mine": 5,
                        "outcrop_mine": 1,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Sena",
                    "buildings": _roman_food_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Ariminum",
                    "buildings": _roman_ore_producer_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Boii",
                    "buildings": _roman_ore_producer_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Asculum",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "warehouse": 1,
                        "carpenters_guild": 1,
                        "hidden_grove": 1,
                        "large_lumber_mill": 4,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Lingones",
                    "buildings": _roman_wood_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Marrucini",
                    "buildings": _roman_ore_producer_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Carsioli",
                    "buildings": _roman_ore_producer_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Paeligni",
                    "buildings": _roman_food_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Marsi",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "large_mine": 5,
                        "outcrop_mine": 1,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Caercini",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "outcrop_mine": 1,
                        "mountain_mine": 1,
                        "large_mine": 4,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Histonium",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "warehouse": 1,
                        "farmers_guild": 1,
                        "fishing_village": 1,
                        "vineyard": 1,
                        "large_farm": 3,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Apulians",
                    "buildings": _roman_military_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Pentri",
                    "buildings": _roman_ore_producer_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Neapolis",
                    "buildings": _roman_food_producer_with_warehouse_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Capua",
                    "buildings": _roman_ore_producer_buildings,
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Caudini",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "outcrop_mine": 1,
                        "large_mine": 5,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Nuceria",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "fishing_village": 1,
                        "large_mine": 5,
                    },
                },
                {
                    "campaign": "Unification of Italy",
                    "name": "Hirpini",
                    "buildings": {
                        "city_hall": 1,
                        "basilica": 1,
                        "miners_guild": 1,
                        "mountain_mine": 1,
                        "large_mine": 5,
                    },
                },
            ],
        )
        
        assert kingdom.campaign == "Unification of Italy"
        assert kingdom.number_of_cities_in_campaign == 45
        
        assert kingdom.kingdom_total_production.food == 2889
        assert kingdom.kingdom_total_production.ore == 7193
        assert kingdom.kingdom_total_production.wood == 2999
        
        assert kingdom.kingdom_total_storage.food == 9475
        assert kingdom.kingdom_total_storage.ore == 14880
        assert kingdom.kingdom_total_storage.wood == 9525
    
    def test_cities_from_different_campaigns_raises_error(self, _roman_military_buildings: BuildingsCount) -> None:
        with raises(expected_exception = CitiesFromMultipleCampaignsError):
            kingdom: Kingdom = Kingdom.from_list(
                data = [
                    {
                        "campaign": "Unification of Italy",
                        "name": "Roma",
                        "buildings": _roman_military_buildings,
                    },
                    {
                        "campaign": "Conquest of Britain",
                        "name": "Alauna",
                        "buildings": _roman_military_buildings,
                    },
                ],
            )
    
    def test_duplicated_cities_raises_error(
            self,
            _roman_military_buildings: BuildingsCount,
            _roman_food_producer_with_warehouse_buildings: BuildingsCount,
        ) -> None:
        with raises(expected_exception = DuplicatedCityError, match = f"Found duplicated city: Roma"):
            kingdom: Kingdom = Kingdom.from_list(
                data = [
                    {
                        "campaign": "Unification of Italy",
                        "name": "Roma",
                        "buildings": _roman_military_buildings,
                    },
                    {
                        "campaign": "Unification of Italy",
                        "name": "Roma",
                        "buildings": _roman_food_producer_with_warehouse_buildings,
                    },
                ],
            )
    
    def test_calculate_indentations(self) -> None:
        # Toy scenarios
        assert Kingdom._calculate_indentations(cell_value = 1, width = 1) == 0
        assert Kingdom._calculate_indentations(cell_value = 1, width = 2) == 1
        assert Kingdom._calculate_indentations(cell_value = 100, width = 5) == 2
        with raises(expected_exception = AssertionError):
            assert Kingdom._calculate_indentations(cell_value = 1, width = 2) == 0
        
        # Actual scenarios
        assert Kingdom._calculate_indentations(cell_value = 0, width = 10) == 9
        assert Kingdom._calculate_indentations(cell_value = 10, width = 10) == 8
        assert Kingdom._calculate_indentations(cell_value = 100, width = 10) == 7
        with raises(expected_exception = AssertionError):
            assert Kingdom._calculate_indentations(cell_value = 1_000, width = 10) == 6
        assert Kingdom._calculate_indentations(cell_value = 1_000, width = 10) == 5
        assert Kingdom._calculate_indentations(cell_value = 10_000, width = 10) == 4
        assert Kingdom._calculate_indentations(cell_value = 100_000, width = 10) == 3
        with raises(expected_exception = AssertionError):
            assert Kingdom._calculate_indentations(cell_value = 1_000_000, width = 10) == 2
        assert Kingdom._calculate_indentations(cell_value = 1_000_000, width = 10) == 1
        assert Kingdom._calculate_indentations(cell_value = 10_000_000, width = 10) == 0
        assert Kingdom._calculate_indentations(cell_value = 100_000_000, width = 10) == 0
        
        assert Kingdom._calculate_indentations(cell_value = 0, width = 6) == 5
        assert Kingdom._calculate_indentations(cell_value = 10, width = 6) == 4
        assert Kingdom._calculate_indentations(cell_value = 100, width = 6) == 3
        with raises(expected_exception = AssertionError):
            assert Kingdom._calculate_indentations(cell_value = 1_000, width = 6) == 2
        assert Kingdom._calculate_indentations(cell_value = 1_000, width = 6) == 1
        assert Kingdom._calculate_indentations(cell_value = 10_000, width = 6) == 0
        assert Kingdom._calculate_indentations(cell_value = 100_000, width = 6) == 0
