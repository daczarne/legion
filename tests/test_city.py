from pytest import mark
from collections import Counter

from modules.city import CityData, City
from modules.resources import Resource

@mark.cities_data
class TestCitiesData:
    
    def test_all_cities_have_all_expected_keys(
            self,
            _errors: list,
            _cities: list[CityData],
        ) -> None:
        expected_keys: list[str] = [
            "name",
            "campaign",
            "resource_potentials",
            "geo_features",
            "effects",
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
            _cities: list[CityData],
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
            _cities: list[CityData],
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
            _cities: list[CityData],
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
            _cities: list[CityData],
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
            _cities: list[CityData],
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
            _cities: list[CityData],
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
            _cities: list[CityData],
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
            _cities: list[CityData],
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
    
    def test_city_roman_military(self) -> None:
        city: City = City(
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
        
        assert city.city_effects.troop_training == 0
        assert city.city_effects.population_growth == 0
        assert city.city_effects.intelligence == 0
        
        assert city.building_effects.troop_training == 30
        assert city.building_effects.population_growth == 100
        assert city.building_effects.intelligence == 10
        
        assert city.worker_effects.troop_training == 5
        assert city.worker_effects.population_growth == 170
        assert city.worker_effects.intelligence == 0
        
        assert city.total_effects.troop_training == 35
        assert city.total_effects.population_growth == 270
        assert city.total_effects.intelligence == 10
        
        assert city.maintenance_costs.food == 62
        assert city.maintenance_costs.ore == 24
        assert city.maintenance_costs.wood == 45
        
        assert city.balance.food == -62
        assert city.balance.ore == -24
        assert city.balance.wood == -45
        
        assert city.defenses.garrison == "Legion"
        assert city.defenses.squadrons == 4
        assert city.defenses.squadron_size == "Huge"
        
        assert city.focus is None
    
    def test_city_roman_food(self) -> None:
        city: City = City(
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
        assert city.base_production.food == 261
        assert city.productivity_bonuses.food == 135
        assert city.total_production.food == 613
        assert city.maintenance_costs.food == 14
        assert city.balance.food == 599
        assert city.city_storage.food == 100
        assert city.buildings_storage.food == 450
        assert city.warehouse_storage.food == 0
        assert city.supply_dump_storage.food == 0
        assert city.total_storage.food == 550
        assert city.focus == Resource.FOOD
    
    def test_city_roman_fishing_village(self) -> None:
        city: City = City(
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
        assert city.base_production.food == 171
        assert city.productivity_bonuses.food == 135
        assert city.total_production.food == 401
        assert city.maintenance_costs.food == 14
        assert city.balance.food == 387
        assert city.city_storage.food == 100
        assert city.buildings_storage.food == 425
        assert city.warehouse_storage.food == 0
        assert city.supply_dump_storage.food == 0
        assert city.total_storage.food == 525
        assert city.focus == Resource.FOOD
    
    def test_city_roman_fishing_village_and_outcrop(self) -> None:
        city: City = City(
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
        assert city.base_production.food == 174
        assert city.base_production.ore == 14
        assert city.productivity_bonuses.food == 135
        assert city.productivity_bonuses.ore == 85
        assert city.total_production.food == 408
        assert city.total_production.ore == 25
        assert city.maintenance_costs.food == 14
        assert city.maintenance_costs.ore == 4
        assert city.balance.food == 394
        assert city.balance.ore == 21
        assert city.city_storage.food == 100
        assert city.city_storage.ore == 100
        assert city.buildings_storage.food == 375
        assert city.buildings_storage.ore == 30
        assert city.total_storage.food == 475
        assert city.total_storage.ore == 130
        assert city.focus == Resource.FOOD
    
    def test_city_roman_ore_outcrop_and_mountain_mine(self) -> None:
        city: City = City(
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
        assert city.base_production.ore == 237
        assert city.productivity_bonuses.ore == 125
        assert city.total_production.ore == 533
        assert city.maintenance_costs.ore == 14
        assert city.balance.ore == 519
        assert city.city_storage.ore == 100
        assert city.buildings_storage.ore == 360
        assert city.warehouse_storage.ore == 0
        assert city.supply_dump_storage.ore == 0
        assert city.total_storage.ore == 460
        assert city.focus == Resource.ORE
    
    def test_city_roman_ore_outcrop_mine(self) -> None:
        city: City = City(
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
        assert city.base_production.ore == 155
        assert city.productivity_bonuses.ore == 125
        assert city.total_production.ore == 348
        assert city.maintenance_costs.ore == 14
        assert city.balance.ore == 334
        assert city.city_storage.ore == 100
        assert city.buildings_storage.ore == 405
        assert city.total_storage.ore == 505
        assert city.focus == Resource.ORE
    
    def test_city_roman_ore_mountains(self) -> None:
        city: City = City(
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
        assert city.base_production.ore == 276
        assert city.productivity_bonuses.ore == 125
        assert city.total_production.ore == 621
        assert city.maintenance_costs.ore == 14
        assert city.balance.ore == 607
        assert city.city_storage.ore == 100
        assert city.buildings_storage.ore == 360
        assert city.total_storage.ore == 460
        assert city.focus == Resource.ORE
    
    def test_city_roman_ore_mountain(self) -> None:
        city: City = City(
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
        assert city.base_production.ore == 250
        assert city.productivity_bonuses.ore == 125
        assert city.total_production.ore == 562
        assert city.maintenance_costs.ore == 14
        assert city.balance.ore == 548
        assert city.city_storage.ore == 100
        assert city.buildings_storage.ore == 405
        assert city.total_storage.ore == 505
        assert city.focus == Resource.ORE
    
    def test_city_roman_ore(self) -> None:
        city: City = City(
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
        assert city.base_production.ore == 234
        assert city.productivity_bonuses.ore == 125
        assert city.total_production.ore == 526
        assert city.maintenance_costs.ore == 14
        assert city.balance.ore == 512
        assert city.city_storage.ore == 100
        assert city.buildings_storage.ore == 450
        assert city.total_storage.ore == 550
        assert city.focus == Resource.ORE
    
    def test_city_roman_wood(self) -> None:
        city: City = City(
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
        assert city.base_production.wood == 324
        assert city.productivity_bonuses.wood == 125
        assert city.total_production.wood == 729
        assert city.maintenance_costs.wood == 14
        assert city.balance.wood == 715
        assert city.city_storage.wood == 100
        assert city.buildings_storage.wood == 450
        assert city.total_storage.wood == 550
        assert city.focus == Resource.WOOD
