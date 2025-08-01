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
            "resource_potential",
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
