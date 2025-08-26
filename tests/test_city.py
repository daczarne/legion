from typing import Literal
from pytest import mark, raises, fixture, FixtureRequest
from collections import Counter

from modules.building import Building, BuildingsCount
from modules.city import _CityData, City, _CityDisplay
from modules.display import DEFAULT_SECTION_COLORS, DisplayConfiguration, DisplaySectionConfiguration
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
            "rock_outcrops",
            "mountains",
            "lakes",
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
        with raises(expected_exception = ValueError, match = "City must include a hall"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [Building(id = "farm")],
            )
    
    def test_city_with_multiple_halls_raises_value_error(self) -> None:
        with raises(expected_exception = ValueError, match = "Too many halls for this city"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "town_hall"),
                ],
            )
    
    def test_city_with_duplicated_halls_raises_value_error(self) -> None:
        with raises(expected_exception = ValueError, match = "Too many halls for this city"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "village_hall"),
                ],
            )
    
    def test_village_with_excess_buildings_raises_value_error(self) -> None:
        with raises(expected_exception = ValueError, match = "Too many buildings"):
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
        with raises(expected_exception = ValueError, match = "Too many buildings"):
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
        with raises(expected_exception = ValueError, match = "Too many buildings"):
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
    
    def test_city_roman_fishing_village_and_outcrop(self) -> None:
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
    
    def test_city_roman_ore_mountains(self) -> None:
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
    
    def test_city_roman_ore_mountain(self) -> None:
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
