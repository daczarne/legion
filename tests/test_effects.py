from collections import Counter
from dataclasses import fields
from pytest import mark, raises
from typing import Literal

from modules.effects import EffectBonuses


@mark.effect_bonuses
class TestEffectBonuses:
    
    def test_default_initialization(self) -> None:
        effects: EffectBonuses = EffectBonuses()
        
        assert effects.troop_training == 0
        assert effects.population_growth == 0
        assert effects.intelligence == 0
    
    def test_custom_initialization(self) -> None:
        effects: EffectBonuses = EffectBonuses(
            troop_training = 10,
            population_growth = 20,
            intelligence = 30,
        )
        
        assert effects.troop_training == 10
        assert effects.population_growth == 20
        assert effects.intelligence == 30
    
    def test_iter_returns_keys(self) -> None:
        effects: EffectBonuses = EffectBonuses(
            troop_training = 10,
            population_growth = 20,
            intelligence = 30,
        )
        keys: list[str] = list(iter(effects))
        expected_keys: list[str] = [f.name for f in fields(class_or_instance = EffectBonuses)]
        
        assert Counter(keys) == Counter(expected_keys)
    
    def test_items_returns_key_value_pairs(self) -> None:
        effects: EffectBonuses = EffectBonuses(
            troop_training = 10,
            population_growth = 20,
            intelligence = 30,
        )
        items: dict[str, int] = dict(effects.items())
        
        assert items == {"troop_training": 10, "population_growth": 20, "intelligence": 30}
    
    def test_values_returns_values(self) -> None:
        effects: EffectBonuses = EffectBonuses(
            troop_training = 10,
            population_growth = 20,
            intelligence = 30,
        )
        values: list[int] = list(effects.values())
        
        assert Counter(values) == Counter([10, 20, 30])
    
    @mark.parametrize(
        argnames = "key, expected",
        argvalues = [
            ("troop_training", 11),
            ("population_growth", 22),
            ("intelligence", 33),
        ],
    )
    def test_get_valid_keys(
        self,
        key: Literal["troop_training"] | Literal["population_growth"] | Literal["intelligence"],
        expected: Literal[11] | Literal[22] | Literal[33],
    ) -> None:
        effects: EffectBonuses = EffectBonuses(
            troop_training = 11,
            population_growth = 22,
            intelligence = 33,
        )
        
        assert effects.get(key = key) == expected
    
    def test_get_invalid_key_raises_keyerror(self) -> None:
        effects: EffectBonuses = EffectBonuses(
            troop_training = 10,
            population_growth = 20,
            intelligence = 30,
        )
        
        with raises(expected_exception = KeyError, match = "Invalid effect name: spy"):
            effects.get(key = "spy")
