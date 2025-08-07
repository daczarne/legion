# Legion

This project is a script that allows to compare different production configurations for a given city in Legion.

To create a comparison, add the building configurations in the `legion.py` script:

```python
Scenario(
    campaign = "Unification of Italy",
    city = "Lingones",
    buildings_a = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "forest": 1,
        "large_lumber_mill": 5,
    },
    buildings_b = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 6,
    },
).display_results()
```

The terminal output will display a comparison between the two scenarios:

[scenarios](img/scenario.png)
