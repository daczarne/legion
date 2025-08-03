from pytest import mark
from collections import Counter

from modules.city_data import CityData


@mark.buildings_data
class TestBuildingsData:
    
    def test_all_buildings_have_all_expected_keys(
            self,
            _errors: list,
            _buildings,
        ) -> None:
        assert len(_errors) == 0, _errors
