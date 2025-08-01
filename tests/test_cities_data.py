from pytest import mark
from collections import Counter

from modules.city_data import CityData


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
        Test all `geo_features` are integers.
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
