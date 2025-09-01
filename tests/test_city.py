from collections import Counter
from pytest import mark, raises, fixture, FixtureRequest

from modules.building import Building, BuildingsCount
from modules.city import _CityData, City, _CityBuildingNode, _CityBuildingsGraph, _CityDisplay
from modules.display import DEFAULT_SECTION_COLORS, DisplayConfiguration, DisplaySectionConfiguration
from modules.exceptions import (
    NoCityHallError,
    TooManyHallsError,
    FortsCannotHaveBuildingsError,
    TooManyBuildingsError,
    NoGarrisonFoundError,
)
from modules.resources import Resource


@mark.city
@mark.cities_data
class TestCitiesData:
    
    def test_all_cities_have_all_expected_keys(
            self,
            _errors: list,
            _cities: list[_CityData],
        ) -> None:
        expected_keys: list[str] = [
            "name",
            "campaign",
            "resource_potentials",
            "geo_features",
            "effects",
            "has_supply_dump",
            "is_fort",
            "garrison",
        ]
        
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            keys_found: list[str] = list(city.keys())
            
            if not Counter(keys_found) == Counter(expected_keys):
                missing_keys: list[str] = list(set(Counter(expected_keys)) - set(Counter(keys_found)))
                extra_keys: list[str] = list(set(Counter(keys_found)) - set(Counter(expected_keys)))
                
                error: dict[str, dict[str, list[str]]] = {
                    f"{campaign} - {city_name}": {
                        "extra_keys": extra_keys,
                        "missing_keys": missing_keys,
                    },
                }
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_each_city_is_unique(
            self,
            _errors: list[str],
            _cities: list[_CityData],
        ) -> None:
        """
        Tests that every `campaign + name` is unique.
        """
        city_names: list[str] = []
        
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            full_name: str = f"{campaign} - {city_name}"
            
            if full_name in city_names:
                _errors.append(full_name)
            else:
                city_names.append(full_name)
        
        assert len(_errors) == 0, _errors
    
    def test_all_campaigns_are_of_expected_value(
            self,
            _errors: list[tuple[str, str]],
            _cities: list[_CityData],
        ) -> None:
        """
        Test that all `campaign` values are of the expected values.
        """
        expected_values: list[str] = [
            "Unification of Italy",
            "Conquest of Britain",
            "Germania",
            "Hispania",
            "Pacifying the North",
            "The Gallic Wars",
        ]
        
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            
            if campaign not in expected_values:
                _errors.append((city_name, campaign))
        
        assert len(_errors) == 0, _errors
    
    def test_all_resource_potentials_have_all_expected_keys(
            self,
            _errors: list,
            _cities: list[_CityData],
        ) -> None:
        expected_keys: list[str] = [
            "food",
            "ore",
            "wood",
        ]
        
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            keys_found: list[str] = list(city["resource_potentials"].keys())
            
            if not Counter(keys_found) == Counter(expected_keys):
                missing_keys: list[str] = list(set(Counter(expected_keys)) - set(Counter(keys_found)))
                extra_keys: list[str] = list(set(Counter(keys_found)) - set(Counter(expected_keys)))
                
                error: dict[str, dict[str, list[str]]] = {
                    f"{campaign} - {city_name}": {
                        "extra_keys": extra_keys,
                        "missing_keys": missing_keys,
                    },
                }
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_resource_potentials_are_int(
            self,
            _errors: list[dict[str, str]],
            _cities: list[_CityData],
        ) -> None:
        """
        Validate `resource_potentials`.
        """
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            
            for resource, potential in city["resource_potentials"].items():
                if not isinstance(potential, int):
                    error: dict[str, str] = {
                        "city": city_name,
                        "campaign": campaign,
                        "resource_potential": f"{resource}: {type(potential)}",
                    }
                    _errors.append(error)
                
                if not 0 <= potential: # type: ignore[reportOperatorIssue]
                    error: dict[str, str] = {
                        "city": city_name,
                        "campaign": campaign,
                        "resource_potential": f"{resource}: {potential}",
                    }
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_geo_features_have_all_expected_keys(
            self,
            _errors: list,
            _cities: list[_CityData],
        ) -> None:
        expected_keys: list[str] = [
            "lakes",
            "rock_outcrops",
            "mountains",
            "forests",
        ]
        
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            keys_found: list[str] = list(city["geo_features"].keys())
            
            if not Counter(keys_found) == Counter(expected_keys):
                missing_keys: list[str] = list(set(Counter(expected_keys)) - set(Counter(keys_found)))
                extra_keys: list[str] = list(set(Counter(keys_found)) - set(Counter(expected_keys)))
                
                error: dict[str, dict[str, list[str]]] = {
                    f"{campaign} - {city_name}": {
                        "extra_keys": extra_keys,
                        "missing_keys": missing_keys,
                    },
                }
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_geo_features_are_int(
            self,
            _errors: list[dict[str, str]],
            _cities: list[_CityData],
        ) -> None:
        """
        Validate `geo_features`.
        """
        
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            
            for geo_feature, qty in city.get("geo_features").items():
                if not isinstance(qty, int):
                    error: dict[str, str] = {
                        "city": city_name,
                        "campaign": campaign,
                        "geo_feature": f"{geo_feature}: {type(qty)}",
                    }
                    _errors.append(error)
                
                if not 0 <= qty: # type: ignore[reportOperatorIssue]
                    error: dict[str, str] = {
                        "city": city_name,
                        "campaign": campaign,
                        "geo_feature": f"{geo_feature}: {qty}",
                    }
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_effects_have_all_expected_keys(
            self,
            _errors: list,
            _cities: list[_CityData],
        ) -> None:
        expected_keys: list[str] = [
            "troop_training",
            "population_growth",
            "intelligence",
        ]
        
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            keys_found: list[str] = list(city["effects"].keys())
            
            if not Counter(keys_found) == Counter(expected_keys):
                missing_keys: list[str] = list(set(Counter(expected_keys)) - set(Counter(keys_found)))
                extra_keys: list[str] = list(set(Counter(keys_found)) - set(Counter(expected_keys)))
                
                error: dict[str, dict[str, list[str]]] = {
                    f"{campaign} - {city_name}": {
                        "extra_keys": extra_keys,
                        "missing_keys": missing_keys,
                    },
                }
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_effects_are_int(
            self,
            _errors: list[dict[str, str]],
            _cities: list[_CityData],
        ) -> None:
        """
        Validates `effects`
        """
        
        for city in _cities:
            city_name: str = city.get("name")
            campaign: str = city.get("campaign")
            
            for effect, size in city.get("effects").items():
                if not isinstance(size, int):
                    error: dict[str, str] = {
                        "city": city_name,
                        "campaign": campaign,
                        "geo_feature": f"{effect}: {type(size)}",
                    }
                    _errors.append(error)
                
                if not 0 <= size: # type: ignore[reportOperatorIssue]
                    error: dict[str, str] = {
                        "city": city_name,
                        "campaign": campaign,
                        "effect": f"{effect}: {size}",
                    }
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors


@mark.city
class TestCity:
    
    @fixture
    def _city(self) -> City:
        sample_city: City = City(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = [
                Building(id = "city_hall"),
                Building(id = "basilica"),
                Building(id = "hospital"),
                Building(id = "training_ground"),
                Building(id = "gladiator_school"),
                Building(id = "stables"),
                Building(id = "bordello"),
                Building(id = "quartermaster"),
                Building(id = "large_fort"),
            ]
        )
        return sample_city
    
    def test_city(self, _city: City) -> None:
        assert _city.campaign == "Unification of Italy"
        assert _city.name == "Roma"
        
        assert _city.effects.city.troop_training == 0
        assert _city.effects.city.population_growth == 0
        assert _city.effects.city.intelligence == 0
        
        assert _city.effects.buildings.troop_training == 30
        assert _city.effects.buildings.population_growth == 100
        assert _city.effects.buildings.intelligence == 10
        
        assert _city.effects.workers.troop_training == 5
        assert _city.effects.workers.population_growth == 170
        assert _city.effects.workers.intelligence == 0
        
        assert _city.effects.total.troop_training == 35
        assert _city.effects.total.population_growth == 270
        assert _city.effects.total.intelligence == 10
        
        assert _city.production.maintenance_costs.food == 62
        assert _city.production.maintenance_costs.ore == 24
        assert _city.production.maintenance_costs.wood == 45
        
        assert _city.production.balance.food == -62
        assert _city.production.balance.ore == -24
        assert _city.production.balance.wood == -45
        
        assert _city.defenses.garrison == "Legion"
        assert _city.defenses.squadrons == 4
        assert _city.defenses.squadron_size == "Huge"
        
        assert _city.focus is None
    
    def test_get_building(self, _city: City) -> None:
        assert isinstance(_city.get_building(id = "city_hall"), Building)
        assert _city.get_building(id = "city_hall").id == "city_hall"
        
        assert isinstance(_city.get_building(id = "quartermaster"), Building)
        assert _city.get_building(id = "quartermaster").id == "quartermaster"
    
    def test_get_building_raises_key_error(self, _city: City) -> None:
        with raises(expected_exception = KeyError):
            _city.get_building(id = "nonexistent_building")
    
    def test_has_building_returns_true_for_existing_building(self, _city: City) -> None:
        assert _city.has_building(id = "stables")
    
    def test_has_building_returns_false_for_nonexistent_building(self, _city: City) -> None:
        assert not _city.has_building(id = "nonexistent_building")
    
    def test_get_hall_returns_the_hall(self, _city: City) -> None:
        assert _city.get_hall().id == "city_hall"
    
    def test_get_buildings_count_by_id(self, _city: City) -> None:
        counts: BuildingsCount = _city.get_buildings_count(by = "id")
        expected_result: BuildingsCount = {
            "city_hall": 1,
            "basilica": 1,
            "hospital": 1,
            "training_ground": 1,
            "gladiator_school": 1,
            "stables": 1,
            "bordello": 1,
            "quartermaster": 1,
            "large_fort": 1,
        }
        
        assert counts == expected_result
    
    def test_get_buildings_count_by_name(self, _city: City) -> None:
        counts: BuildingsCount = _city.get_buildings_count(by = "name")
        expected_result: BuildingsCount = {
            "City hall": 1,
            "Basilica": 1,
            "Hospital": 1,
            "Training ground": 1,
            "Gladiator school": 1,
            "Stables": 1,
            "Bordello": 1,
            "Quartermaster": 1,
            "Large fort": 1,
        }
        
        assert counts == expected_result
    
    def test_city_with_no_hall_raises_value_error(self) -> None:
        with raises(expected_exception = NoCityHallError, match = "City must include a hall."):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [Building(id = "farm")],
            )
    
    def test_city_with_multiple_halls_raises_value_error(self) -> None:
        with raises(expected_exception = TooManyHallsError, match = "Too many halls for this city"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "town_hall"),
                ],
            )
    
    def test_city_with_duplicated_halls_raises_value_error(self) -> None:
        with raises(expected_exception = TooManyHallsError, match = "Too many halls for this city"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "village_hall"),
                ],
            )
    
    def test_village_with_excess_buildings_raises_value_error(self) -> None:
        with raises(expected_exception = TooManyBuildingsError, match = "Too many buildings"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "farm"),
                    Building(id = "mine"),
                    Building(id = "lumber_mill"),
                    Building(id = "shrine"),
                    Building(id = "blacksmith"),
                ],
            )
    
    def test_town_with_excess_buildings_raises_value_error(self) -> None:
        with raises(expected_exception = TooManyBuildingsError, match = "Too many buildings"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "town_hall"),
                    Building(id = "farm"),
                    Building(id = "farm"),
                    Building(id = "mine"),
                    Building(id = "mine"),
                    Building(id = "lumber_mill"),
                    Building(id = "lumber_mill"),
                    Building(id = "shrine"),
                ],
            )
    
    def test_city_with_excess_buildings_raises_value_error(self) -> None:
        with raises(expected_exception = TooManyBuildingsError, match = "Too many buildings"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "city_hall"),
                    Building(id = "farm"),
                    Building(id = "farm"),
                    Building(id = "farm"),
                    Building(id = "mine"),
                    Building(id = "mine"),
                    Building(id = "mine"),
                    Building(id = "lumber_mill"),
                    Building(id = "lumber_mill"),
                    Building(id = "lumber_mill"),
                    Building(id = "shrine"),
                ],
            )
    
    def test_zero_count_buildings_are_ignored(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = {
                "village_hall": 1,
                "mine": 0,
                "lumber_mill": 0,
                "farm": 0,
            }
        )
        
        assert len(city.buildings) == 1
        assert city.get_buildings_count(by = "id") == {"village_hall": 1}


@mark.city
@mark.city_scenarios
class TestCityScenarios:
    
    def test_city_roman_military(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "hospital": 1,
                "training_ground": 1,
                "gladiator_school": 1,
                "stables": 1,
                "bordello": 1,
                "quartermaster": 1,
                "large_fort": 1,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Roma"
        
        assert city.effects.city.troop_training == 0
        assert city.effects.city.population_growth == 0
        assert city.effects.city.intelligence == 0
        
        assert city.effects.buildings.troop_training == 30
        assert city.effects.buildings.population_growth == 100
        assert city.effects.buildings.intelligence == 10
        
        assert city.effects.workers.troop_training == 5
        assert city.effects.workers.population_growth == 170
        assert city.effects.workers.intelligence == 0
        
        assert city.effects.total.troop_training == 35
        assert city.effects.total.population_growth == 270
        assert city.effects.total.intelligence == 10
        
        assert city.production.maintenance_costs.food == 62
        assert city.production.maintenance_costs.ore == 24
        assert city.production.maintenance_costs.wood == 45
        
        assert city.production.balance.food == -62
        assert city.production.balance.ore == -24
        assert city.production.balance.wood == -45
        
        assert city.defenses.garrison == "Legion"
        assert city.defenses.squadrons == 4
        assert city.defenses.squadron_size == "Huge"
        
        assert city.focus is None
    
    def test_city_roman_food(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 5,
                "vineyard": 1,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Roma"
        
        assert city.resource_potentials.food == 125
        assert city.production.base.food == 261
        assert city.production.productivity_bonuses.food == 135
        assert city.production.total.food == 613
        assert city.production.maintenance_costs.food == 14
        assert city.production.balance.food == 599
        assert city.storage.city.food == 100
        assert city.storage.buildings.food == 450
        assert city.storage.warehouse.food == 0
        assert city.storage.supply_dump.food == 0
        assert city.storage.total.food == 550
        assert city.focus == Resource.FOOD
    
    def test_city_roman_fishing_village(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Faesula",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 4,
                "vineyard": 1,
                "fishing_village": 1,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Faesula"
        
        assert city.resource_potentials.food == 90
        assert city.geo_features.lakes == 1
        assert city.production.base.food == 171
        assert city.production.productivity_bonuses.food == 135
        assert city.production.total.food == 401
        assert city.production.maintenance_costs.food == 14
        assert city.production.balance.food == 387
        assert city.storage.city.food == 100
        assert city.storage.buildings.food == 425
        assert city.storage.warehouse.food == 0
        assert city.storage.supply_dump.food == 0
        assert city.storage.total.food == 525
        assert city.focus == Resource.FOOD
    
    def test_city_roman_fishing_village_and_outcrop_mine(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Falerii",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 4,
                "vineyard": 1,
                "outcrop_mine": 1,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Falerii"
        
        assert city.resource_potentials.food == 100
        assert city.resource_potentials.ore == 60
        assert city.geo_features.rock_outcrops == 1
        assert city.production.base.food == 174
        assert city.production.base.ore == 14
        assert city.production.productivity_bonuses.food == 135
        assert city.production.productivity_bonuses.ore == 85
        assert city.production.total.food == 408
        assert city.production.total.ore == 25
        assert city.production.maintenance_costs.food == 14
        assert city.production.maintenance_costs.ore == 4
        assert city.production.balance.food == 394
        assert city.production.balance.ore == 21
        assert city.storage.city.food == 100
        assert city.storage.city.ore == 100
        assert city.storage.buildings.food == 375
        assert city.storage.buildings.ore == 30
        assert city.storage.total.food == 475
        assert city.storage.total.ore == 130
        assert city.focus == Resource.FOOD
    
    def test_city_roman_ore_outcrop_and_mountain_mine(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Caercini",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "outcrop_mine": 1,
                "mountain_mine": 1,
                "large_mine": 4,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Caercini"
        
        assert city.resource_potentials.ore == 125
        assert city.geo_features.rock_outcrops == 1
        assert city.geo_features.mountains == 1
        assert city.production.base.ore == 237
        assert city.production.productivity_bonuses.ore == 125
        assert city.production.total.ore == 533
        assert city.production.maintenance_costs.ore == 14
        assert city.production.balance.ore == 519
        assert city.storage.city.ore == 100
        assert city.storage.buildings.ore == 360
        assert city.storage.warehouse.ore == 0
        assert city.storage.supply_dump.ore == 0
        assert city.storage.total.ore == 460
        assert city.focus == Resource.ORE
    
    def test_city_roman_ore_outcrop_mine(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Caudini",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "large_mine": 5,
                "outcrop_mine": 1,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Caudini"
        
        assert city.resource_potentials.ore == 80
        assert city.geo_features.rock_outcrops == 1
        assert city.production.base.ore == 155
        assert city.production.productivity_bonuses.ore == 125
        assert city.production.total.ore == 348
        assert city.production.maintenance_costs.ore == 14
        assert city.production.balance.ore == 334
        assert city.storage.city.ore == 100
        assert city.storage.buildings.ore == 405
        assert city.storage.total.ore == 505
        assert city.focus == Resource.ORE
    
    def test_city_roman_ore_mountain_mines(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Reate",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 2,
                "large_mine": 4,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Reate"
        
        assert city.resource_potentials.ore == 150
        assert city.geo_features.mountains == 2
        assert city.production.base.ore == 276
        assert city.production.productivity_bonuses.ore == 125
        assert city.production.total.ore == 621
        assert city.production.maintenance_costs.ore == 14
        assert city.production.balance.ore == 607
        assert city.storage.city.ore == 100
        assert city.storage.buildings.ore == 360
        assert city.storage.total.ore == 460
        assert city.focus == Resource.ORE
    
    def test_city_roman_ore_mountain_mine(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Hirpini",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "mountain_mine": 1,
                "large_mine": 5,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Hirpini"
        
        assert city.resource_potentials.ore == 125
        assert city.geo_features.mountains == 1
        assert city.production.base.ore == 250
        assert city.production.productivity_bonuses.ore == 125
        assert city.production.total.ore == 562
        assert city.production.maintenance_costs.ore == 14
        assert city.production.balance.ore == 548
        assert city.storage.city.ore == 100
        assert city.storage.buildings.ore == 405
        assert city.storage.total.ore == 505
        assert city.focus == Resource.ORE
    
    def test_city_roman_ore(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Pentri",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "miners_guild": 1,
                "large_mine": 6,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Pentri"
        
        assert city.resource_potentials.ore == 110
        assert city.production.base.ore == 234
        assert city.production.productivity_bonuses.ore == 125
        assert city.production.total.ore == 526
        assert city.production.maintenance_costs.ore == 14
        assert city.production.balance.ore == 512
        assert city.storage.city.ore == 100
        assert city.storage.buildings.ore == 450
        assert city.storage.total.ore == 550
        assert city.focus == Resource.ORE
    
    def test_city_roman_wood(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Lingones",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "carpenters_guild": 1,
                "large_lumber_mill": 6,
            },
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Lingones"
        
        assert city.resource_potentials.wood == 150
        assert city.geo_features.forests == 1
        assert city.production.base.wood == 324
        assert city.production.productivity_bonuses.wood == 125
        assert city.production.total.wood == 729
        assert city.production.maintenance_costs.wood == 14
        assert city.production.balance.wood == 715
        assert city.storage.city.wood == 100
        assert city.storage.buildings.wood == 450
        assert city.storage.total.wood == 550
        assert city.focus == Resource.WOOD
    
    def test_fort(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Germania",
            name = "Vetera",
            buildings = {},
        )
        
        assert len(city.buildings) == 1
        assert city.get_hall() == Building(id = "fort")
        
        assert city.resource_potentials.food == 0
        assert city.resource_potentials.ore == 0
        assert city.resource_potentials.wood == 0
        
        assert city.geo_features.rock_outcrops == 0
        assert city.geo_features.mountains == 0
        assert city.geo_features.lakes == 0
        assert city.geo_features.forests == 0
        
        assert city.production.total.food == 0
        assert city.production.total.ore == 0
        assert city.production.total.wood == 0
        
        assert city.effects.city.troop_training == 20
        assert city.effects.city.population_growth == 0
        assert city.effects.city.intelligence == 30
        assert city.effects.total.troop_training == 20
        assert city.effects.total.population_growth == 0
        assert city.effects.total.intelligence == 30
        
        assert city.storage.city.food == 150
        assert city.storage.city.ore == 150
        assert city.storage.city.wood == 150
        assert city.storage.total.food == 150
        assert city.storage.total.ore == 150
        assert city.storage.total.wood == 150
        
        assert city.defenses.garrison == "Legion"
        assert city.defenses.squadrons == 3
        assert city.defenses.squadron_size == "Medium"
        
        assert city.focus is None
    
    def test_fort_with_buildings(self) -> None:
        with raises(expected_exception = FortsCannotHaveBuildingsError, match = "Forts cannot have buildings"):
            city: City = City.from_buildings_count(
                campaign = "Germania",
                name = "Vetera",
                buildings = {
                    "farm": 1,
                },
            )


@mark.city
# @mark.city_buildings_graph
@mark.city_buildings_node
class TestCityBuildingNode:
    
    def test_initialization_with_positive_allowed_count(self) -> None:
        building = Building(id = "farm")
        node = _CityBuildingNode(building = building, allowed_count = 2)
        
        assert node.building.id == "farm"
        assert node.allowed_count == 2
        assert node.current_count == 0
        assert node.is_available is True
    
    def test_initialization_with_zero_allowed_count(self) -> None:
        building = Building(id = "fishing_village")
        node = _CityBuildingNode(building = building, allowed_count = 0)
        
        assert node.building.id == "fishing_village"
        assert node.allowed_count == 0
        assert node.current_count == 0
        assert node.is_available is False
    
    def test_increment_count_until_limit(self) -> None:
        building = Building(id = "farm")
        node = _CityBuildingNode(building = building, allowed_count = 2)
        
        node.increment_count()
        assert node.current_count == 1
        assert node.is_available is True
        
        node.increment_count()
        assert node.current_count == 2
        assert node.is_available is False
    
    def test_increment_count_raises_error_if_over_limit(self) -> None:
        building = Building(id = "farm")
        node = _CityBuildingNode(building = building, allowed_count = 1)
        
        node.increment_count()
        assert node.current_count == 1
        assert node.is_available is False
        
        # trying to increment past limit -> should raise ValueError
        with raises(expected_exception = ValueError):
            node.increment_count()
    
    def test_cannot_corrupt_internal_state(self) -> None:
        """Attempting to overwrite internal state should raise AttributeError due to __slots__."""
        building = Building(id = "farm")
        node = _CityBuildingNode(building = building, allowed_count = 1)
        
        with raises(expected_exception = AttributeError):
            # cannot set property
            node.current_count = 10 # type: ignore
        
        with raises(expected_exception = AttributeError):
            # cannot set property
            node.is_available = True # type: ignore
        
        with raises(expected_exception = AttributeError):
            # cannot add new attributes
            node.random_attr = 123 # type: ignore
    
    def test_cannot_change_building_after_init(self) -> None:
        building = Building(id = "farm")
        node = _CityBuildingNode(building = building, allowed_count = 1)
        
        new_building = Building(id = "city_hall")
        
        with raises(expected_exception = AttributeError):
            # cannot change the building
            node.building = new_building # type: ignore 
    
    def test_negative_allowed_count_raises_value_error(self) -> None:
        building = Building(id = "farm")
        with raises(expected_exception = ValueError):
            _CityBuildingNode(building = building, allowed_count = -1)


@mark.city
@mark.city_buildings_graph
class TestCityBuildingsGraph:
    
    @fixture
    def _village_with_no_restrictions(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Bomio",
            buildings = [
                Building(id = "village_hall"),
            ],
        )
        return city
    
    @fixture
    def _town_with_no_restrictions(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Bomio",
            buildings = [
                Building(id = "town_hall"),
            ],
        )
        return city
    
    @fixture
    def _city_with_no_restrictions(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Bomio",
            buildings = [
                Building(id = "city_hall"),
            ],
        )
        return city
    
    @mark.parametrize(
        argnames = ["city", "building", "expected_allowed_count"],
        argvalues = [
            ("_village_with_no_restrictions", "village_hall", 1),
            ("_village_with_no_restrictions", "town_hall", 1),
            ("_village_with_no_restrictions", "city_hall", 1),
            ("_village_with_no_restrictions", "fort", 0),
            ("_village_with_no_restrictions", "farm", 4),
            ("_village_with_no_restrictions", "large_farm", 4),
            ("_village_with_no_restrictions", "vineyard", 1),
            ("_village_with_no_restrictions", "fishing_village", 0),
            ("_village_with_no_restrictions", "farmers_guild", 1),
            ("_village_with_no_restrictions", "mine", 4),
            ("_village_with_no_restrictions", "large_mine", 4),
            ("_village_with_no_restrictions", "outcrop_mine", 0),
            ("_village_with_no_restrictions", "mountain_mine", 0),
            ("_village_with_no_restrictions", "miners_guild", 1),
            ("_village_with_no_restrictions", "lumber_mill", 4),
            ("_village_with_no_restrictions", "large_lumber_mill", 4),
            ("_village_with_no_restrictions", "forest", 0),
            ("_village_with_no_restrictions", "carpenters_guild", 1),
            ("_village_with_no_restrictions", "training_ground", 1),
            ("_village_with_no_restrictions", "gladiator_school", 1),
            ("_village_with_no_restrictions", "bordello", 1),
            ("_village_with_no_restrictions", "stables", 1),
            ("_village_with_no_restrictions", "blacksmith", 1),
            ("_village_with_no_restrictions", "fletcher", 1),
            ("_village_with_no_restrictions", "imperial_residence", 1),
            ("_village_with_no_restrictions", "small_fort", 1),
            ("_village_with_no_restrictions", "medium_fort", 1),
            ("_village_with_no_restrictions", "large_fort", 1),
            ("_village_with_no_restrictions", "barracks", 1),
            ("_village_with_no_restrictions", "quartermaster", 1),
            ("_village_with_no_restrictions", "watch_tower", 1),
            ("_village_with_no_restrictions", "shrine", 1),
            ("_village_with_no_restrictions", "temple", 1),
            ("_village_with_no_restrictions", "basilica", 1),
            ("_village_with_no_restrictions", "bath_house", 1),
            ("_village_with_no_restrictions", "hospital", 1),
            ("_village_with_no_restrictions", "hidden_grove", 0),
            ("_village_with_no_restrictions", "herbalist", 1),
            ("_village_with_no_restrictions", "warehouse", 1),
            ("_village_with_no_restrictions", "small_market", 1),
            ("_village_with_no_restrictions", "large_market", 1),
            ("_village_with_no_restrictions", "hunters_lodge", 0),
            ("_village_with_no_restrictions", "supply_dump", 0),
            ("_town_with_no_restrictions", "village_hall", 1),
            ("_town_with_no_restrictions", "town_hall", 1),
            ("_town_with_no_restrictions", "city_hall", 1),
            ("_town_with_no_restrictions", "fort", 0),
            ("_town_with_no_restrictions", "farm", 6),
            ("_town_with_no_restrictions", "large_farm", 6),
            ("_town_with_no_restrictions", "vineyard", 1),
            ("_town_with_no_restrictions", "fishing_village", 0),
            ("_town_with_no_restrictions", "farmers_guild", 1),
            ("_town_with_no_restrictions", "mine", 6),
            ("_town_with_no_restrictions", "large_mine", 6),
            ("_town_with_no_restrictions", "outcrop_mine", 0),
            ("_town_with_no_restrictions", "mountain_mine", 0),
            ("_town_with_no_restrictions", "miners_guild", 1),
            ("_town_with_no_restrictions", "lumber_mill", 6),
            ("_town_with_no_restrictions", "large_lumber_mill", 6),
            ("_town_with_no_restrictions", "forest", 0),
            ("_town_with_no_restrictions", "carpenters_guild", 1),
            ("_town_with_no_restrictions", "training_ground", 1),
            ("_town_with_no_restrictions", "gladiator_school", 1),
            ("_town_with_no_restrictions", "bordello", 1),
            ("_town_with_no_restrictions", "stables", 1),
            ("_town_with_no_restrictions", "blacksmith", 1),
            ("_town_with_no_restrictions", "fletcher", 1),
            ("_town_with_no_restrictions", "imperial_residence", 1),
            ("_town_with_no_restrictions", "small_fort", 1),
            ("_town_with_no_restrictions", "medium_fort", 1),
            ("_town_with_no_restrictions", "large_fort", 1),
            ("_town_with_no_restrictions", "barracks", 1),
            ("_town_with_no_restrictions", "quartermaster", 1),
            ("_town_with_no_restrictions", "watch_tower", 1),
            ("_town_with_no_restrictions", "shrine", 1),
            ("_town_with_no_restrictions", "temple", 1),
            ("_town_with_no_restrictions", "basilica", 1),
            ("_town_with_no_restrictions", "bath_house", 1),
            ("_town_with_no_restrictions", "hospital", 1),
            ("_town_with_no_restrictions", "hidden_grove", 0),
            ("_town_with_no_restrictions", "herbalist", 1),
            ("_town_with_no_restrictions", "warehouse", 1),
            ("_town_with_no_restrictions", "small_market", 1),
            ("_town_with_no_restrictions", "large_market", 1),
            ("_town_with_no_restrictions", "hunters_lodge", 0),
            ("_town_with_no_restrictions", "supply_dump", 0),
            ("_city_with_no_restrictions", "village_hall", 1),
            ("_city_with_no_restrictions", "town_hall", 1),
            ("_city_with_no_restrictions", "city_hall", 1),
            ("_city_with_no_restrictions", "fort", 0),
            ("_city_with_no_restrictions", "farm", 8),
            ("_city_with_no_restrictions", "large_farm", 8),
            ("_city_with_no_restrictions", "vineyard", 1),
            ("_city_with_no_restrictions", "fishing_village", 0),
            ("_city_with_no_restrictions", "farmers_guild", 1),
            ("_city_with_no_restrictions", "mine", 8),
            ("_city_with_no_restrictions", "large_mine", 8),
            ("_city_with_no_restrictions", "outcrop_mine", 0),
            ("_city_with_no_restrictions", "mountain_mine", 0),
            ("_city_with_no_restrictions", "miners_guild", 1),
            ("_city_with_no_restrictions", "lumber_mill", 8),
            ("_city_with_no_restrictions", "large_lumber_mill", 8),
            ("_city_with_no_restrictions", "forest", 0),
            ("_city_with_no_restrictions", "carpenters_guild", 1),
            ("_city_with_no_restrictions", "training_ground", 1),
            ("_city_with_no_restrictions", "gladiator_school", 1),
            ("_city_with_no_restrictions", "bordello", 1),
            ("_city_with_no_restrictions", "stables", 1),
            ("_city_with_no_restrictions", "blacksmith", 1),
            ("_city_with_no_restrictions", "fletcher", 1),
            ("_city_with_no_restrictions", "imperial_residence", 1),
            ("_city_with_no_restrictions", "small_fort", 1),
            ("_city_with_no_restrictions", "medium_fort", 1),
            ("_city_with_no_restrictions", "large_fort", 1),
            ("_city_with_no_restrictions", "barracks", 1),
            ("_city_with_no_restrictions", "quartermaster", 1),
            ("_city_with_no_restrictions", "watch_tower", 1),
            ("_city_with_no_restrictions", "shrine", 1),
            ("_city_with_no_restrictions", "temple", 1),
            ("_city_with_no_restrictions", "basilica", 1),
            ("_city_with_no_restrictions", "bath_house", 1),
            ("_city_with_no_restrictions", "hospital", 1),
            ("_city_with_no_restrictions", "hidden_grove", 0),
            ("_city_with_no_restrictions", "herbalist", 1),
            ("_city_with_no_restrictions", "warehouse", 1),
            ("_city_with_no_restrictions", "small_market", 1),
            ("_city_with_no_restrictions", "large_market", 1),
            ("_city_with_no_restrictions", "hunters_lodge", 0),
            ("_city_with_no_restrictions", "supply_dump", 0),
        ],
    )
    def test_allowed_count_no_restrictions(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        graph: _CityBuildingsGraph = _CityBuildingsGraph(city = request.getfixturevalue(argname = city))
        assert graph.nodes[building].allowed_count == expected_allowed_count
    
    
    @fixture
    def _village_with_one_lake(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Durobrivae",
            buildings = [
                Building(id = "village_hall"),
            ],
        )
        return city
    
    @fixture
    def _town_with_one_lake(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Durobrivae",
            buildings = [
                Building(id = "town_hall"),
            ],
        )
        return city
    
    @fixture
    def _city_with_one_lake(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Durobrivae",
            buildings = [
                Building(id = "city_hall"),
            ],
        )
        return city
    
    @mark.parametrize(
        argnames = ["city", "building", "expected_allowed_count"],
        argvalues = [
            ("_village_with_one_lake", "farm", 3),
            ("_village_with_one_lake", "large_farm", 3),
            ("_village_with_one_lake", "vineyard", 1),
            ("_village_with_one_lake", "fishing_village", 1),
            ("_village_with_one_lake", "farmers_guild", 1),
            ("_village_with_one_lake", "mine", 3),
            ("_village_with_one_lake", "large_mine", 3),
            ("_village_with_one_lake", "outcrop_mine", 0),
            ("_village_with_one_lake", "mountain_mine", 0),
            ("_village_with_one_lake", "miners_guild", 1),
            ("_village_with_one_lake", "lumber_mill", 3),
            ("_village_with_one_lake", "large_lumber_mill", 3),
            ("_village_with_one_lake", "forest", 0),
            ("_village_with_one_lake", "carpenters_guild", 1),
            ("_village_with_one_lake", "stables", 1),
            ("_village_with_one_lake", "blacksmith", 1),
            ("_village_with_one_lake", "fletcher", 1),
            ("_village_with_one_lake", "hidden_grove", 0),
            ("_village_with_one_lake", "hunters_lodge", 0),
            ("_village_with_one_lake", "supply_dump", 0),
            ("_town_with_one_lake", "farm", 5),
            ("_town_with_one_lake", "large_farm", 5),
            ("_town_with_one_lake", "vineyard", 1),
            ("_town_with_one_lake", "fishing_village", 1),
            ("_town_with_one_lake", "farmers_guild", 1),
            ("_town_with_one_lake", "mine", 5),
            ("_town_with_one_lake", "large_mine", 5),
            ("_town_with_one_lake", "outcrop_mine", 0),
            ("_town_with_one_lake", "mountain_mine", 0),
            ("_town_with_one_lake", "miners_guild", 1),
            ("_town_with_one_lake", "lumber_mill", 5),
            ("_town_with_one_lake", "large_lumber_mill", 5),
            ("_town_with_one_lake", "forest", 0),
            ("_town_with_one_lake", "carpenters_guild", 1),
            ("_town_with_one_lake", "stables", 1),
            ("_town_with_one_lake", "blacksmith", 1),
            ("_town_with_one_lake", "fletcher", 1),
            ("_town_with_one_lake", "hidden_grove", 0),
            ("_town_with_one_lake", "hunters_lodge", 0),
            ("_town_with_one_lake", "supply_dump", 0),
            ("_city_with_one_lake", "farm", 7),
            ("_city_with_one_lake", "large_farm", 7),
            ("_city_with_one_lake", "vineyard", 1),
            ("_city_with_one_lake", "fishing_village", 1),
            ("_city_with_one_lake", "farmers_guild", 1),
            ("_city_with_one_lake", "mine", 7),
            ("_city_with_one_lake", "large_mine", 7),
            ("_city_with_one_lake", "outcrop_mine", 0),
            ("_city_with_one_lake", "mountain_mine", 0),
            ("_city_with_one_lake", "miners_guild", 1),
            ("_city_with_one_lake", "lumber_mill", 7),
            ("_city_with_one_lake", "large_lumber_mill", 7),
            ("_city_with_one_lake", "forest", 0),
            ("_city_with_one_lake", "carpenters_guild", 1),
            ("_city_with_one_lake", "stables", 1),
            ("_city_with_one_lake", "blacksmith", 1),
            ("_city_with_one_lake", "fletcher", 1),
            ("_city_with_one_lake", "hidden_grove", 0),
            ("_city_with_one_lake", "hunters_lodge", 0),
            ("_city_with_one_lake", "supply_dump", 0),
        ],
    )
    def test_allowed_count_one_lake(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        graph: _CityBuildingsGraph = _CityBuildingsGraph(city = request.getfixturevalue(argname = city))
        assert graph.nodes[building].allowed_count == expected_allowed_count
    
    
    @fixture
    def _village_with_one_lake_but_no_food_rss_and_one_mountain(self) -> City:
        city: City = City(
            campaign = "Pacifying the North",
            name = "Olenacum",
            buildings = [
                Building(id = "village_hall"),
            ],
        )
        return city
    
    @fixture
    def _town_with_one_lake_but_no_food_rss_and_one_mountain(self) -> City:
        city: City = City(
            campaign = "Pacifying the North",
            name = "Olenacum",
            buildings = [
                Building(id = "town_hall"),
            ],
        )
        return city
    
    @fixture
    def _city_with_one_lake_but_no_food_rss_and_one_mountain(self) -> City:
        city: City = City(
            campaign = "Pacifying the North",
            name = "Olenacum",
            buildings = [
                Building(id = "city_hall"),
            ],
        )
        return city
    
    @mark.parametrize(
        argnames = ["city", "building", "expected_allowed_count"],
        argvalues = [
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "farm", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "large_farm", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "vineyard", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "fishing_village", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "farmers_guild", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "mine", 2),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "large_mine", 2),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "outcrop_mine", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "mountain_mine", 1),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "miners_guild", 1),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "lumber_mill", 2),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "large_lumber_mill", 2),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "forest", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "carpenters_guild", 1),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "stables", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "blacksmith", 1),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "fletcher", 1),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "hidden_grove", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "hunters_lodge", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "supply_dump", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "farm", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "large_farm", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "vineyard", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "fishing_village", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "farmers_guild", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "mine", 4),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "large_mine", 4),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "outcrop_mine", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "mountain_mine", 1),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "miners_guild", 1),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "lumber_mill", 4),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "large_lumber_mill", 4),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "forest", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "carpenters_guild", 1),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "stables", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "blacksmith", 1),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "fletcher", 1),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "hidden_grove", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "hunters_lodge", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "supply_dump", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "farm", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "large_farm", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "vineyard", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "fishing_village", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "farmers_guild", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "mine", 6),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "large_mine", 6),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "outcrop_mine", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "mountain_mine", 1),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "miners_guild", 1),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "lumber_mill", 6),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "large_lumber_mill", 6),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "forest", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "carpenters_guild", 1),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "stables", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "blacksmith", 1),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "fletcher", 1),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "hidden_grove", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "hunters_lodge", 0),
            ("_city_with_one_lake_but_no_food_rss_and_one_mountain", "supply_dump", 0),
        ],
    )
    def test_allowed_count_one_lake_but_no_food_rss_and_one_mountain(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        graph: _CityBuildingsGraph = _CityBuildingsGraph(city = request.getfixturevalue(argname = city))
        assert graph.nodes[building].allowed_count == expected_allowed_count
    
    
    @fixture
    def _village_with_two_geo_features(self) -> City:
        city: City = City(
            campaign = "Unification of Italy",
            name = "Hernici",
            buildings = [
                Building(id = "village_hall"),
            ],
        )
        return city
    
    @fixture
    def _town_with_two_geo_features(self) -> City:
        city: City = City(
            campaign = "Unification of Italy",
            name = "Hernici",
            buildings = [
                Building(id = "town_hall"),
            ],
        )
        return city
    
    @fixture
    def _city_with_two_geo_features(self) -> City:
        city: City = City(
            campaign = "Unification of Italy",
            name = "Hernici",
            buildings = [
                Building(id = "city_hall"),
            ],
        )
        return city
    
    @mark.parametrize(
        argnames = ["city", "building", "expected_allowed_count"],
        argvalues = [
            ("_village_with_two_geo_features", "farm", 2),
            ("_village_with_two_geo_features", "large_farm", 2),
            ("_village_with_two_geo_features", "vineyard", 1),
            ("_village_with_two_geo_features", "fishing_village", 1),
            ("_village_with_two_geo_features", "farmers_guild", 1),
            ("_village_with_two_geo_features", "mine", 2),
            ("_village_with_two_geo_features", "large_mine", 2),
            ("_village_with_two_geo_features", "outcrop_mine", 1),
            ("_village_with_two_geo_features", "mountain_mine", 0),
            ("_village_with_two_geo_features", "miners_guild", 1),
            ("_village_with_two_geo_features", "lumber_mill", 2),
            ("_village_with_two_geo_features", "large_lumber_mill", 2),
            ("_village_with_two_geo_features", "forest", 0),
            ("_village_with_two_geo_features", "carpenters_guild", 1),
            ("_village_with_two_geo_features", "stables", 1),
            ("_village_with_two_geo_features", "blacksmith", 1),
            ("_village_with_two_geo_features", "fletcher", 1),
            ("_village_with_two_geo_features", "hidden_grove", 0),
            ("_village_with_two_geo_features", "hunters_lodge", 0),
            ("_village_with_two_geo_features", "supply_dump", 0),
            ("_town_with_two_geo_features", "farm", 4),
            ("_town_with_two_geo_features", "large_farm", 4),
            ("_town_with_two_geo_features", "vineyard", 1),
            ("_town_with_two_geo_features", "fishing_village", 1),
            ("_town_with_two_geo_features", "farmers_guild", 1),
            ("_town_with_two_geo_features", "mine", 4),
            ("_town_with_two_geo_features", "large_mine", 4),
            ("_town_with_two_geo_features", "outcrop_mine", 1),
            ("_town_with_two_geo_features", "mountain_mine", 0),
            ("_town_with_two_geo_features", "miners_guild", 1),
            ("_town_with_two_geo_features", "lumber_mill", 4),
            ("_town_with_two_geo_features", "large_lumber_mill", 4),
            ("_town_with_two_geo_features", "forest", 0),
            ("_town_with_two_geo_features", "carpenters_guild", 1),
            ("_town_with_two_geo_features", "stables", 1),
            ("_town_with_two_geo_features", "blacksmith", 1),
            ("_town_with_two_geo_features", "fletcher", 1),
            ("_town_with_two_geo_features", "hidden_grove", 0),
            ("_town_with_two_geo_features", "hunters_lodge", 0),
            ("_town_with_two_geo_features", "supply_dump", 0),
            ("_city_with_two_geo_features", "farm", 6),
            ("_city_with_two_geo_features", "large_farm", 6),
            ("_city_with_two_geo_features", "vineyard", 1),
            ("_city_with_two_geo_features", "fishing_village", 1),
            ("_city_with_two_geo_features", "farmers_guild", 1),
            ("_city_with_two_geo_features", "mine", 6),
            ("_city_with_two_geo_features", "large_mine", 6),
            ("_city_with_two_geo_features", "outcrop_mine", 1),
            ("_city_with_two_geo_features", "mountain_mine", 0),
            ("_city_with_two_geo_features", "miners_guild", 1),
            ("_city_with_two_geo_features", "lumber_mill", 6),
            ("_city_with_two_geo_features", "large_lumber_mill", 6),
            ("_city_with_two_geo_features", "forest", 0),
            ("_city_with_two_geo_features", "carpenters_guild", 1),
            ("_city_with_two_geo_features", "stables", 1),
            ("_city_with_two_geo_features", "blacksmith", 1),
            ("_city_with_two_geo_features", "fletcher", 1),
            ("_city_with_two_geo_features", "hidden_grove", 0),
            ("_city_with_two_geo_features", "hunters_lodge", 0),
            ("_city_with_two_geo_features", "supply_dump", 0),
        ],
    )
    def test_allowed_count_two_geo_features(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        graph: _CityBuildingsGraph = _CityBuildingsGraph(city = request.getfixturevalue(argname = city))
        assert graph.nodes[building].allowed_count == expected_allowed_count
    
    
    @fixture
    def _village_with_forest(self) -> City:
        city: City = City(
            campaign = "Unification of Italy",
            name = "Latins",
            buildings = [
                Building(id = "village_hall"),
            ],
        )
        return city
    
    @fixture
    def _town_with_forest(self) -> City:
        city: City = City(
            campaign = "Unification of Italy",
            name = "Latins",
            buildings = [
                Building(id = "town_hall"),
            ],
        )
        return city
    
    @fixture
    def _city_with_forest(self) -> City:
        city: City = City(
            campaign = "Unification of Italy",
            name = "Latins",
            buildings = [
                Building(id = "city_hall"),
            ],
        )
        return city
    
    @mark.parametrize(
        argnames = ["city", "building", "expected_allowed_count"],
        argvalues = [
            ("_village_with_forest", "farm", 4),
            ("_village_with_forest", "large_farm", 4),
            ("_village_with_forest", "vineyard", 1),
            ("_village_with_forest", "fishing_village", 0),
            ("_village_with_forest", "farmers_guild", 1),
            ("_village_with_forest", "mine", 0),
            ("_village_with_forest", "large_mine", 0),
            ("_village_with_forest", "outcrop_mine", 0),
            ("_village_with_forest", "mountain_mine", 0),
            ("_village_with_forest", "miners_guild", 0),
            ("_village_with_forest", "lumber_mill", 4),
            ("_village_with_forest", "large_lumber_mill", 4),
            ("_village_with_forest", "forest", 1),
            ("_village_with_forest", "carpenters_guild", 1),
            ("_village_with_forest", "stables", 1),
            ("_village_with_forest", "blacksmith", 0),
            ("_village_with_forest", "fletcher", 1),
            ("_village_with_forest", "hidden_grove", 1),
            ("_village_with_forest", "hunters_lodge", 0),
            ("_village_with_forest", "supply_dump", 0),
            ("_town_with_forest", "farm", 6),
            ("_town_with_forest", "large_farm", 6),
            ("_town_with_forest", "vineyard", 1),
            ("_town_with_forest", "fishing_village", 0),
            ("_town_with_forest", "farmers_guild", 1),
            ("_town_with_forest", "mine", 0),
            ("_town_with_forest", "large_mine", 0),
            ("_town_with_forest", "outcrop_mine", 0),
            ("_town_with_forest", "mountain_mine", 0),
            ("_town_with_forest", "miners_guild", 0),
            ("_town_with_forest", "lumber_mill", 6),
            ("_town_with_forest", "large_lumber_mill", 6),
            ("_town_with_forest", "forest", 1),
            ("_town_with_forest", "carpenters_guild", 1),
            ("_town_with_forest", "stables", 1),
            ("_town_with_forest", "blacksmith", 0),
            ("_town_with_forest", "fletcher", 1),
            ("_town_with_forest", "hidden_grove", 1),
            ("_town_with_forest", "hunters_lodge", 0),
            ("_town_with_forest", "supply_dump", 0),
            ("_city_with_forest", "farm", 8),
            ("_city_with_forest", "large_farm", 8),
            ("_city_with_forest", "vineyard", 1),
            ("_city_with_forest", "fishing_village", 0),
            ("_city_with_forest", "farmers_guild", 1),
            ("_city_with_forest", "mine", 0),
            ("_city_with_forest", "large_mine", 0),
            ("_city_with_forest", "outcrop_mine", 0),
            ("_city_with_forest", "mountain_mine", 0),
            ("_city_with_forest", "miners_guild", 0),
            ("_city_with_forest", "lumber_mill", 8),
            ("_city_with_forest", "large_lumber_mill", 8),
            ("_city_with_forest", "forest", 1),
            ("_city_with_forest", "carpenters_guild", 1),
            ("_city_with_forest", "stables", 1),
            ("_city_with_forest", "blacksmith", 0),
            ("_city_with_forest", "fletcher", 1),
            ("_city_with_forest", "hidden_grove", 1),
            ("_city_with_forest", "hunters_lodge", 0),
            ("_city_with_forest", "supply_dump", 0),
        ],
    )
    def test_allowed_count_forest(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        graph: _CityBuildingsGraph = _CityBuildingsGraph(city = request.getfixturevalue(argname = city))
        assert graph.nodes[building].allowed_count == expected_allowed_count
    
    
    @fixture
    def _village_with_supply_dump(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Noviomagus",
            buildings = [
                Building(id = "village_hall"),
            ],
        )
        return city
    
    @fixture
    def _town_with_supply_dump(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Noviomagus",
            buildings = [
                Building(id = "town_hall"),
            ],
        )
        return city
    
    @fixture
    def _city_with_supply_dump(self) -> City:
        city: City = City(
            campaign = "Conquest of Britain",
            name = "Noviomagus",
            buildings = [
                Building(id = "city_hall"),
            ],
        )
        return city
    
    @mark.parametrize(
        argnames = ["city", "building", "expected_allowed_count"],
        argvalues = [
            ("_village_with_supply_dump", "farm", 3),
            ("_village_with_supply_dump", "large_farm", 3),
            ("_village_with_supply_dump", "vineyard", 1),
            ("_village_with_supply_dump", "fishing_village", 0),
            ("_village_with_supply_dump", "farmers_guild", 1),
            ("_village_with_supply_dump", "mine", 0),
            ("_village_with_supply_dump", "large_mine", 0),
            ("_village_with_supply_dump", "outcrop_mine", 0),
            ("_village_with_supply_dump", "mountain_mine", 0),
            ("_village_with_supply_dump", "miners_guild", 0),
            ("_village_with_supply_dump", "lumber_mill", 3),
            ("_village_with_supply_dump", "large_lumber_mill", 3),
            ("_village_with_supply_dump", "forest", 0),
            ("_village_with_supply_dump", "carpenters_guild", 1),
            ("_village_with_supply_dump", "stables", 1),
            ("_village_with_supply_dump", "blacksmith", 0),
            ("_village_with_supply_dump", "fletcher", 1),
            ("_village_with_supply_dump", "hidden_grove", 0),
            ("_village_with_supply_dump", "hunters_lodge", 0),
            ("_village_with_supply_dump", "supply_dump", 1),
            ("_town_with_supply_dump", "farm", 5),
            ("_town_with_supply_dump", "large_farm", 5),
            ("_town_with_supply_dump", "vineyard", 1),
            ("_town_with_supply_dump", "fishing_village", 0),
            ("_town_with_supply_dump", "farmers_guild", 1),
            ("_town_with_supply_dump", "mine", 0),
            ("_town_with_supply_dump", "large_mine", 0),
            ("_town_with_supply_dump", "outcrop_mine", 0),
            ("_town_with_supply_dump", "mountain_mine", 0),
            ("_town_with_supply_dump", "miners_guild", 0),
            ("_town_with_supply_dump", "lumber_mill", 5),
            ("_town_with_supply_dump", "large_lumber_mill", 5),
            ("_town_with_supply_dump", "forest", 0),
            ("_town_with_supply_dump", "carpenters_guild", 1),
            ("_town_with_supply_dump", "stables", 1),
            ("_town_with_supply_dump", "blacksmith", 0),
            ("_town_with_supply_dump", "fletcher", 1),
            ("_town_with_supply_dump", "hidden_grove", 0),
            ("_town_with_supply_dump", "hunters_lodge", 0),
            ("_town_with_supply_dump", "supply_dump", 1),
            ("_city_with_supply_dump", "farm", 7),
            ("_city_with_supply_dump", "large_farm", 7),
            ("_city_with_supply_dump", "vineyard", 1),
            ("_city_with_supply_dump", "fishing_village", 0),
            ("_city_with_supply_dump", "farmers_guild", 1),
            ("_city_with_supply_dump", "mine", 0),
            ("_city_with_supply_dump", "large_mine", 0),
            ("_city_with_supply_dump", "outcrop_mine", 0),
            ("_city_with_supply_dump", "mountain_mine", 0),
            ("_city_with_supply_dump", "miners_guild", 0),
            ("_city_with_supply_dump", "lumber_mill", 7),
            ("_city_with_supply_dump", "large_lumber_mill", 7),
            ("_city_with_supply_dump", "forest", 0),
            ("_city_with_supply_dump", "carpenters_guild", 1),
            ("_city_with_supply_dump", "stables", 1),
            ("_city_with_supply_dump", "blacksmith", 0),
            ("_city_with_supply_dump", "fletcher", 1),
            ("_city_with_supply_dump", "hidden_grove", 0),
            ("_city_with_supply_dump", "hunters_lodge", 0),
            ("_city_with_supply_dump", "supply_dump", 1),
        ],
    )
    def test_allowed_supply_dump(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        graph: _CityBuildingsGraph = _CityBuildingsGraph(city = request.getfixturevalue(argname = city))
        assert graph.nodes[building].allowed_count == expected_allowed_count


@mark.city
@mark.display
@mark.city_display
class TestCityDisplay:
    
    @fixture
    def _military_city(self) -> City:
        sample_city: City = City(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = [
                Building(id = "city_hall"),
                Building(id = "basilica"),
                Building(id = "hospital"),
                Building(id = "training_ground"),
                Building(id = "gladiator_school"),
                Building(id = "stables"),
                Building(id = "bordello"),
                Building(id = "quartermaster"),
                Building(id = "large_fort"),
            ]
        )
        return sample_city
    
    @fixture
    def _production_city(self) -> City:
        sample_city: City = City(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = [
                Building(id = "city_hall"),
                Building(id = "basilica"),
                Building(id = "farmers_guild"),
                Building(id = "vineyard"),
                Building(id = "large_farm"),
                Building(id = "large_farm"),
                Building(id = "large_farm"),
                Building(id = "large_farm"),
                Building(id = "large_farm"),
            ]
        )
        return sample_city
    
    @mark.parametrize(
        argnames = ["city", "section", "expected_height"],
        argvalues = [
            ("_military_city", "city", 2),
            ("_production_city", "city", 2),
            ("_military_city", "buildings", 11),
            ("_production_city", "buildings", 7),
            ("_military_city", "effects", 8),
            ("_production_city", "effects", 8),
            ("_military_city", "production", 8),
            ("_production_city", "production", 8),
            ("_military_city", "storage", 8),
            ("_production_city", "storage", 8),
            ("_military_city", "defenses", 6),
            ("_production_city", "defenses", 6),
            ("_military_city", "unknown", 0),
            ("_production_city", "unknown", 0),
        ],
    )
    def test_calculate_default_section_height(
        self,
        city: str,
        section: str,
        expected_height: int,
        request: FixtureRequest,
    ) -> None:
        city_display = _CityDisplay(city = request.getfixturevalue(argname = city))
        assert city_display._calculate_default_section_height(section = section) == expected_height
    
    @mark.parametrize(argnames = "city", argvalues = ["_military_city", "_production_city"])
    def test_build_default_configuration(
        self,
        city: str,
        request: FixtureRequest,
    ) -> None:
        city_display = _CityDisplay(city = request.getfixturevalue(argname = city))
        config: DisplayConfiguration = city_display._build_default_configuration()
        
        expected_sections: list[str] = ["city", "buildings", "effects", "production", "storage", "defenses"]
        assert Counter(config.keys()) == Counter(expected_sections)
        
        for section in expected_sections:
            section_conf: DisplaySectionConfiguration = config[section]
            assert section_conf["include"] is True # type: ignore
            assert isinstance(section_conf["height"], int) # type: ignore
            assert isinstance(section_conf["color"], str) # type: ignore
        
        assert config["buildings"]["height"] == len(city.buildings) + 2 if "height" in config else True
        
        for section in expected_sections:
            default_color: str = DEFAULT_SECTION_COLORS.get(section, "white")
            assert config[section]["color"] == default_color
    
    @mark.parametrize(argnames = "city", argvalues = ["_military_city", "_production_city"])
    def test_build_configuration_merges_user_config(
        self,
        city: str,
        request: FixtureRequest,
    ) -> None:
        user_conf: DisplayConfiguration = {
            "city": {
                "include": False,
                "color": "white",
            },
            "buildings": {
                "height": 99,
            },
        }
        city_display = _CityDisplay(city = request.getfixturevalue(argname = city), configuration = user_conf)
        config: DisplayConfiguration = city_display._build_configuration()
        
        # User config should override defaults
        assert config["city"]["include"] is False # type: ignore
        assert config["city"]["color"] == "white" # type: ignore
        assert config["buildings"]["height"] == 99 # type: ignore
        
        # Other sections still have defaults
        assert config["effects"]["include"] is True # type: ignore
        assert config["effects"]["color"] == DEFAULT_SECTION_COLORS["effects"] # type: ignore
    
    def test_city_roman_food_with_supply_dump_declared(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Conquest of Britain",
            name = "Anderitum",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 4,
                "vineyard": 1,
            },
        )
        
        assert city.campaign == "Conquest of Britain"
        assert city.name == "Anderitum"
        
        assert city.resource_potentials.food == 100
        assert city.production.base.food == 174
        assert city.production.productivity_bonuses.food == 135
        assert city.production.total.food == 408
        assert city.production.maintenance_costs.food == 4
        assert city.production.balance.food == 404
        assert city.storage.city.food == 100
        assert city.storage.buildings.food == 375
        assert city.storage.warehouse.food == 0
        assert city.storage.supply_dump.food == 300
        assert city.storage.total.food == 775
        assert city.has_supply_dump is True
        assert city.focus == Resource.FOOD
    
    def test_city_roman_food_with_supply_dump_added(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Germania",
            name = "Rogomagnum",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "supply_dump": 1,
                "farmers_guild": 1,
                "vineyard": 1,
                "large_farm": 4,
            },
        )
        
        assert city.campaign == "Germania"
        assert city.name == "Rogomagnum"
        
        assert city.has_supply_dump is True
        assert city.has_building(id = "supply_dump")
    
    def test_city_roman_military_with_supply_dump(self) -> None:
        city: City = City.from_buildings_count(
            campaign = "Germania",
            name = "Rogomagnum",
            buildings = {
                "city_hall": 1,
                "basilica": 1,
                "hospital": 1,
                "training_ground": 1,
                "gladiator_school": 1,
                "supply_dump": 1,
                "bordello": 1,
                "quartermaster": 1,
                "large_fort": 1,
            },
        )
        
        assert city.campaign == "Germania"
        assert city.name == "Rogomagnum"
        
        assert city.has_supply_dump is True
        assert city.has_building(id = "supply_dump")
        
        assert city.effects.city.troop_training == 0
        assert city.effects.city.population_growth == 0
        assert city.effects.city.intelligence == 0
        assert city.effects.buildings.troop_training == 30
        assert city.effects.buildings.population_growth == 200
        assert city.effects.buildings.intelligence == 10
        assert city.effects.workers.troop_training == 5
        assert city.effects.workers.population_growth == 170
        assert city.effects.workers.intelligence == 0
        assert city.effects.total.troop_training == 35
        assert city.effects.total.population_growth == 370
        assert city.effects.total.intelligence == 10
        
        assert city.defenses.garrison == "Equites"
        assert city.defenses.squadrons == 4
        assert city.defenses.squadron_size == "Huge"
