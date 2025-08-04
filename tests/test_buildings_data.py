from pytest import mark
from collections import Counter
from typing import Any

from modules.buildings import GeoFeature, Resource


@mark.buildings_data
class TestBuildingsData:
    
    def test_all_buildings_have_all_expected_keys(
            self,
            _errors: list,
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
            "required_building",
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
            _errors: list,
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
            _errors: list,
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
            _errors: list,
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
            # ("storage_capacity"),
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
    
    def test_all_required_geo_are_of_expected_value(
            self,
            _errors: list,
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
            _errors: list,
            _buildings: list[dict[str, Any]],
        ) -> None:
        
        for building in _buildings:
            building_id: str = building["id"]
            required_rss: str | None = building["required_rss"]
            
            if not (
                required_rss in [r.value for r in Resource]
                or required_rss is None
            ):
                error: tuple[str, str] = (building_id, required_rss)
                _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_required_buildings_are_building_ids(
            self,
            _errors: list,
            _buildings: list[dict[str, Any]],
        ) -> None:
        all_building_ids: list[str] = [building["id"] for building in _buildings]
        
        for building in _buildings:
            building_id: str = building["id"]
            required_building: list[str] = building["required_building"]
            
            for rb in required_building:
                if rb not in all_building_ids:
                    error: tuple[str, str] = (building_id, rb)
                    _errors.append(error)
        
        assert len(_errors) == 0, _errors
    
    def test_all_replaces_are_building_ids(
            self,
            _errors: list,
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
