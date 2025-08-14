# Legion

This project is a collection of classes that help you organize your kingdom in Legion.

## The `City` class

The `City` class is the backbone of it all. Given a city (identified by campaign and city name) and the configuration
of buildings that you'd like to build in it, it displays the information about the city (its effects, production,
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
example, you could want the Defenses section to be omitted and the Production section to be shown in yellow.

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

The `Scenario` class is used to compare two or more possible configurations for a given city, or different cities
altogether. You can create a comparison by passing a list of `City` objects to the `Scenario` class or via a convenient
`Scenario.from_list()` method. Each element of the list must be a dictionary just like with the `City` class.

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

![scenario 1](img/scenario_1.png)

Just as with the `CityDisplay` class, you can pass a `DisplayConfiguration` object to control how the cities are
displayed. The configuration supplied will be used for all cities in the `Scenario`.

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

## The `DisplayConfiguration` class

This helper class is used to help you create valid configurations. The different sections of the output that can be
configured are:

- `city` controls the printing of the campaign and city title
- `buildings` controls the printing of the list of buildings
- `effects` controls the printing of the effects table
- `production` controls the printing of the production table
- `storage` controls the printing of the storage table
- `defenses` controls the printing of the defenses table

For each section you can control:

- `include (bool)`: controls whether the section should be included in the output.
- `height (int)`: controls the space available for that section in the output. It is advisable to let the program handle
  this or you may end up causing the output to be truncated in different ways. The space used will be adjusted based on
  the sections that you decide to include.
- `color (str)`: controls the color in which the section is displayed.
