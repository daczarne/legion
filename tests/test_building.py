from collections import Counter
from typing import Any

from pytest import mark, raises

from modules.building import Building
from modules.effects import EffectBonuses
from modules.exceptions import (
    InsufficientNumberOfWorkersError,
    NegativeNumberOfWorkersError,
    TooManyWorkersError,
    UnknownBuildingError,
)
from modules.geo_features import GeoFeature
from modules.resources import Resource, ResourceCollection


@mark.building
@mark.buildings_data
class TestBuildingsData:
    
    def test_all_buildings_have_all_expected_keys(
            self,
            _errors: list[dict[str, dict[str, list[str]]]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        expected_keys: list[str] = [
            "id",
            "name",
            "building_cost",
            "maintenance_cost",
            "productivity_bonuses",
            "productivity_per_worker",
            "effect_bonuses",
            "effect_bonuses_per_worker",
            "storage_capacity",
            "max_workers",
            "is_buildable",
            "is_deletable",
            "is_upgradeable",
            "required_geo",
            "required_rss",
            "required_hall",
            "required_building",
            "blocked_by_building",
            "replaces",
        ]
        
        for building in _buildings:
            building_id: str = building["id"]
            keys_found: list[str] = list(building.keys())
            
            if not Counter(keys_found) == Counter(expected_keys):
                missing_keys: list[str] = list(set(Counter(expected_keys)) - set(Counter(keys_found)))
                extra_keys: list[str] = list(set(Counter(keys_found)) - set(Counter(expected_keys)))
                
                error: dict[str, dict[str, list[str]]] = {
                    f"{building_id}": {
                        "extra_keys": extra_keys,
                        "missing_keys": missing_keys,
                    },
                }
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_each_building_is_unique(
            self,
            _errors: list[str],
            _buildings: list[dict[str, Any]],
        ) -> None:
        building_ids: list[str] = []
        
        for building in _buildings:
            building_id: str = building["id"]
            
            if building_id in building_ids:
                _errors.append(building_id)
            else:
                building_ids.append(building_id)
        
        assert len(_errors) == 0, _errors
    
    @mark.parametrize(
        argnames = "collection",
        argvalues = [
            ("building_cost"),
            ("maintenance_cost"),
            ("productivity_bonuses"),
            ("productivity_per_worker"),
            ("storage_capacity"),
        ],
    )
    def test_all_building_rss_collections_have_all_expected_keys(
            self,
            collection: str,
            _errors: list[dict[str, dict[str, list[str]]]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        expected_keys: list[str] = [
            "food",
            "ore",
            "wood",
        ]
        
        for building in _buildings:
            building_id: str = building["id"]
            keys_found: list[str] = list(building[collection].keys())
            
            if not Counter(keys_found) == Counter(expected_keys):
                missing_keys: list[str] = list(set(Counter(expected_keys)) - set(Counter(keys_found)))
                extra_keys: list[str] = list(set(Counter(keys_found)) - set(Counter(expected_keys)))
                
                error: dict[str, dict[str, list[str]]] = {
                    f"{building_id}": {
                        "extra_keys": extra_keys,
                        "missing_keys": missing_keys,
                    },
                }
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    @mark.parametrize(
        argnames = "collection",
        argvalues = [
            ("effect_bonuses"),
            ("effect_bonuses_per_worker"),
        ],
    )
    def test_all_building_effects_collections_have_all_expected_keys(
            self,
            collection: str,
            _errors: list[dict[str, dict[str, list[str]]]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        expected_keys: list[str] = [
            "troop_training",
            "population_growth",
            "intelligence",
        ]
        
        for building in _buildings:
            building_id: str = building["id"]
            keys_found: list[str] = list(building[collection].keys())
            
            if not Counter(keys_found) == Counter(expected_keys):
                missing_keys: list[str] = list(set(Counter(expected_keys)) - set(Counter(keys_found)))
                extra_keys: list[str] = list(set(Counter(keys_found)) - set(Counter(expected_keys)))
                
                error: dict[str, dict[str, list[str]]] = {
                    f"{building_id}": {
                        "extra_keys": extra_keys,
                        "missing_keys": missing_keys,
                    },
                }
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    @mark.parametrize(
        argnames = "collection",
        argvalues = [
            ("building_cost"),
            ("maintenance_cost"),
            ("productivity_bonuses"),
            ("productivity_per_worker"),
            ("storage_capacity"),
        ],
    )
    def test_all_rss_collection_values_are_int(
            self,
            collection: str,
            _errors: list[dict[str, str]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        
        for building in _buildings:
            building_id: str = building["id"]
            
            for resource, potential in building[collection].items():
                if not isinstance(potential, int):
                    error: dict[str, str] = {
                        "building_id": building_id,
                        f"{collection}": f"{resource}: {type(potential)}",
                    }
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    @mark.parametrize(
        argnames = "collection",
        argvalues = [
            ("effect_bonuses"),
            ("effect_bonuses_per_worker"),
        ],
    )
    def test_all_effects_collection_values_are_int(
            self,
            collection: str,
            _errors: list[dict[str, str]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        
        for building in _buildings:
            building_id: str = building["id"]
            
            for effect, effect_value in building[collection].items():
                if not isinstance(effect_value, int):
                    error: dict[str, str] = {
                        "building_id": building_id,
                        f"{collection}": f"{effect}: {type(effect_value)}",
                    }
                    _errors.append(error)
                
                if not 0 <= effect_value:
                    error: dict[str, str] = {
                        "building_id": building_id,
                        f"{collection}": f"{effect}: {effect_value}",
                    }
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_required_geo_are_of_expected_value(
            self,
            _errors: list[tuple[str, str]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        
        for building in _buildings:
            building_id: str = building["id"]
            required_geo: str | None = building["required_geo"]
            
            if not (
                required_geo in [gf.value for gf in GeoFeature]
                or required_geo is None
            ):
                error: tuple[str, str] = (building_id, required_geo)
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_required_rss_are_of_expected_value(
            self,
            _errors: list[tuple[str, str]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        
        for building in _buildings:
            building_id: str = building["id"]
            required_rss: list[str] = building["required_rss"]
            
            for rss in required_rss:
                if rss not in [r.value for r in Resource]:
                    error: tuple[str, str] = (building_id, rss)
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_required_halls_are_halls_or_none(
            self,
            _errors: list[tuple[str, str]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        halls: list[str | None] = [None, "fort", "village_hall", "town_hall", "city_hall"]
        
        for building in _buildings:
            building_id: str = building["id"]
            required_hall: str = building["required_hall"]
            
            if required_hall not in halls:
                error: tuple[str, str] = (building_id, required_hall)
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_required_buildings_are_building_ids(
            self,
            _errors: list[tuple[str, str]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        all_building_ids: list[str] = [building["id"] for building in _buildings]
        
        for building in _buildings:
            building_id: str = building["id"]
            required_building: list[str] = building["required_building"]
            
            for requirement in required_building:
                if requirement not in all_building_ids:
                    error: tuple[str, str] = (building_id, requirement)
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_blocked_by_buildings_are_building_ids(
            self,
            _errors: list[tuple[str, str]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        all_building_ids: list[str] = [building["id"] for building in _buildings]
        
        for building in _buildings:
            building_id: str = building["id"]
            blocked_by_building: list[str] = building["blocked_by_building"]
            
            for blocker in blocked_by_building:
                if blocker not in all_building_ids:
                    error: tuple[str, str] = (building_id, blocker)
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_replaces_are_building_ids(
            self,
            _errors: list[tuple[str, str]],
            _buildings: list[dict[str, Any]],
        ) -> None:
        all_building_ids: list[str] = [building["id"] for building in _buildings]
        
        for building in _buildings:
            building_id: str = building["id"]
            replaces: str | None = building["replaces"]
            
            if not (
                replaces in all_building_ids
                or replaces is None
            ):
                error: tuple[str, str] = (building_id, replaces)
                _errors.append(error)
        
        assert len(_errors) == 0, _errors


@mark.building
class TestBuilding:
    
    def test_building_instantiation(self) -> None:
        city_hall: Building = Building(id = "city_hall")
        
        assert city_hall.id == "city_hall"
        assert city_hall.name == "City hall"
        assert isinstance(city_hall.building_cost, ResourceCollection)
        assert city_hall.building_cost == ResourceCollection(food = 350, ore = 100, wood = 350)
        assert isinstance(city_hall.maintenance_cost, ResourceCollection)
        assert city_hall.maintenance_cost == ResourceCollection(food = 1, ore = 1, wood = 1)
        assert isinstance(city_hall.productivity_bonuses, ResourceCollection)
        assert city_hall.productivity_bonuses == ResourceCollection(food = 25, ore = 25, wood = 25)
        assert isinstance(city_hall.productivity_per_worker, ResourceCollection)
        assert city_hall.productivity_per_worker == ResourceCollection(food = 0, ore = 0, wood = 0)
        assert isinstance(city_hall.effect_bonuses, EffectBonuses)
        assert city_hall.effect_bonuses == EffectBonuses(troop_training = 0, population_growth = 0, intelligence = 0)
        assert isinstance(city_hall.effect_bonuses_per_worker, EffectBonuses)
        assert city_hall.effect_bonuses_per_worker == EffectBonuses(troop_training = 0, population_growth = 0, intelligence = 0)
        assert isinstance(city_hall.storage_capacity, ResourceCollection)
        assert city_hall.storage_capacity == ResourceCollection(food = 100, ore = 100, wood = 100)
        assert city_hall.max_workers == 0
        assert city_hall.is_buildable == True
        assert city_hall.is_deletable == False
        assert city_hall.is_upgradeable == False
        assert city_hall.required_geo is None
        assert len(city_hall.required_rss) == 0
        assert city_hall.required_hall == "town_hall"
        assert city_hall.required_building == ["town_hall"]
        assert city_hall.replaces == "town_hall"
        assert city_hall.workers == 0
    
    def test_creating_nonexistent_building(self) -> None:
        with raises(expected_exception = UnknownBuildingError):
            Building(id = "nonexistent_building")
    
    def test_building_requirements(self) -> None:
        mountain_mine: Building = Building(id = "mountain_mine")
        
        assert mountain_mine.id == "mountain_mine"
        assert mountain_mine.name == "Mountain mine"
        assert mountain_mine.required_hall == "village_hall"
        assert mountain_mine.required_geo == GeoFeature.MOUNTAIN
        assert mountain_mine.required_rss == [Resource.ORE]
        assert mountain_mine.max_workers == 1
    
    def test_building_workers_logics(self) -> None:
        large_mine: Building = Building(id = "large_mine")
        
        assert large_mine.id == "large_mine"
        assert large_mine.name == "Large mine"
        assert large_mine.required_hall == "village_hall"
        assert large_mine.required_rss == [Resource.ORE]
        assert large_mine.max_workers == 3
        assert large_mine.workers == 0
        
        large_mine.add_workers(qty = 2)
        assert large_mine.workers == 2
        
        large_mine.remove_workers(qty = 1)
        assert large_mine.workers == 1
        
        large_mine.set_workers(qty = 3)
        assert large_mine.workers == 3
        
        with raises(expected_exception = TooManyWorkersError):
            large_mine.add_workers(qty = 1)
        
        with raises(expected_exception = NegativeNumberOfWorkersError):
            large_mine.add_workers(qty = -1)
        
        with raises(expected_exception = InsufficientNumberOfWorkersError):
            large_mine.remove_workers(qty = 4)
        
        with raises(expected_exception = NegativeNumberOfWorkersError):
            large_mine.remove_workers(qty = -1)
        
        with raises(expected_exception = TooManyWorkersError):
            large_mine.set_workers(qty = 10)
        
        with raises(expected_exception = NegativeNumberOfWorkersError):
            large_mine.set_workers(qty = -1)


@mark.building
@mark.building_scenarios
class TestBuildingScenarios:
    
    def test_farmers_guild(self) -> None:
        farmers_guild: Building = Building(id = "farmers_guild")
        
        assert farmers_guild.required_hall == "city_hall"
        assert farmers_guild.required_building == ["large_farm"]
        assert farmers_guild.required_rss == [Resource.FOOD]
    
    def test_stables(self) -> None:
        stables: Building = Building(id = "stables")
        
        assert stables.required_hall == "village_hall"
        assert stables.required_building == ["farm", "large_farm", "vineyard", "fishing_village"]
        assert len(stables.required_rss) == 0
