from collections import Counter
from pytest import mark, raises, fixture, FixtureRequest

from modules.building import Building, BuildingsCount
from modules.city import _CityData, City, _CityDisplay
from modules.display import DisplayConfiguration, DisplaySectionConfiguration, DEFAULT_SECTION_COLORS
from modules.exceptions import (
    CityNotFoundError,
    NoCityHallError,
    MoreThanOneHallTypeError,
    TooManyHallsError,
    FortsCannotHaveBuildingsError,
    TooManyBuildingsError,
    MoreThanOneGuildTypeError,
    UnknownBuildingStaffingStrategyError,
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
    
    def test_city_initialization(self, _roman_military_city: City) -> None:
        assert _roman_military_city.campaign == "Unification of Italy"
        assert _roman_military_city.name == "Roma"
        assert _roman_military_city.hall.id == "city_hall"
        
        assert _roman_military_city.effects.city.troop_training == 0
        assert _roman_military_city.effects.city.population_growth == 0
        assert _roman_military_city.effects.city.intelligence == 0
        
        assert _roman_military_city.effects.buildings.troop_training == 30
        assert _roman_military_city.effects.buildings.population_growth == 100
        assert _roman_military_city.effects.buildings.intelligence == 10
        
        assert _roman_military_city.effects.workers.troop_training == 5
        assert _roman_military_city.effects.workers.population_growth == 170
        assert _roman_military_city.effects.workers.intelligence == 0
        
        assert _roman_military_city.effects.total.troop_training == 35
        assert _roman_military_city.effects.total.population_growth == 270
        assert _roman_military_city.effects.total.intelligence == 10
        
        assert _roman_military_city.production.maintenance_costs.food == 62
        assert _roman_military_city.production.maintenance_costs.ore == 24
        assert _roman_military_city.production.maintenance_costs.wood == 45
        
        assert _roman_military_city.production.balance.food == -62
        assert _roman_military_city.production.balance.ore == -24
        assert _roman_military_city.production.balance.wood == -45
        
        assert _roman_military_city.defenses.garrison == "Legion"
        assert _roman_military_city.defenses.squadrons == 4
        assert _roman_military_city.defenses.squadron_size == "Huge"
        
        assert _roman_military_city.focus is None
    
    def test_city_initialization_from_buildings_count(self, _roman_food_producer_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = _roman_food_producer_buildings,
        )
        
        assert city.campaign == "Unification of Italy"
        assert city.name == "Roma"
        
        assert city.hall.id == "city_hall"
        assert city.is_fort is False
        assert city.has_supply_dump is False
        assert len(city.buildings) == 9
    
    def test_non_existent_city_raises_error(self) -> None:
        with raises(expected_exception = CityNotFoundError):
            city: City = City(
                campaign = "Conquer the World",
                name = "Atlantis",
                buildings = [],
            )
    
    def test_get_building(self, _roman_military_city: City) -> None:
        assert isinstance(_roman_military_city.get_building(id = "city_hall"), Building)
        assert _roman_military_city.get_building(id = "city_hall").id == "city_hall"
        
        assert isinstance(_roman_military_city.get_building(id = "quartermaster"), Building)
        assert _roman_military_city.get_building(id = "quartermaster").id == "quartermaster"
    
    def test_get_building_raises_error(self, _roman_military_city: City) -> None:
        with raises(expected_exception = KeyError):
            _roman_military_city.get_building(id = "nonexistent_building")
    
    def test_has_building_returns_true_for_existing_building(self, _roman_military_city: City) -> None:
        assert _roman_military_city.has_building(id = "stables")
    
    def test_has_building_returns_false_for_nonexistent_building(self, _roman_military_city: City) -> None:
        assert not _roman_military_city.has_building(id = "nonexistent_building")
    
    def test_get_buildings_count_by_id(
            self,
            _roman_military_city: City,
            _roman_military_buildings: BuildingsCount,
        ) -> None:
        counts: BuildingsCount = _roman_military_city.get_buildings_count(by = "id")
        expected_result: BuildingsCount = _roman_military_buildings
        
        assert counts == expected_result
    
    def test_get_buildings_count_by_name(self, _roman_military_city: City) -> None:
        counts: BuildingsCount = _roman_military_city.get_buildings_count(by = "name")
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
    
    def test_city_with_no_hall_raises_error(self) -> None:
        with raises(expected_exception = NoCityHallError):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [],
            )
    
    def test_city_with_multiple_halls_raises_error(self) -> None:
        with raises(expected_exception = MoreThanOneHallTypeError):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "town_hall"),
                ],
            )
    
    def test_city_with_duplicated_halls_raises_error(self) -> None:
        with raises(expected_exception = TooManyHallsError, match = "Too many halls for this city"):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "village_hall"),
                ],
            )


@mark.city
class TestCityAllowedBuildingCounts:
    """
    These tests are separated into a different class simply because of how many of them are needed to test this feature
    thorughly.
    """
    
    def test_village_with_excess_buildings_raises_error(self) -> None:
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
    
    def test_town_with_excess_buildings_raises_error(self) -> None:
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
    
    def test_city_with_excess_buildings_raises_error(self) -> None:
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
            ("_village_with_no_restrictions", "city_hall", 0),
            ("_village_with_no_restrictions", "fort", 0),
            ("_village_with_no_restrictions", "farm", 4),
            ("_village_with_no_restrictions", "large_farm", 4),
            ("_village_with_no_restrictions", "vineyard", 0),
            ("_village_with_no_restrictions", "fishing_village", 0),
            ("_village_with_no_restrictions", "farmers_guild", 0),
            ("_village_with_no_restrictions", "mine", 4),
            ("_village_with_no_restrictions", "large_mine", 4),
            ("_village_with_no_restrictions", "outcrop_mine", 0),
            ("_village_with_no_restrictions", "mountain_mine", 0),
            ("_village_with_no_restrictions", "miners_guild", 0),
            ("_village_with_no_restrictions", "lumber_mill", 4),
            ("_village_with_no_restrictions", "large_lumber_mill", 4),
            ("_village_with_no_restrictions", "forest", 0),
            ("_village_with_no_restrictions", "carpenters_guild", 0),
            ("_village_with_no_restrictions", "training_ground", 0),
            ("_village_with_no_restrictions", "gladiator_school", 0),
            ("_village_with_no_restrictions", "bordello", 0),
            ("_village_with_no_restrictions", "stables", 1),
            ("_village_with_no_restrictions", "blacksmith", 1),
            ("_village_with_no_restrictions", "fletcher", 1),
            ("_village_with_no_restrictions", "imperial_residence", 0),
            ("_village_with_no_restrictions", "small_fort", 1),
            ("_village_with_no_restrictions", "medium_fort", 0),
            ("_village_with_no_restrictions", "large_fort", 0),
            ("_village_with_no_restrictions", "barracks", 0),
            ("_village_with_no_restrictions", "quartermaster", 0),
            ("_village_with_no_restrictions", "watch_tower", 1),
            ("_village_with_no_restrictions", "shrine", 1),
            ("_village_with_no_restrictions", "temple", 0),
            ("_village_with_no_restrictions", "basilica", 0),
            ("_village_with_no_restrictions", "bath_house", 0),
            ("_village_with_no_restrictions", "hospital", 0),
            ("_village_with_no_restrictions", "hidden_grove", 0),
            ("_village_with_no_restrictions", "herbalist", 1),
            ("_village_with_no_restrictions", "warehouse", 1),
            ("_village_with_no_restrictions", "small_market", 1),
            ("_village_with_no_restrictions", "large_market", 1),
            ("_village_with_no_restrictions", "hunters_lodge", 4),
            ("_village_with_no_restrictions", "supply_dump", 0),
            ("_town_with_no_restrictions", "village_hall", 1),
            ("_town_with_no_restrictions", "town_hall", 1),
            ("_town_with_no_restrictions", "city_hall", 1),
            ("_town_with_no_restrictions", "fort", 0),
            ("_town_with_no_restrictions", "farm", 6),
            ("_town_with_no_restrictions", "large_farm", 6),
            ("_town_with_no_restrictions", "vineyard", 1),
            ("_town_with_no_restrictions", "fishing_village", 0),
            ("_town_with_no_restrictions", "farmers_guild", 0),
            ("_town_with_no_restrictions", "mine", 6),
            ("_town_with_no_restrictions", "large_mine", 6),
            ("_town_with_no_restrictions", "outcrop_mine", 0),
            ("_town_with_no_restrictions", "mountain_mine", 0),
            ("_town_with_no_restrictions", "miners_guild", 0),
            ("_town_with_no_restrictions", "lumber_mill", 6),
            ("_town_with_no_restrictions", "large_lumber_mill", 6),
            ("_town_with_no_restrictions", "forest", 0),
            ("_town_with_no_restrictions", "carpenters_guild", 0),
            ("_town_with_no_restrictions", "training_ground", 1),
            ("_town_with_no_restrictions", "gladiator_school", 1),
            ("_town_with_no_restrictions", "bordello", 1),
            ("_town_with_no_restrictions", "stables", 1),
            ("_town_with_no_restrictions", "blacksmith", 1),
            ("_town_with_no_restrictions", "fletcher", 1),
            ("_town_with_no_restrictions", "imperial_residence", 0),
            ("_town_with_no_restrictions", "small_fort", 1),
            ("_town_with_no_restrictions", "medium_fort", 1),
            ("_town_with_no_restrictions", "large_fort", 0),
            ("_town_with_no_restrictions", "barracks", 1),
            ("_town_with_no_restrictions", "quartermaster", 0),
            ("_town_with_no_restrictions", "watch_tower", 1),
            ("_town_with_no_restrictions", "shrine", 1),
            ("_town_with_no_restrictions", "temple", 1),
            ("_town_with_no_restrictions", "basilica", 0),
            ("_town_with_no_restrictions", "bath_house", 1),
            ("_town_with_no_restrictions", "hospital", 1),
            ("_town_with_no_restrictions", "hidden_grove", 0),
            ("_town_with_no_restrictions", "herbalist", 1),
            ("_town_with_no_restrictions", "warehouse", 1),
            ("_town_with_no_restrictions", "small_market", 1),
            ("_town_with_no_restrictions", "large_market", 1),
            ("_town_with_no_restrictions", "hunters_lodge", 6),
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
            ("_city_with_no_restrictions", "hunters_lodge", 6),
            ("_city_with_no_restrictions", "supply_dump", 0),
        ],
    )
    def test_allowed_building_counts_no_restrictions(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        test_city: City = request.getfixturevalue(argname = city)
        allowed_building_counts: BuildingsCount = test_city._calculate_allowed_building_counts()
        assert allowed_building_counts[building] == expected_allowed_count
    
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
            ("_village_with_one_lake", "vineyard", 0),
            ("_village_with_one_lake", "fishing_village", 1),
            ("_village_with_one_lake", "farmers_guild", 0),
            ("_village_with_one_lake", "mine", 3),
            ("_village_with_one_lake", "large_mine", 3),
            ("_village_with_one_lake", "outcrop_mine", 0),
            ("_village_with_one_lake", "mountain_mine", 0),
            ("_village_with_one_lake", "miners_guild", 0),
            ("_village_with_one_lake", "lumber_mill", 3),
            ("_village_with_one_lake", "large_lumber_mill", 3),
            ("_village_with_one_lake", "forest", 0),
            ("_village_with_one_lake", "carpenters_guild", 0),
            ("_village_with_one_lake", "stables", 1),
            ("_village_with_one_lake", "blacksmith", 1),
            ("_village_with_one_lake", "fletcher", 1),
            ("_village_with_one_lake", "hidden_grove", 0),
            ("_village_with_one_lake", "hunters_lodge", 3),
            ("_village_with_one_lake", "supply_dump", 0),
            ("_town_with_one_lake", "farm", 5),
            ("_town_with_one_lake", "large_farm", 5),
            ("_town_with_one_lake", "vineyard", 1),
            ("_town_with_one_lake", "fishing_village", 1),
            ("_town_with_one_lake", "farmers_guild", 0),
            ("_town_with_one_lake", "mine", 5),
            ("_town_with_one_lake", "large_mine", 5),
            ("_town_with_one_lake", "outcrop_mine", 0),
            ("_town_with_one_lake", "mountain_mine", 0),
            ("_town_with_one_lake", "miners_guild", 0),
            ("_town_with_one_lake", "lumber_mill", 5),
            ("_town_with_one_lake", "large_lumber_mill", 5),
            ("_town_with_one_lake", "forest", 0),
            ("_town_with_one_lake", "carpenters_guild", 0),
            ("_town_with_one_lake", "stables", 1),
            ("_town_with_one_lake", "blacksmith", 1),
            ("_town_with_one_lake", "fletcher", 1),
            ("_town_with_one_lake", "hidden_grove", 0),
            ("_town_with_one_lake", "hunters_lodge", 5),
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
            ("_city_with_one_lake", "hunters_lodge", 5),
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
        test_city: City = request.getfixturevalue(argname = city)
        allowed_building_counts: BuildingsCount = test_city._calculate_allowed_building_counts()
        assert allowed_building_counts[building] == expected_allowed_count
    
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
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "miners_guild", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "lumber_mill", 2),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "large_lumber_mill", 2),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "forest", 0),
            ("_village_with_one_lake_but_no_food_rss_and_one_mountain", "carpenters_guild", 0),
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
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "miners_guild", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "lumber_mill", 4),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "large_lumber_mill", 4),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "forest", 0),
            ("_town_with_one_lake_but_no_food_rss_and_one_mountain", "carpenters_guild", 0),
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
        test_city: City = request.getfixturevalue(argname = city)
        allowed_building_counts: BuildingsCount = test_city._calculate_allowed_building_counts()
        assert allowed_building_counts[building] == expected_allowed_count
    
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
            ("_village_with_two_geo_features", "vineyard", 0),
            ("_village_with_two_geo_features", "fishing_village", 1),
            ("_village_with_two_geo_features", "farmers_guild", 0),
            ("_village_with_two_geo_features", "mine", 2),
            ("_village_with_two_geo_features", "large_mine", 2),
            ("_village_with_two_geo_features", "outcrop_mine", 1),
            ("_village_with_two_geo_features", "mountain_mine", 0),
            ("_village_with_two_geo_features", "miners_guild", 0),
            ("_village_with_two_geo_features", "lumber_mill", 2),
            ("_village_with_two_geo_features", "large_lumber_mill", 2),
            ("_village_with_two_geo_features", "forest", 0),
            ("_village_with_two_geo_features", "carpenters_guild", 0),
            ("_village_with_two_geo_features", "stables", 1),
            ("_village_with_two_geo_features", "blacksmith", 1),
            ("_village_with_two_geo_features", "fletcher", 1),
            ("_village_with_two_geo_features", "hidden_grove", 0),
            ("_village_with_two_geo_features", "hunters_lodge", 2),
            ("_village_with_two_geo_features", "supply_dump", 0),
            ("_town_with_two_geo_features", "farm", 4),
            ("_town_with_two_geo_features", "large_farm", 4),
            ("_town_with_two_geo_features", "vineyard", 1),
            ("_town_with_two_geo_features", "fishing_village", 1),
            ("_town_with_two_geo_features", "farmers_guild", 0),
            ("_town_with_two_geo_features", "mine", 4),
            ("_town_with_two_geo_features", "large_mine", 4),
            ("_town_with_two_geo_features", "outcrop_mine", 1),
            ("_town_with_two_geo_features", "mountain_mine", 0),
            ("_town_with_two_geo_features", "miners_guild", 0),
            ("_town_with_two_geo_features", "lumber_mill", 4),
            ("_town_with_two_geo_features", "large_lumber_mill", 4),
            ("_town_with_two_geo_features", "forest", 0),
            ("_town_with_two_geo_features", "carpenters_guild", 0),
            ("_town_with_two_geo_features", "stables", 1),
            ("_town_with_two_geo_features", "blacksmith", 1),
            ("_town_with_two_geo_features", "fletcher", 1),
            ("_town_with_two_geo_features", "hidden_grove", 0),
            ("_town_with_two_geo_features", "hunters_lodge", 4),
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
            ("_city_with_two_geo_features", "hunters_lodge", 4),
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
        test_city: City = request.getfixturevalue(argname = city)
        allowed_building_counts: BuildingsCount = test_city._calculate_allowed_building_counts()
        assert allowed_building_counts[building] == expected_allowed_count
    
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
            ("_village_with_forest", "vineyard", 0),
            ("_village_with_forest", "fishing_village", 0),
            ("_village_with_forest", "farmers_guild", 0),
            ("_village_with_forest", "mine", 0),
            ("_village_with_forest", "large_mine", 0),
            ("_village_with_forest", "outcrop_mine", 0),
            ("_village_with_forest", "mountain_mine", 0),
            ("_village_with_forest", "miners_guild", 0),
            ("_village_with_forest", "lumber_mill", 4),
            ("_village_with_forest", "large_lumber_mill", 4),
            ("_village_with_forest", "forest", 1),
            ("_village_with_forest", "carpenters_guild", 0),
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
            ("_town_with_forest", "farmers_guild", 0),
            ("_town_with_forest", "mine", 0),
            ("_town_with_forest", "large_mine", 0),
            ("_town_with_forest", "outcrop_mine", 0),
            ("_town_with_forest", "mountain_mine", 0),
            ("_town_with_forest", "miners_guild", 0),
            ("_town_with_forest", "lumber_mill", 6),
            ("_town_with_forest", "large_lumber_mill", 6),
            ("_town_with_forest", "forest", 1),
            ("_town_with_forest", "carpenters_guild", 0),
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
        test_city: City = request.getfixturevalue(argname = city)
        allowed_building_counts: BuildingsCount = test_city._calculate_allowed_building_counts()
        assert allowed_building_counts[building] == expected_allowed_count
    
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
            ("_village_with_supply_dump", "vineyard", 0),
            ("_village_with_supply_dump", "fishing_village", 0),
            ("_village_with_supply_dump", "farmers_guild", 0),
            ("_village_with_supply_dump", "mine", 0),
            ("_village_with_supply_dump", "large_mine", 0),
            ("_village_with_supply_dump", "outcrop_mine", 0),
            ("_village_with_supply_dump", "mountain_mine", 0),
            ("_village_with_supply_dump", "miners_guild", 0),
            ("_village_with_supply_dump", "lumber_mill", 3),
            ("_village_with_supply_dump", "large_lumber_mill", 3),
            ("_village_with_supply_dump", "forest", 0),
            ("_village_with_supply_dump", "carpenters_guild", 0),
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
            ("_town_with_supply_dump", "farmers_guild", 0),
            ("_town_with_supply_dump", "mine", 0),
            ("_town_with_supply_dump", "large_mine", 0),
            ("_town_with_supply_dump", "outcrop_mine", 0),
            ("_town_with_supply_dump", "mountain_mine", 0),
            ("_town_with_supply_dump", "miners_guild", 0),
            ("_town_with_supply_dump", "lumber_mill", 5),
            ("_town_with_supply_dump", "large_lumber_mill", 5),
            ("_town_with_supply_dump", "forest", 0),
            ("_town_with_supply_dump", "carpenters_guild", 0),
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
    def test_allowed_count_supply_dump(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        test_city: City = request.getfixturevalue(argname = city)
        allowed_building_counts: BuildingsCount = test_city._calculate_allowed_building_counts()
        assert allowed_building_counts[building] == expected_allowed_count
    
    @fixture
    def _fort(self) -> City:
        city: City = City(
            campaign = "Germania",
            name = "Vetera",
            buildings = [],
        )
        return city
    
    @mark.parametrize(
        argnames = ["city", "building", "expected_allowed_count"],
        argvalues = [
            ("_fort", "village_hall", 0),
            ("_fort", "town_hall", 0),
            ("_fort", "city_hall", 0),
            ("_fort", "fort", 1),
            ("_fort", "farm", 0),
            ("_fort", "large_farm", 0),
            ("_fort", "vineyard", 0),
            ("_fort", "fishing_village", 0),
            ("_fort", "farmers_guild", 0),
            ("_fort", "mine", 0),
            ("_fort", "large_mine", 0),
            ("_fort", "outcrop_mine", 0),
            ("_fort", "mountain_mine", 0),
            ("_fort", "miners_guild", 0),
            ("_fort", "lumber_mill", 0),
            ("_fort", "large_lumber_mill", 0),
            ("_fort", "forest", 0),
            ("_fort", "carpenters_guild", 0),
            ("_fort", "training_ground", 0),
            ("_fort", "gladiator_school", 0),
            ("_fort", "bordello", 0),
            ("_fort", "stables", 0),
            ("_fort", "blacksmith", 0),
            ("_fort", "fletcher", 0),
            ("_fort", "imperial_residence", 0),
            ("_fort", "small_fort", 0),
            ("_fort", "medium_fort", 0),
            ("_fort", "large_fort", 0),
            ("_fort", "barracks", 0),
            ("_fort", "quartermaster", 0),
            ("_fort", "watch_tower", 0),
            ("_fort", "shrine", 0),
            ("_fort", "temple", 0),
            ("_fort", "basilica", 0),
            ("_fort", "bath_house", 0),
            ("_fort", "hospital", 0),
            ("_fort", "hidden_grove", 0),
            ("_fort", "herbalist", 0),
            ("_fort", "warehouse", 0),
            ("_fort", "small_market", 0),
            ("_fort", "large_market", 0),
            ("_fort", "hunters_lodge", 0),
            ("_fort", "supply_dump", 0),
        ],
    )
    def test_allowed_count_fort(
        self,
        city: str,
        building: str,
        expected_allowed_count: int,
        request: FixtureRequest,
    ) -> None:
        test_city: City = request.getfixturevalue(argname = city)
        allowed_building_counts: BuildingsCount = test_city._calculate_allowed_building_counts()
        assert allowed_building_counts[building] == expected_allowed_count


@mark.city
class TestWorkersDistribution:
    
    def test_workers_distribution_roman_military(self, _roman_military_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = _roman_military_buildings,
            staffing_strategy = "effects_first",
        )
        
        assert city.available_workers == 18
        assert city.assigned_workers == 5
        assert city.get_building(id = "basilica").workers == 1
        assert city.get_building(id = "hospital").workers == 3
        assert city.get_building(id = "training_ground").workers == 1
        
        assert city.effects.city.troop_training == 0
        assert city.effects.buildings.troop_training == 30
        assert city.effects.workers.troop_training == 5
        assert city.effects.total.troop_training == 35
        
        assert city.effects.city.population_growth == 0
        assert city.effects.buildings.population_growth == 100
        assert city.effects.workers.population_growth == 170
        assert city.effects.total.population_growth == 270
        
        assert city.effects.city.intelligence == 0
        assert city.effects.buildings.intelligence == 10
        assert city.effects.workers.intelligence == 0
        assert city.effects.total.intelligence == 10
    
    def test_workers_distribution_roman_food_producer(self, _roman_food_producer_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Populonia",
            buildings = _roman_food_producer_buildings,
            staffing_strategy = "production_first",
        )
        
        assert city.available_workers == 18
        assert city.assigned_workers == 18
        assert city.get_building(id = "basilica").workers == 0
        
        assert city.effects.city.troop_training == 0
        assert city.effects.buildings.troop_training == 0
        assert city.effects.workers.troop_training == 0
        assert city.effects.total.troop_training == 0
        
        assert city.effects.city.population_growth == 0
        assert city.effects.buildings.population_growth == 0
        assert city.effects.workers.population_growth == 0
        assert city.effects.total.population_growth == 0
        
        assert city.effects.city.intelligence == 0
        assert city.effects.buildings.intelligence == 0
        assert city.effects.workers.intelligence == 0
        assert city.effects.total.intelligence == 0
    
    def test_workers_distribution_roman_ore_producer(self, _roman_ore_producer_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Germania",
            name = "Varini",
            buildings = _roman_ore_producer_buildings,
            staffing_strategy = "production_first",
        )
        
        assert city.available_workers == 18
        assert city.assigned_workers == 18
        assert city.get_building(id = "basilica").workers == 0
        
        assert city.effects.city.troop_training == 25
        assert city.effects.buildings.troop_training == 0
        assert city.effects.workers.troop_training == 0
        assert city.effects.total.troop_training == 25
        
        assert city.effects.city.population_growth == 0
        assert city.effects.buildings.population_growth == 0
        assert city.effects.workers.population_growth == 0
        assert city.effects.total.population_growth == 0
        
        assert city.effects.city.intelligence == 0
        assert city.effects.buildings.intelligence == 0
        assert city.effects.workers.intelligence == 0
        assert city.effects.total.intelligence == 0
    
    def test_workers_distribution_roman_wood_producer(self, _roman_wood_producer_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Pacifying the North",
            name = "Corda",
            buildings = _roman_wood_producer_buildings,
            staffing_strategy = "production_first",
        )
        
        assert city.available_workers == 18
        assert city.assigned_workers == 18
        assert city.get_building(id = "basilica").workers == 0
        
        assert city.effects.city.troop_training == 10
        assert city.effects.buildings.troop_training == 0
        assert city.effects.workers.troop_training == 0
        assert city.effects.total.troop_training == 10
        
        assert city.effects.city.population_growth == 0
        assert city.effects.buildings.population_growth == 0
        assert city.effects.workers.population_growth == 0
        assert city.effects.total.population_growth == 0
        
        assert city.effects.city.intelligence == 0
        assert city.effects.buildings.intelligence == 0
        assert city.effects.workers.intelligence == 0
        assert city.effects.total.intelligence == 0
    
    def test_production_first_strategy(self, _roman_military_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = _roman_military_buildings,
            staffing_strategy = "production_first",
        )
        
        assert city.get_building(id = "basilica").workers == 1
        assert city.get_building(id = "hospital").workers == 3
        assert city.get_building(id = "training_ground").workers == 1
        
        assert city.available_workers == 18
        assert city.assigned_workers == 5
    
    def test_production_only_strategy(self, _roman_military_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Roma",
            buildings = _roman_military_buildings,
            staffing_strategy = "production_only",
        )
        
        assert city.get_building(id = "basilica").workers == 0
        assert city.get_building(id = "hospital").workers == 0
        assert city.get_building(id = "training_ground").workers == 0
        
        assert city.available_workers == 18
        assert city.assigned_workers == 0
    
    def test_effects_first_strategy(self, _roman_food_producer_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Populonia",
            buildings = _roman_food_producer_buildings,
            staffing_strategy = "effects_first",
        )
        
        assert city.available_workers == 18
        assert city.assigned_workers == 18
        assert city.get_building(id = "basilica").workers == 1
        food_producers: list[int] = [building.workers for building in city.buildings if building.id in ["large_farm", "vineyard"]]
        assert sum(food_producers) == 17
        
        assert city.effects.city.troop_training == 0
        assert city.effects.buildings.troop_training == 0
        assert city.effects.workers.troop_training == 0
        assert city.effects.total.troop_training == 0
        
        assert city.effects.city.population_growth == 0
        assert city.effects.buildings.population_growth == 0
        assert city.effects.workers.population_growth == 50
        assert city.effects.total.population_growth == 50
        
        assert city.effects.city.intelligence == 0
        assert city.effects.buildings.intelligence == 0
        assert city.effects.workers.intelligence == 0
        assert city.effects.total.intelligence == 0
        
        assert city.production.base.food == 300
        assert city.production.productivity_bonuses.food == 135
        assert city.production.total.food == 705
        assert city.production.maintenance_costs.food == 14
        assert city.production.balance.food == 691
    
    def test_effects_only_strategy(self, _roman_food_producer_buildings: BuildingsCount) -> None:
        city: City = City.from_buildings_count(
            campaign = "Unification of Italy",
            name = "Populonia",
            buildings = _roman_food_producer_buildings,
            staffing_strategy = "effects_only",
        )
        
        assert city.available_workers == 18
        assert city.assigned_workers == 1
        assert city.get_building(id = "basilica").workers == 1
        food_producers: list[int] = [building.workers for building in city.buildings if building.id in ["large_farm", "vineyard"]]
        assert sum(food_producers) == 0
        
        assert city.effects.city.troop_training == 0
        assert city.effects.buildings.troop_training == 0
        assert city.effects.workers.troop_training == 0
        assert city.effects.total.troop_training == 0
        
        assert city.effects.city.population_growth == 0
        assert city.effects.buildings.population_growth == 0
        assert city.effects.workers.population_growth == 50
        assert city.effects.total.population_growth == 50
        
        assert city.effects.city.intelligence == 0
        assert city.effects.buildings.intelligence == 0
        assert city.effects.workers.intelligence == 0
        assert city.effects.total.intelligence == 0
        
        assert city.production.base.food == 0
        assert city.production.productivity_bonuses.food == 135
        assert city.production.total.food == 0
        assert city.production.maintenance_costs.food == 14
        assert city.production.balance.food == -14
    
    def test_unknown_staffing_strategy_raises_error(self) -> None:
        with raises(expected_exception = UnknownBuildingStaffingStrategyError):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "city_hall"),
                ],
                staffing_strategy = "military_first",
            )


@mark.city
@mark.city_scenarios
class TestCityScenarios:
    
    def test_roman_military_city(self, _roman_military_city: City) -> None:
        assert _roman_military_city.campaign == "Unification of Italy"
        assert _roman_military_city.name == "Roma"
        
        assert _roman_military_city.hall.id == "city_hall"
        assert _roman_military_city.is_fort is False
        assert _roman_military_city.has_supply_dump is False
        
        assert _roman_military_city.effects.city.troop_training == 0
        assert _roman_military_city.effects.city.population_growth == 0
        assert _roman_military_city.effects.city.intelligence == 0
        
        assert _roman_military_city.effects.buildings.troop_training == 30
        assert _roman_military_city.effects.buildings.population_growth == 100
        assert _roman_military_city.effects.buildings.intelligence == 10
        
        assert _roman_military_city.effects.workers.troop_training == 5
        assert _roman_military_city.effects.workers.population_growth == 170
        assert _roman_military_city.effects.workers.intelligence == 0
        
        assert _roman_military_city.effects.total.troop_training == 35
        assert _roman_military_city.effects.total.population_growth == 270
        assert _roman_military_city.effects.total.intelligence == 10
        
        assert _roman_military_city.production.maintenance_costs.food == 62
        assert _roman_military_city.production.maintenance_costs.ore == 24
        assert _roman_military_city.production.maintenance_costs.wood == 45
        
        assert _roman_military_city.production.balance.food == -62
        assert _roman_military_city.production.balance.ore == -24
        assert _roman_military_city.production.balance.wood == -45
        
        assert _roman_military_city.defenses.garrison == "Legion"
        assert _roman_military_city.defenses.squadrons == 4
        assert _roman_military_city.defenses.squadron_size == "Huge"
        
        assert _roman_military_city.focus is None
    
    def test_roman_food_producer_city(self, _roman_food_producer_city: City) -> None:
        assert _roman_food_producer_city.campaign == "Unification of Italy"
        assert _roman_food_producer_city.name == "Roma"
        
        assert _roman_food_producer_city.hall.id == "city_hall"
        assert _roman_food_producer_city.is_fort is False
        assert _roman_food_producer_city.has_supply_dump is False
        
        assert _roman_food_producer_city.resource_potentials.food == 125
        assert _roman_food_producer_city.production.base.food == 261
        assert _roman_food_producer_city.production.productivity_bonuses.food == 135
        assert _roman_food_producer_city.production.total.food == 613
        assert _roman_food_producer_city.production.maintenance_costs.food == 14
        assert _roman_food_producer_city.production.balance.food == 599
        
        assert _roman_food_producer_city.storage.city.food == 100
        assert _roman_food_producer_city.storage.buildings.food == 450
        assert _roman_food_producer_city.storage.warehouse.food == 0
        assert _roman_food_producer_city.storage.supply_dump.food == 0
        assert _roman_food_producer_city.storage.total.food == 550
        
        assert _roman_food_producer_city.focus == Resource.FOOD
    
    def test_roman_city_with_fishing_village(
            self,
            _roman_city_with_fishing_village: City,
        ) -> None:
        
        assert _roman_city_with_fishing_village.campaign == "Unification of Italy"
        assert _roman_city_with_fishing_village.name == "Faesula"
        
        assert _roman_city_with_fishing_village.hall.id == "city_hall"
        assert _roman_city_with_fishing_village.is_fort is False
        assert _roman_city_with_fishing_village.has_supply_dump is False
        
        assert _roman_city_with_fishing_village.resource_potentials.food == 90
        assert _roman_city_with_fishing_village.geo_features.lakes == 1
        assert _roman_city_with_fishing_village.production.base.food == 171
        assert _roman_city_with_fishing_village.production.productivity_bonuses.food == 135
        assert _roman_city_with_fishing_village.production.total.food == 401
        assert _roman_city_with_fishing_village.production.maintenance_costs.food == 14
        assert _roman_city_with_fishing_village.production.balance.food == 387
        assert _roman_city_with_fishing_village.storage.city.food == 100
        assert _roman_city_with_fishing_village.storage.buildings.food == 425
        assert _roman_city_with_fishing_village.storage.warehouse.food == 0
        assert _roman_city_with_fishing_village.storage.supply_dump.food == 0
        assert _roman_city_with_fishing_village.storage.total.food == 525
        assert _roman_city_with_fishing_village.focus == Resource.FOOD
    
    def test_roman_city_with_fishing_village_and_outcrop_mine(
            self,
            _roman_city_with_fishing_village_and_outcrop_mine: City,
        ) -> None:
        
        assert _roman_city_with_fishing_village_and_outcrop_mine.campaign == "Unification of Italy"
        assert _roman_city_with_fishing_village_and_outcrop_mine.name == "Falerii"
        
        assert _roman_city_with_fishing_village_and_outcrop_mine.hall.id == "city_hall"
        assert _roman_city_with_fishing_village_and_outcrop_mine.is_fort is False
        assert _roman_city_with_fishing_village_and_outcrop_mine.has_supply_dump is False
        
        assert _roman_city_with_fishing_village_and_outcrop_mine.resource_potentials.food == 100
        assert _roman_city_with_fishing_village_and_outcrop_mine.resource_potentials.ore == 60
        assert _roman_city_with_fishing_village_and_outcrop_mine.geo_features.rock_outcrops == 1
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.base.food == 174
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.base.ore == 14
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.productivity_bonuses.food == 135
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.productivity_bonuses.ore == 85
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.total.food == 408
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.total.ore == 25
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.maintenance_costs.food == 14
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.maintenance_costs.ore == 4
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.balance.food == 394
        assert _roman_city_with_fishing_village_and_outcrop_mine.production.balance.ore == 21
        assert _roman_city_with_fishing_village_and_outcrop_mine.storage.city.food == 100
        assert _roman_city_with_fishing_village_and_outcrop_mine.storage.city.ore == 100
        assert _roman_city_with_fishing_village_and_outcrop_mine.storage.buildings.food == 375
        assert _roman_city_with_fishing_village_and_outcrop_mine.storage.buildings.ore == 30
        assert _roman_city_with_fishing_village_and_outcrop_mine.storage.total.food == 475
        assert _roman_city_with_fishing_village_and_outcrop_mine.storage.total.ore == 130
        assert _roman_city_with_fishing_village_and_outcrop_mine.focus == Resource.FOOD
    
    def test_roman_city_with_outcrop_and_mountain_mine(
            self,
            _roman_city_with_outcrop_and_mountain_mine: City,
        ) -> None:
        assert _roman_city_with_outcrop_and_mountain_mine.campaign == "Unification of Italy"
        assert _roman_city_with_outcrop_and_mountain_mine.name == "Caercini"
        
        assert _roman_city_with_outcrop_and_mountain_mine.hall.id == "city_hall"
        assert _roman_city_with_outcrop_and_mountain_mine.is_fort is False
        assert _roman_city_with_outcrop_and_mountain_mine.has_supply_dump is False
        
        assert _roman_city_with_outcrop_and_mountain_mine.resource_potentials.ore == 125
        assert _roman_city_with_outcrop_and_mountain_mine.geo_features.rock_outcrops == 1
        assert _roman_city_with_outcrop_and_mountain_mine.geo_features.mountains == 1
        assert _roman_city_with_outcrop_and_mountain_mine.production.base.ore == 237
        assert _roman_city_with_outcrop_and_mountain_mine.production.productivity_bonuses.ore == 125
        assert _roman_city_with_outcrop_and_mountain_mine.production.total.ore == 533
        assert _roman_city_with_outcrop_and_mountain_mine.production.maintenance_costs.ore == 14
        assert _roman_city_with_outcrop_and_mountain_mine.production.balance.ore == 519
        assert _roman_city_with_outcrop_and_mountain_mine.storage.city.ore == 100
        assert _roman_city_with_outcrop_and_mountain_mine.storage.buildings.ore == 360
        assert _roman_city_with_outcrop_and_mountain_mine.storage.warehouse.ore == 0
        assert _roman_city_with_outcrop_and_mountain_mine.storage.supply_dump.ore == 0
        assert _roman_city_with_outcrop_and_mountain_mine.storage.total.ore == 460
        assert _roman_city_with_outcrop_and_mountain_mine.focus == Resource.ORE
    
    def test_roman_city_with_outcrop_mine(
            self,
            _roman_city_with_outcrop_mine: City,
        ) -> None:
        assert _roman_city_with_outcrop_mine.campaign == "Unification of Italy"
        assert _roman_city_with_outcrop_mine.name == "Caudini"
        
        assert _roman_city_with_outcrop_mine.hall.id == "city_hall"
        assert _roman_city_with_outcrop_mine.is_fort is False
        assert _roman_city_with_outcrop_mine.has_supply_dump is False
        
        assert _roman_city_with_outcrop_mine.resource_potentials.ore == 80
        assert _roman_city_with_outcrop_mine.geo_features.rock_outcrops == 1
        assert _roman_city_with_outcrop_mine.production.base.ore == 155
        assert _roman_city_with_outcrop_mine.production.productivity_bonuses.ore == 125
        assert _roman_city_with_outcrop_mine.production.total.ore == 348
        assert _roman_city_with_outcrop_mine.production.maintenance_costs.ore == 14
        assert _roman_city_with_outcrop_mine.production.balance.ore == 334
        assert _roman_city_with_outcrop_mine.storage.city.ore == 100
        assert _roman_city_with_outcrop_mine.storage.buildings.ore == 405
        assert _roman_city_with_outcrop_mine.storage.total.ore == 505
        assert _roman_city_with_outcrop_mine.focus == Resource.ORE
    
    def test_roman_city_with_mountain_mines(
            self,
            _roman_city_with_mountain_mines: City,
        ) -> None:
        assert _roman_city_with_mountain_mines.campaign == "Unification of Italy"
        assert _roman_city_with_mountain_mines.name == "Reate"
        
        assert _roman_city_with_mountain_mines.hall.id == "city_hall"
        assert _roman_city_with_mountain_mines.is_fort is False
        assert _roman_city_with_mountain_mines.has_supply_dump is False
        
        assert _roman_city_with_mountain_mines.resource_potentials.ore == 150
        assert _roman_city_with_mountain_mines.geo_features.mountains == 2
        assert _roman_city_with_mountain_mines.production.base.ore == 276
        assert _roman_city_with_mountain_mines.production.productivity_bonuses.ore == 125
        assert _roman_city_with_mountain_mines.production.total.ore == 621
        assert _roman_city_with_mountain_mines.production.maintenance_costs.ore == 14
        assert _roman_city_with_mountain_mines.production.balance.ore == 607
        assert _roman_city_with_mountain_mines.storage.city.ore == 100
        assert _roman_city_with_mountain_mines.storage.buildings.ore == 360
        assert _roman_city_with_mountain_mines.storage.total.ore == 460
        assert _roman_city_with_mountain_mines.focus == Resource.ORE
    
    def test_roman_city_with_mountain_mine(
            self,
            _roman_city_with_mountain_mine: City,
        ) -> None:
        assert _roman_city_with_mountain_mine.campaign == "Unification of Italy"
        assert _roman_city_with_mountain_mine.name == "Hirpini"
        
        assert _roman_city_with_mountain_mine.hall.id == "city_hall"
        assert _roman_city_with_mountain_mine.is_fort is False
        assert _roman_city_with_mountain_mine.has_supply_dump is False
        
        assert _roman_city_with_mountain_mine.resource_potentials.ore == 125
        assert _roman_city_with_mountain_mine.geo_features.mountains == 1
        assert _roman_city_with_mountain_mine.production.base.ore == 250
        assert _roman_city_with_mountain_mine.production.productivity_bonuses.ore == 125
        assert _roman_city_with_mountain_mine.production.total.ore == 562
        assert _roman_city_with_mountain_mine.production.maintenance_costs.ore == 14
        assert _roman_city_with_mountain_mine.production.balance.ore == 548
        assert _roman_city_with_mountain_mine.storage.city.ore == 100
        assert _roman_city_with_mountain_mine.storage.buildings.ore == 405
        assert _roman_city_with_mountain_mine.storage.total.ore == 505
        assert _roman_city_with_mountain_mine.focus == Resource.ORE
    
    def test_city_roman_ore(
            self,
            _roman_ore_producer_city: City,
        ) -> None:
        assert _roman_ore_producer_city.campaign == "Unification of Italy"
        assert _roman_ore_producer_city.name == "Pentri"
        
        assert _roman_ore_producer_city.hall.id == "city_hall"
        assert _roman_ore_producer_city.is_fort is False
        assert _roman_ore_producer_city.has_supply_dump is False
        
        assert _roman_ore_producer_city.resource_potentials.ore == 110
        assert _roman_ore_producer_city.production.base.ore == 234
        assert _roman_ore_producer_city.production.productivity_bonuses.ore == 125
        assert _roman_ore_producer_city.production.total.ore == 526
        assert _roman_ore_producer_city.production.maintenance_costs.ore == 14
        assert _roman_ore_producer_city.production.balance.ore == 512
        assert _roman_ore_producer_city.storage.city.ore == 100
        assert _roman_ore_producer_city.storage.buildings.ore == 450
        assert _roman_ore_producer_city.storage.total.ore == 550
        assert _roman_ore_producer_city.focus == Resource.ORE
    
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
        
        assert city.hall.id == "city_hall"
        assert city.is_fort is False
        assert city.has_supply_dump is False
        
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
        
        assert city.hall.id == "fort"
        assert city.is_fort is True
        assert city.has_supply_dump is False
        
        assert city.resource_potentials.food == 0
        assert city.resource_potentials.ore == 0
        assert city.resource_potentials.wood == 0
        
        assert city.geo_features.lakes == 0
        assert city.geo_features.rock_outcrops == 0
        assert city.geo_features.mountains == 0
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
    
    def test_fort_with_buildings_raises_error(self) -> None:
        with raises(expected_exception = FortsCannotHaveBuildingsError, match = "Forts cannot have buildings"):
            city: City = City.from_buildings_count(
                campaign = "Germania",
                name = "Vetera",
                buildings = {
                    "farm": 1,
                },
            )
    
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
        
        assert city.hall.id == "city_hall"
        assert city.is_fort is False
        assert city.has_supply_dump is True
        
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
        
        assert city.hall.id == "city_hall"
        assert city.is_fort is False
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
        
        assert city.hall.id == "city_hall"
        assert city.is_fort is False
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


@mark.city
@mark.city_scenarios
class TestImpossibleScenarios:
    """
    This class tests that city scenarios that are not possible raise errors. These tests are a bit redundant as they
    are already covered by the "allowed counts" tests.
    """
    
    def test_mine_with_no_ore_raises_error(self) -> None:
        with raises(expected_exception = TooManyBuildingsError):
            # Roma has no iron ore so it cannot build mines. It also has no geo features for outcrop or mountain mines.
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "town_hall"),
                    Building(id = "mine"),
                ]
            )
    
    def test_outcrop_mine_with_no_geo_or_rss_raises_error(self) -> None:
        with raises(expected_exception = TooManyBuildingsError):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "town_hall"),
                    Building(id = "outcrop_mine"),
                ]
            )
    
    def test_hunters_lodge_with_no_rss_raises_error(self) -> None:
        with raises(expected_exception = TooManyBuildingsError):
            # Roma has no iron ore so it cannot build hunters' lodges
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "hunters_lodge"),
                ]
            )
    
    def test_vineyard_with_no_town_hall_raises_error(self) -> None:
        with raises(expected_exception = TooManyBuildingsError):
            # Town hall is required for building a vineyard
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "village_hall"),
                    Building(id = "vineyard"),
                ]
            )
    
    def test_multiple_guilds_raises_errors(self) -> None:
        with raises(expected_exception = MoreThanOneGuildTypeError):
            city: City = City(
                campaign = "Unification of Italy",
                name = "Roma",
                buildings = [
                    Building(id = "city_hall"),
                    Building(id = "farmers_guild"),
                    Building(id = "carpenters_guild"),
                ]
            )


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
