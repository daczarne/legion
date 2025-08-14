# Legion

This project is a collection of classes that help you organize your kingdom in Legion.

## The `City` class

The `City` class is the backbone of it all. Given a city (identified by campaign and city name) and the configuration
of buildings that you'd like to build in it, it displays the information about the city (it's effects, production,
storage, and defenses).

```python
from modules.display import CityDisplay
from modules.city import City

city: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "farmers_guild": 1,
        "large_farm": 5,
        "vineyard": 1,
    },
)

CityDisplay(city = city).display_city_results()
```

![full city](img/city_1.png)

You can pass a `DisplayConfiguration` dictionary to the `CityDisplay` class to control how the city is displayed. For
example, you could want the Defenses section to be omited and the Production section to be shown in yellow.

```python
display_configuration: DisplayConfiguration = {
    "production": {
        "color": "yellow"
    },
    "defenses": {
        "include": False,
    },
}

CityDisplay(city = city, configuration = display_configuration).display_city_results()
```

![partial city](img/city_2.png)

## The `Scenario` class

To create a comparison, add the city configurations in the `legion.py` script:

```python
from modules.scenario import Scenario


scenario: Scenario = Scenario.from_list(
    data = [
        {
            "campaign": "Unification of Italy",
            "name": "Roma",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "farmers_guild": 1,
                "large_farm": 5,
                "vineyard": 1,
            },
        },
        {
            "campaign": "Unification of Italy",
            "name": "Roma",
            "buildings": {
                "city_hall": 1,
                "basilica": 1,
                "carpenters_guild": 1,
                "large_lumber_mill": 5,
                "warehouse": 1,
            },
        },
    ],
)

scenario.display_scenario_results()
```

The terminal output will display a comparison between the different scenarios

![scenario 1](img/scenario_1.png)

You can chose to pass a configuration to control which elements are displayed. The available elements include:

- `city` controls the printing of the campaign and city title
- `buildings` controls the printing of the list of buildings
- `effects` controls the printing of the effects table
- `production` controls the printing of the production table
- `storage` controls the printing of the storage table
- `defenses` controls the printing of the defenses table

```python
scenario: Scenario = Scenario.from_list(
    data = [
        ...
    ],
    configuration = {
        "defenses": {
            "include": False,
        },
        "storage": {
            "include": False,
        },
    },
)
```

![scenario 2](img/scenario_2.png)

By default, all elements have been set to `"include": True` and thus will be displayed.
