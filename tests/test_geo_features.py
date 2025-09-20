from collections import Counter
from dataclasses import fields
from typing import Literal

from modules.geo_features import GeoFeatures

from pytest import mark, raises


@mark.geo_features
class TestGeoFeatures:
    
    def test_default_initialization(self) -> None:
        geo_features: GeoFeatures = GeoFeatures()
        
        assert geo_features.lakes == 0
        assert geo_features.rock_outcrops == 0
        assert geo_features.mountains == 0
        assert geo_features.forests == 0
    
    def test_custom_initialization(self) -> None:
        geo_features: GeoFeatures = GeoFeatures(
            lakes = 1,
            rock_outcrops = 2,
            mountains = 3,
            forests = 4,
        )
        
        assert geo_features.lakes == 1
        assert geo_features.rock_outcrops == 2
        assert geo_features.mountains == 3
        assert geo_features.forests == 4
    
    def test_iter_returns_keys(self) -> None:
        geo_features: GeoFeatures = GeoFeatures(
            lakes = 1,
            rock_outcrops = 2,
            mountains = 3,
            forests = 4,
        )
        keys: list[str] = list(iter(geo_features))
        expected_keys: list[str] = [f.name for f in fields(class_or_instance = GeoFeatures)]
        
        assert Counter(keys) == Counter(expected_keys)
    
    def test_items_returns_key_value_pairs(self) -> None:
        geo_features: GeoFeatures = GeoFeatures(
            lakes = 1,
            rock_outcrops = 2,
            mountains = 3,
            forests = 4,
        )
        items: dict[str, int] = dict(geo_features.items())
        
        assert items == {"lakes": 1, "rock_outcrops": 2, "mountains": 3, "forests": 4}
    
    def test_values_returns_values(self) -> None:
        geo_features: GeoFeatures = GeoFeatures(
            lakes = 1,
            rock_outcrops = 2,
            mountains = 3,
            forests = 4,
        )
        values: list[int] = list(geo_features.values())
        
        assert Counter(values) == Counter([1, 2, 3, 4])
    
    @mark.parametrize(
        argnames = ["key", "expected"],
        argvalues = [
            ("lakes", 11),
            ("rock_outcrops", 22),
            ("mountains", 33),
            ("forests", 44),
        ],
    )
    def test_get_valid_keys(
        self,
        key: Literal["lakes", "rock_outcrops", "mountains", "forests"],
        expected: Literal[11, 22, 33, 44],
    ) -> None:
        geo_features: GeoFeatures = GeoFeatures(
            lakes = 11,
            rock_outcrops = 22,
            mountains = 33,
            forests = 44,
        )
        
        assert geo_features.get(key = key) == expected
    
    def test_get_invalid_key_raises_error(self) -> None:
        geo_features: GeoFeatures = GeoFeatures(
            lakes = 3,
            rock_outcrops = 1,
            mountains = 2,
            forests = 4,
        )
        
        with raises(expected_exception = KeyError, match = "Invalid geo feature name: gold_deposit"):
            geo_features.get(key = "gold_deposit")
