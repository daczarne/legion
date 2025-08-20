from collections import Counter
from dataclasses import fields
from pytest import mark, raises
from typing import Literal

from modules.resources import ResourceCollection


@mark.resources
class TestResourceCollection:
    
    def test_default_initialization(self) -> None:
        rss_collection: ResourceCollection = ResourceCollection()
        
        assert rss_collection.food == 0
        assert rss_collection.ore == 0
        assert rss_collection.wood == 0
    
    def test_custom_initialization(self) -> None:
        rss_collection: ResourceCollection = ResourceCollection(
            food = 100,
            ore = 110,
            wood = 120,
        )
        
        assert rss_collection.food == 100
        assert rss_collection.ore == 110
        assert rss_collection.wood == 120
    
    def test_iter_returns_keys(self) -> None:
        rss_collection: ResourceCollection = ResourceCollection(
            food = 10,
            ore = 20,
            wood = 30,
        )
        keys: list[str] = list(iter(rss_collection))
        expected_keys: list[str] = [f.name for f in fields(class_or_instance = ResourceCollection)]
        
        assert Counter(keys) == Counter(expected_keys)
    
    def test_items_returns_key_value_pairs(self) -> None:
        rss_collection: ResourceCollection = ResourceCollection(
            food = 7,
            ore = 8,
            wood = 9,
        )
        items: dict[str, int] = dict(rss_collection.items())
        
        assert items == {"food": 7, "ore": 8, "wood": 9}
    
    def test_values_returns_values(self) -> None:
        rss_collection: ResourceCollection = ResourceCollection(
            food = 1,
            ore = 2,
            wood = 3,
        )
        values: list[int] = list(rss_collection.values())
        
        assert Counter(values) == Counter([1, 2, 3])
    
    @mark.parametrize(
        argnames = "key, expected",
        argvalues = [
            ("food", 11),
            ("ore", 22),
            ("wood", 33),
        ],
    )
    def test_get_valid_keys(
        self,
        key: Literal["food"] | Literal["ore"] | Literal["wood"],
        expected: Literal[11] | Literal[22] | Literal[33],
    ) -> None:
        rss_collection: ResourceCollection = ResourceCollection(
            food = 11,
            ore = 22,
            wood = 33,
        )
        
        assert rss_collection.get(key = key) == expected
    
    def test_get_invalid_key_raises_keyerror(self) -> None:
        rss_collection: ResourceCollection = ResourceCollection(
            food = 1,
            ore = 2,
            wood = 3,
        )
        
        with raises(expected_exception = KeyError, match = "Invalid resource name: gold"):
            rss_collection.get(key = "gold")
