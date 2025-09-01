<!-- markdownlint-disable MD013 -->
<!-- markdownlint-disable MD029 -->
# Prompts

## p1

At least at a first glance, your algorithm seems correct in validating that all requirements for a given building are present.
That's good.

But that is not enough for validating whether a given list of buildings can be built in a city. Maybe this is my fault and I should have clarified all possible requirements. I didn't because there are a lot of them. And that's why I was thinking that using a graph would be a sound design decision that will allow for expanding further.

The problem that I see with your algo is that though it validates that the requirements are met, it does not account for what buildings the city "already has". Meaning that after validating a given building, it doesn't validate the next one thinking "I already have these other buildings".

Let me give you an example of this problem. Take the following city

```python
roma: City = City(
  campaign = "Unification of Italy",
  name = "Roma",
  buildings = [
    Building(id = "city_hall"),
    Building(id = "farm"),
    Building(id = "stables"),
    Building(id = "stables"),
  ]
)
```

You algo will say that this city is valid because all requirements are met. But a city can only have one "stables". Once one is built, it cannot build another one. That's why we need an algo that keeps track of the state of the City as it validates one building and the next one. Your algo looks alright, but limited.

Here's where I think that having a `BuildingsGraph` model that keeps track of the state is better. We could define the nodes as

```python
class _BuildingNode:

    def __init__(
            self,
            building: Building,
            max_per_city: int = 1,
            current_count: int = 0,
            is_available: bool = True,
        ) -> None:
        self.building: Building = building
        self.max_per_city: int = max_per_city
        self.current_count: int = current_count
        self.is_available: bool = is_available

    def __repr__(self) -> str:
        return self.building.__repr__()
```

where the `max_per_city` is an int that establishes how many of a given building can be built, `current_count` keeps track
of how many the algo has seen, and `is_available` is a boolean that keeps track of whether another instance of that building can be added to the city.

With this, we could create the `BuildingsGraph` class.

```python
class BuildingsGraph:
    # Need to complete this class
    pass
```

This class will have the methods to create an instance that can be adjusted to the characterisitics of the city. This is important because of another validation that I have not yet mentioned. Take for example the "fishing_village" building that I have mentioned before. This building can only be built on cities that have a lake.

I have gathered all the cities information in another YAML file that lists, for each city, amongst other things, with geographical features the city has (like lakes and mountains, and forests).

Appart from the methods to creating the graph instance, the key method that this class would have is a traversal method. This will use either breath or depth first search (not sure which one I need) to traverse the graph.

So the `_CityValidator` will say that a city is valid is all its buildings can be traversed (i.e. found and reached) in the graph model. And because in the graph model each node keeps track of things like how many of that building are already in the city, the graph can resolve building counts too.

I don't have the full traversal algorithm solved. That (and creating the graph model) is where I need your help. But it will go something like this:

- the method will take a building as its parameter
- we start the traversal from the "village_hall" always
- we move through the graph until we find the node that has the building with the same ID as the building that was passed to the method
- once we find it we need to check whether the `is_available` flag for that building is `True`
  - if it is `False` we raise an exception. We don't need to validate all other buildings, we already know that these group of buildings includes at least one non-possible building, and therefore it is not valid. I think that this is specially good. Because we are raising the error from here, we are at standing at the problem that causes the exception. Which means that we can raise an error that clearly explains the issue to the user. We can report the building that we are validating, the `max_per_city` that this building has, and the `current_count`. This way the user knows exactly what to correct in his city.
  - if it is `True`, we increment the `current_counter` by 1
    - if the `current_counter` value now matches the `max_per_city`, we change `is_available` to `False`. This means that no more buildings of this type can be added to this city.
- now that we have finished evaluating the node itself, we need to move "upwards" until we reach the "village_hall" node again. We do this so that we can account for building evolution. If the building that we are validating has a `replaces` value, then we need to also increment the counter of that building (node). And, once again, if the current counter matches the max, then the availability flag gets switched to False.

I know that there are some rough edges still to polish here. But you see now why I think that having a graph model is better?

## p2

I'm glad we are on the same page now as what we are going to be doing. But before we move on to the traversal, let's align in a few other spots.

First, I have decided that the class names will be `_CityBuildingNode` and `_CityBuildingsGraph`. These are better names. Since each graph is city-dependent, these classes are more at home in the `city.py` module. Therefore, they should be named "city..." and they are not private to the module, so they should start with underscore.

Here's the node class

```python
class _CityBuildingNode:

    def __init__(
            self,
            building: Building,
            max_per_city: int = 1,
            current_count: int = 0,
            is_available: bool = True,
        ) -> None:
        self.building: Building = building
        self.max_per_city: int = max_per_city
        self.current_count: int = current_count
        self.is_available: bool = is_available

    def __repr__(self) -> str:
        return f"_CityBuildingNode(id = \"{self.building.id}\", count = {self.current_count}/{self.max_per_city}, is_available = {self.is_available})"
```

Now let's talk about the graph class it self. I agree with the `self.nodes` members. No argument there. That's pretty
standard graph stuff.

But what I am not sure I follow with your idea of `self.edges`. Remember we need to implement the idea of multiple requirements being statisfied. What does this member add?

## p3

Not yet. First let's talk about the inicialization of the graph. Usually, when creating a graph model one needs to add methods for `add_node()`, `delete_node()`, `add_edge()`, and `delete_edge()`. We clarily don't need the methods for adding and removing edges since we don't have that concept here. But what about the methods for creating nodes? We probably won't need one for removing nodes either given the nature of what we are doing.

## p4

Aha! That's good! So we don't need methods for adding and removing neither nodes nor edges.

But, the graph instances will be instantiated by the `_CityValidator` class. This class will have to already inject some state (context) into the graph. For example, if the city has no lake, then it will need to inform the graph that the `max_per_city` for the "fishing_village" node is actually zero in this case. The node needs to receive this information and, since now the current count and the max match, flip the is available flag to False already. How would you handled that? It seems to me like we need to add some methods to the node class so that the node class knows how to handle its own state. Or should the state of the node always be updated by the graph class?

## p5

That's alright, but how about:

```python
def increment_count(self) -> None:
    """
    Increment the `current_count` by one.
    """
    if not self.is_available:
        raise ValueError(
            f"Cannot build \"{self.building.id}\": "
            f"limit of {self.allowed_count} reached (current = {self.current_count})."
        )

    if self.current_count + 1 > self.allowed_count:
        raise RuntimeError(
            f"Internal error: \"{self.building.id}\" exceeded allowed_count. "
            f"current = {self.current_count}, allowed = {self.allowed_count}"
        )

    self.current_count += 1

    if self.current_count == self.allowed_count:
        self.is_available = False
```

This means that we validate the action before doing it.

You have to keep in mind that this is actually not an unimportant thing. We actually do need to consider this problem so that the validation is not dependent on the order of the buildings. Let me give you an example.

Suppose you have the following city

```python
city: City = City.from_buildings_count(
    campaign = "Conquest of Britain",
    name = "Anderitum",
    buildings = {
        "city_hall": 1,
        "village_hall": 1,
    },
)
```

This city is invalid. But, will the algo catch it? Well, if our algo is not order-agnostic, we will need to be careful about the order in which the buildings are passed (i.e. the order in which the buildings are traversed).

Let's suppose that the first step of the loop is with "city_hall". The algo starts from "village_hall". It searches DFS until it finds "city_hall". Changes the state. And then it searches backwards changing the states of those nodes too.

Next up, the loop moves on to the "village_hall". The algo finds the node. It sees that the node is in the is_available = False state. An error is raised. The algo worked fine.

Now suppose the algo starts with the "village_hall" instead. At the end of the first iteration, the graph will have hte "village_hall" node in the is available False state, but the "city_hall" node will be in the is available True state.

Next, the loop moves on to "city_hall". It starts from the "village_hall", which has already been set to is_available = False, but that is not a problem. The traversal can travel through unavailable nodes, it just cannot end in them. It reaches the "city_hall" node and adds the building. Then it moves upwards to the "town_hall" and it does the backwards steps there too. Now it needs to move up to the "village_hall". It will set the current_count = 2. This is a problem! If we have no validation for this value, it will not change the flag because the changing of the flag is only asking whether current_count == allowed_count, and since 2 != 1, the changing of the flag will be skipped, and since we are already at the "village_hall" node, the iteration terminates "successfully" and the error is not caught.

By ensuring that current_count cannot be greater than allowed_count in the nodes, we prevent this error.

## p6

I like it when, without me even saying it, you already start going in the right direction.

The city is already aware of its geography. Let me show you how.

There's an entire module called `geo_features.py` in the program. Amongst a few other small things, the main class in
that module is:

```python
@dataclass
class GeoFeatures:
    """
    Stores counts of geographic features and provides dictionary-like access.

    Each instance tracks the four geographic feature types: rock outcrops, mountains, lakes, and forests. Supports
    iteration and retrieval like a dictionary.

    Public methods:
        __iter__(): Iterate over feature names.
        items(): Return (feature_name, value) pairs.
        values(): Return counts of all features.
        get(key): Get the count for a given feature name. Raises KeyError if the key is not found.
    """
    rock_outcrops: int = 0
    mountains: int = 0
    lakes: int = 0
    forests: int = 0

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over keys, like a dict.
        """
        return (field.name for field in fields(class_or_instance = self))

    def items(self) -> Iterator[tuple[str, int]]:
        """
        Return an iterator of (key, value) pairs, like dict.items().
        """
        return ((field.name, getattr(self, field.name)) for field in fields(class_or_instance = self))

    def values(self) -> Iterator[int]:
        """
        Return an iterator of values, like dict.values().
        """
        return (getattr(self, field.name) for field in fields(class_or_instance = self))

    def get(self, key: str) -> int:
        """
        Get the value for a given geo feature name.
        """
        if key not in (f.name for f in fields(class_or_instance = self)):
            raise KeyError(f"Invalid geo feature name: {key}")

        return getattr(self, key)
```

When an instance of the city class gets created it reads for a YAML file the info about that city. In this info, it learns about the city's geo features. Here's an excerpt of the city class. It's not the whole thing of course, just the part that concerns us right now.

```python
@dataclass(
    match_args = False,
    order = False,
    kw_only = True,
)
class City:
    campaign: str = field(init = True, default = "", repr = True, compare = True, hash = True)
    name: str = field(init = True, default = "", repr = True, compare = True, hash = True)
    buildings: list[Building] = field(init = True, default_factory = list, repr = False, compare = False, hash = False)
    has_supply_dump: bool = field(init = False, default = False, repr = False, compare = False, hash = False)
    is_fort: bool = field(init = False, default = False, repr = False, compare = False, hash = False)

    # Post init fields
    resource_potentials: ResourceCollection = field(
        init = False,
        default_factory = ResourceCollection,
        repr = False,
        compare = False,
        hash = False,
    )
    geo_features: GeoFeatures = field(
        init = False,
        default_factory = GeoFeatures,
        repr = False,
        compare = False,
        hash = False,
    )

    __match_args__: ClassVar[tuple[str, ...]] = ("campaign", "name")

    def _get_rss_potentials(self) -> ResourceCollection:
        """
        Finds the city supplied by the user in the directory of cities and returns its resource potentials.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return ResourceCollection(**city["resource_potentials"])

        return ResourceCollection()

    def _get_geo_features(self) -> GeoFeatures:
        """
        Finds the city supplied by the user in the directory of cities and returns its geo-features.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return GeoFeatures(**city["geo_features"])

        return GeoFeatures()

    def _has_supply_dump(self) -> bool:
        """
        Checks if the city has a Supply dump.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return city["has_supply_dump"]

        return False

    def _is_fort(self) -> bool:
        """
        Checks if the city is a "Small Fort" city.
        """
        for city in CITIES:
            if (
                city["campaign"] == self.campaign
                and city["name"] == self.name
            ):
                return city["is_fort"]

        return False

    # Lots of other methods and things here until we get to the __post_init__ method
    def __post_init__(self) -> None:
        self.resource_potentials = self._get_rss_potentials()
        self.geo_features = self._get_geo_features()

        self.has_supply_dump = self._has_supply_dump()
        self._add_supply_dump_to_buildings()

        self.is_fort = self._is_fort()
        self._add_fort_to_buildings()

        #* Validate city
        validator: _CityValidator = _CityValidator(city = self)
        validator._validate_halls()
        validator._validate_number_of_buildings()

        # Lots of other things here too that are not relevant now.

    def get_building(self, id: str) -> Building:
        """
        Retrieve a building from the city by its ID. In case the city has more than one it will return the first one.

        Args:
            id (str): the building ID to search for.

        Returns:
            Building: the first building in the city with the given ID.

        Raises:
            KeyError: if no building with the given ID exists in the city.
        """
        for building in self.buildings:
            if building.id == id:
                return building

        raise KeyError(f"No building with ID={id} found in {self.name}.")

    def has_building(self, id: str) -> bool:
        """
        Check whether the city contains a building with the specified ID.

        Args:
            id (str): the building ID to search for.

        Returns:
            bool: True if the building is present, False otherwise.
        """
        for building in self.buildings:
            if building.id == id:
                return True

        return False

    def get_hall(self) -> Building: # type: ignore
        """
        Retrieve the hall building of the city.

        The hall is the central building of the city and must be one of "Village hall", "Town hall", or "City hall".

        Returns:
            Building: the hall building of the city.
        """
        for building in self.buildings:
            if building.id not in _CityValidator.POSSIBLE_CITY_HALLS:
                continue

            return building

    def get_buildings_count(self, by: Literal["name", "id"]) -> BuildingsCount:
        """
        Count the number of buildings in the city grouped by ID or name.

        Args:
            by (Literal["name", "id"]): whether to group counts by building name or ID.

        Returns:
            BuildingsCount: a dictionary mapping either building IDs or names to their respective counts.
        """
        from collections import Counter

        if by == "name":
            buildings_count: BuildingsCount = Counter([building.name for building in self.buildings])
            return buildings_count

        if by == "id":
            buildings_count: BuildingsCount = Counter([building.id for building in self.buildings])
            return buildings_count

    def build_city_displayer(self, configuration: DisplayConfiguration | None = None) -> "_CityDisplay":
        """
        Creates a displayer for the City.

        Args:
            configuration: An optional dictionary for customizing the display. This can be used to hide specific
                sections or change their appearance.

        Returns:
            _CityDisplay: An instance of the _CityDisplay class.
        """
        return _CityDisplay(city = self, configuration = configuration)

    def display_city(self, configuration: DisplayConfiguration | None = None) -> None:
        """
        Renders and prints the city's statistics to the console.

        This method acts as a facade, delegating the display logic to the `_CityDisplay` class.

        Args:
            configuration: An optional dictionary for customizing the display. This can be used to hide specific
                sections or change their appearance.
        """
        displayer: _CityDisplay = self.build_city_displayer(configuration = configuration)
        displayer.display_city()
```

And here's an example of what the `./data/cities.yaml` file has for each city:

```yaml
  - name: Caercini
    campaign: Unification of Italy
    resource_potentials:
      food: 50
      ore: 125
      wood: 0
    geo_features:
      rock_outcrops: 1
      mountains: 1
      lakes: 0
      forests: 0
    effects:
      troop_training: 25
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Hill Tribe Warriors
  - name: Hernici
    campaign: Unification of Italy
    resource_potentials:
      food: 80
      ore: 100
      wood: 80
    geo_features:
      rock_outcrops: 1
      mountains: 0
      lakes: 1
      forests: 0
    effects:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Auxilia
  - name: Roma
    campaign: Unification of Italy
    resource_potentials:
      food: 125
      ore: 0
      wood: 50
    geo_features:
      rock_outcrops: 0
      mountains: 0
      lakes: 0
      forests: 0
    effects:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Legion
```

There are hundreds more cities across several campaigns. But I think this gives you an idea of how they all look.

Then there's the Building class. Apart from the properties that we have already discussed, the buildings have two that are going to become relevant here: `required_geo` and `required_rss`. Here are some examples that we have been talking about

```yaml
  - id: village_hall
    name: Village hall
    building_cost:
      food: 0
      ore: 0
      wood: 0
    maintenance_cost:
      food: -5
      ore: -5
      wood: -5
    productivity_bonuses:
      food: 0
      ore: 0
      wood: 0
    productivity_per_worker:
      food: 0
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 50
      ore: 50
      wood: 50
    max_workers: 0
    is_buildable: false
    is_deletable: false
    is_upgradeable: true
    required_geo: null
    required_rss: null
    required_building: []
    replaces: null
  - id: town_hall
    name: Town hall
    building_cost:
      food: 250
      ore: 0
      wood: 250
    maintenance_cost:
      food: -3
      ore: -3
      wood: -3
    productivity_bonuses:
      food: 0
      ore: 0
      wood: 0
    productivity_per_worker:
      food: 0
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 75
      ore: 75
      wood: 75
    max_workers: 0
    is_buildable: true
    is_deletable: false
    is_upgradeable: true
    required_geo: null
    required_rss: null
    required_building:
      - village_hall
    replaces: village_hall
  - id: city_hall
    name: City hall
    building_cost:
      food: 350
      ore: 100
      wood: 350
    maintenance_cost:
      food: 1
      ore: 1
      wood: 1
    productivity_bonuses:
      food: 25
      ore: 25
      wood: 25
    productivity_per_worker:
      food: 0
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 100
      ore: 100
      wood: 100
    max_workers: 0
    is_buildable: true
    is_deletable: false
    is_upgradeable: false
    required_geo: null
    required_rss: null
    required_building:
      - town_hall
    replaces: town_hall
  - id: farm
    name: Farm
    building_cost:
      food: 0
      ore: 100
      wood: 0
    maintenance_cost:
      food: 0
      ore: 0
      wood: 0
    productivity_bonuses:
      food: 0
      ore: 0
      wood: 0
    productivity_per_worker:
      food: 7
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 50
      ore: 0
      wood: 0
    max_workers: 3
    is_buildable: true
    is_deletable: true
    is_upgradeable: true
    required_geo: null
    required_rss: food
    required_building:
      - village_hall
    replaces: null
  - id: large_farm
    name: Large farm
    building_cost:
      food: 0
      ore: 150
      wood: 150
    maintenance_cost:
      food: 0
      ore: 0
      wood: 0
    productivity_bonuses:
      food: 0
      ore: 0
      wood: 0
    productivity_per_worker:
      food: 12
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 75
      ore: 0
      wood: 0
    max_workers: 3
    is_buildable: true
    is_deletable: true
    is_upgradeable: false
    required_geo: null
    required_rss: food
    required_building:
      - farm
    replaces: farm
  - id: vineyard
    name: Vineyard
    building_cost:
      food: 0
      ore: 150
      wood: 150
    maintenance_cost:
      food: 0
      ore: 0
      wood: 0
    productivity_bonuses:
      food: 10
      ore: 10
      wood: 10
    productivity_per_worker:
      food: 10
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 75
      ore: 0
      wood: 0
    max_workers: 3
    is_buildable: true
    is_deletable: true
    is_upgradeable: false
    required_geo: null
    required_rss: food
    required_building:
      - town_hall, farm
    replaces: farm
  - id: fishing_village
    name: Fishing village
    building_cost:
      food: 0
      ore: 50
      wood: 0
    maintenance_cost:
      food: 0
      ore: 0
      wood: 0
    productivity_bonuses:
      food: 0
      ore: 0
      wood: 0
    productivity_per_worker:
      food: 9
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 50
      ore: 0
      wood: 0
    max_workers: 3
    is_buildable: true
    is_deletable: false
    is_upgradeable: false
    required_geo: lake
    required_rss: food
    required_building:
      - village_hall
    replaces: null
  - id: farmers_guild
    name: Farmers' guild
    building_cost:
      food: 250
      ore: 250
      wood: 250
    maintenance_cost:
      food: 10
      ore: 0
      wood: 0
    productivity_bonuses:
      food: 50
      ore: 0
      wood: 0
    productivity_per_worker:
      food: 0
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 0
      ore: 0
      wood: 0
    max_workers: 0
    is_buildable: true
    is_deletable: true
    is_upgradeable: false
    required_geo: null
    required_rss: food
    required_building:
      - city_hall, large_farm
    replaces: null
  - id: stables
    name: Stables
    building_cost:
      food: 200
      ore: 0
      wood: 0
    maintenance_cost:
      food: 5
      ore: 0
      wood: 0
    productivity_bonuses:
      food: 0
      ore: 0
      wood: 0
    productivity_per_worker:
      food: 0
      ore: 0
      wood: 0
    effect_bonuses:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    effect_bonuses_per_worker:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    storage_capacity:
      food: 0
      ore: 0
      wood: 0
    max_workers: 0
    is_buildable: true
    is_deletable: true
    is_upgradeable: false
    required_geo: null
    required_rss: null
    required_building:
      - farm
      - large_farm
      - vineyard
      - fishing_village
    replaces: null
```

Before we continue, do let me know if you have any questions about how this all works?

## p7

Answering to your questions.

1. Can a building’s required_geo ever be plural (e.g. needs 2 lakes, or one mountain + one forest), or is it always a single feature?

Great question. The answer is no. Buildings will ever only need one geo feature. If there are multiple geo features, that means multiple buildings can be built. Here's an example.

```yaml
  - name: Reate
    campaign: Unification of Italy
    resource_potentials:
      food: 50
      ore: 150
      wood: 0
    geo_features:
      rock_outcrops: 0
      mountains: 2
      lakes: 0
      forests: 0
    effects:
      troop_training: 25
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Hill Tribe Warriors
```

This city has two mountains. That means that two instances of `Building(id = "mountain_mine")` can be built. This means that the `allowed_count` for the mountain mine node of the graph for this city, needs to be 2.

Here's another city, this one with one outcrop and one mountain

```yaml
  - name: Grumentum
    campaign: Unification of Italy
    resource_potentials:
      food: 50
      ore: 115
      wood: 50
    geo_features:
      rock_outcrops: 1
      mountains: 1
      lakes: 0
      forests: 0
    effects:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Peltasts
```

This city will be able to build 1 mountain mine, and one outcrop mine. It will not be able to build any fishing_villages.

2. Same for required_rss: always a single resource type, or can it be multiple?

Same here too: only one per building. For example, a farm requires that a city has rss production potential for food > 0. All types of mines (mine, large_mine, outcrop_mine, or mountain_mine) required that the city have rss production potential for ore > 0.

3. For prerequisites (required_building): sometimes you list one (["farm"]), sometimes many (["farm", "large_farm", "vineyard"]). Do we treat that as an OR (any one suffices) or AND (all required)?

This has not changed from what we discussed. This is how to express the DNF in YAML. YAML doesn't have things like tuples. So line here is an OR condition. In each line, there can be more than one requirement, those are AND conditions.

Here's an excerpt of the `Building` class. I think seeing the init and post init here shed better light on how this gets treated than what words can ever do.

```python
@dataclass(match_args = False, kw_only = True)
class Building:
    id: str = field(init = True, repr = True, compare = True, hash = True)
    workers: int = field(default = 0, repr = False, compare = False, hash = False)

    name: str = field(init = False, repr = False, compare = False, hash = False)
    building_cost: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    maintenance_cost: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    productivity_bonuses: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    productivity_per_worker: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    effect_bonuses: EffectBonuses = field(init = False, repr = False, compare = False, hash = False)
    effect_bonuses_per_worker: EffectBonuses = field(init = False, repr = False, compare = False, hash = False)
    storage_capacity: ResourceCollection = field(init = False, repr = False, compare = False, hash = False)
    max_workers: int = field(init = False, repr = False, compare = False, hash = False)
    is_buildable: bool = field(init = False, repr = False, compare = False, hash = False)
    is_deletable: bool = field(init = False, repr = False, compare = False, hash = False)
    is_upgradeable: bool = field(init = False, repr = False, compare = False, hash = False)
    required_geo: GeoFeature | None = field(init = False, default = None, repr = False, compare = False, hash = False)
    required_rss: Resource | None = field(init = False, default = None, repr = False, compare = False, hash = False)
    # Dependencies here need to be interpreted as an OR. Either of the listed buildings unblocks the building. For
    # example, a Stable requires either a Farm, or a Large Farm, or a Vineyard, or a Fishing Village. If the city has
    # any one for them it can build a Stable. Similarly, a Blacksmith requires either a Mine, or a Large Mine, or a
    # Mountain Mine, or an Outcrop Mine. If a building has no dependencies the list will be empty.
    required_building: list[tuple[str, ...]] = field(init = False, default_factory = list, repr = False, compare = False, hash = False)
    replaces: str | None = field(init = False, default = None, repr = False, compare = False, hash = False)


    __match_args__: ClassVar[str] = ("id")


    def _validate_building_exists(self) -> None:
        if self.id not in _BUILDINGS:
            raise UnknownBuildingError(f"Building {self.id} does not exist.")

    def _validate_initial_number_of_workers(self) -> None:
        if self.workers > self.max_workers:
            raise TooManyWorkersError(f"Too many workers. Max is {self.max_workers} for {self.name}.")

    def _unpack_required_buildings(self) -> list[tuple[str, ...]]:
        required_buildings_list_of_strings: list[str] = _BUILDINGS[self.id]["required_building"]
        required_buildings: list[tuple[str, ...]] = []

        for requirement in required_buildings_list_of_strings:
            required_buildings.append(tuple(requirement.split(sep = ", ")))

        return required_buildings


    def __post_init__(self) -> None:
        self._validate_building_exists()

        self.name = _BUILDINGS[self.id]["name"]
        self.building_cost = ResourceCollection(**_BUILDINGS[self.id]["building_cost"])
        self.maintenance_cost = ResourceCollection(**_BUILDINGS[self.id]["maintenance_cost"])
        self.productivity_bonuses = ResourceCollection(**_BUILDINGS[self.id]["productivity_bonuses"])
        self.productivity_per_worker = ResourceCollection(**_BUILDINGS[self.id]["productivity_per_worker"])
        self.effect_bonuses = EffectBonuses(**_BUILDINGS[self.id]["effect_bonuses"])
        self.effect_bonuses_per_worker = EffectBonuses(**_BUILDINGS[self.id]["effect_bonuses_per_worker"])
        self.storage_capacity = ResourceCollection(**_BUILDINGS[self.id]["storage_capacity"])
        self.max_workers = _BUILDINGS[self.id]["max_workers"]
        self.is_buildable = _BUILDINGS[self.id]["is_buildable"]
        self.is_deletable = _BUILDINGS[self.id]["is_deletable"]
        self.is_upgradeable = _BUILDINGS[self.id]["is_upgradeable"]
        self.required_geo = GeoFeature(value = _BUILDINGS[self.id]["required_geo"]) if _BUILDINGS[self.id]["required_geo"] else None
        self.required_rss = Resource(value = _BUILDINGS[self.id]["required_rss"]) if _BUILDINGS[self.id]["required_rss"] else None
        self.required_building = self._unpack_required_buildings()
        self.replaces = _BUILDINGS[self.id]["replaces"]

        self._validate_initial_number_of_workers()


    def add_workers(self, qty: int) -> None:
        """
        Assigns additional workers to the building.

        Args:
            qty (int): Number of workers to add.

        Raises:
            TooManyWorkersError: If the new total (current + the qty to be added) exceeds the maximum worker capacity.
            NegativeNumberOfWorkersError: If the supplied quantity (`qty`) is negative.
        """
        if qty < 0:
            raise NegativeNumberOfWorkersError("Cannot add a negative number of workers.")

        if self.workers + qty > self.max_workers:
            raise TooManyWorkersError(f"Too many workers. Max is {self.max_workers} for {self.name}.")

        self.workers += qty

    def remove_workers(self, qty: int) -> None:
        """
        Removes workers from the building.

        Args:
            qty (int): Number of workers to remove.

        Raises:
            InsufficientNumberOfWorkersError: If the operation results in fewer than zero workers.
            NegativeNumberOfWorkersError: If the supplied quantity (`qty`) is negative.
        """
        if qty < 0:
            raise NegativeNumberOfWorkersError("Cannot remove a negative number of workers.")

        if self.workers - qty < 0:
            raise InsufficientNumberOfWorkersError(f"Can not remove {qty} workers. Building currently has {self.workers}.")

        self.workers -= qty

    def set_workers(self, qty: int) -> None:
        """
        Sets the exact number of workers for the building.

        Args:
            qty (int): Number of workers to assign.

        Raises:
            TooManyWorkersError: If the value exceeds the maximum number of workers the building can have.
            NegativeNumberOfWorkersError: If the supplied quantity (`qty`) is negative.
        """
        if qty < 0:
            raise NegativeNumberOfWorkersError("Cannot set a negative number of workers.")

        if qty > self.max_workers:
            raise TooManyWorkersError(f"{self.name} cannot allocate {qty} workers. Max is {self.max_workers}.")

        self.workers = qty
```

## p8

I think I have found the reason why I don't follow with your proposal. You are assuming that `_BUILDINGS` from the `building.py` module is already a collection of all possible buildings. And, in a way, it is. But this is just the data being read from the yaml file, it is not a collection of `Building` objects.

Here's the code that creates it

```python
class _BuildingData(TypedDict):
    """
    This is a helper class meant to be used when reading building data from YAML or JSON files. Its only purpose is to
    provide good type annotations and hints.
    """
    id: str
    name: str
    building_cost: ResourceCollectionData
    maintenance_cost: ResourceCollectionData
    productivity_bonuses: ResourceCollectionData
    productivity_per_worker: ResourceCollectionData
    effect_bonuses: EffectBonusesData
    effect_bonuses_per_worker: EffectBonusesData
    storage_capacity: ResourceCollectionData
    max_workers: int
    is_buildable: bool
    is_deletable: bool
    is_upgradeable: bool
    required_geo: str | None
    required_rss: str | None
    required_building: list[str]
    replaces: str | None

with open(file = "./data/buildings.yaml", mode = "r") as file:
    _buildings_data: dict[Literal["buildings"], list[_BuildingData]] = yaml.safe_load(stream = file)

_BUILDINGS: dict[str, _BuildingData] = {building["id"]: building for building in _buildings_data["buildings"]}
```

This dictionary of "raw data" is used by the `Building` class to init the `Building` objects.

## p9

This is quite bad. But it's not your fault. I think you need more information about how the cities work.

In this game, a city can be thought as a collection of buildings. At the center of this collection is the Hall. The hall can be evolved from village to town to city, but there can always be only one, and there must always be one.

The hall determines many things for a city. One of those things is how many other buildings the city can support. The `MAX_BUILDINGS_PER_CITY` variable describes this limit. A city that only has a "village_hall" can only build 4, with a "town_hall" that grows to 6 and with a "city_hall" that grows to its maximum of 8.

What happens with other buildings?

Well, those can be classified into two groups: production buildings, and non-production buildings.

Non-production buildings (like a bath -> hospital, a shrine -> temple -> basilica, training grounds, etc) are limited to 1 per city. This means that most buildings are limited to 1 by default, and that's why I set the default `allowed_count` to 1 in the `_CityBuildingNode` class.

The problem happens with the production buildings. One rule that governs all production buildings is that a city can only have production buildings that produce a resource for which the city itself has a production potential > 0. Therefore, everytime we see a city with rss pot of 0 for a given rss, we need to set the `allowed_count` to 0, for all buildings that have that rss as `required_rss`.

Next, production buildings can be further sub-classified into two groups. Let's call these groups "basic" and "geo-dependent".

The "basic" ones are the "farm -> large_farm", "mine -> large_mine", and "lumber_mill -> large_lumber_mill". The number of `allowed_count` for this count depends on two things:

- the size of the hall. For example, a city with only a "village_hall" will only be able to build a max of 4 total buildings, so this limits the basic production buildings. On the other end, a city with a "city_hall" will be able to have 8 total buildings.
- the presence of geo features. Geo features like lakes or mountains are always present in the city. This building spots can only be "evolved" into the specific building to expolit it. For example, if the city has a lake, the only thing that can be built there is a fishing_village

So let's go over some examples. Let's start with a city with no geo features:

```yaml
  - name: Roma
    campaign: Unification of Italy
    resource_potentials:
      food: 125
      ore: 0
      wood: 50
    geo_features:
      rock_outcrops: 0
      mountains: 0
      lakes: 0
      forests: 0
    effects:
      troop_training: 0
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Legion
```

and let's assume that the city only has

```python
City(
  campaign = "Unification of Italy",
  name = "Roma",
  buildings = [
    Building(id = "village_hall"),
    ...
  ]
)
```

Since this city no geo features already occupying any building spot, the max number of, for example, farms that it can build needs to be set to 4.

If instead, the player says that:

```python
City(
  campaign = "Unification of Italy",
  name = "Roma",
  buildings = [
    Building(id = "town_hall"),
    ...
  ]
)
```

then the `allowed_count` for the "farm" node grows to 6.

Now let's look at a city with one geo feature and enough rss production potential to exploit that geo feature.

```yaml
  - name: Friniates
    campaign: Unification of Italy
    resource_potentials:
      food: 0
      ore: 100
      wood: 100
    geo_features:
      rock_outcrops: 1
      mountains: 0
      lakes: 0
      forests: 0
    effects:
      troop_training: 25
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Hill Tribe Warriors
```

If when this city first starts it only has a "village_hall":

```python
City(
  campaign = "Unification of Italy",
  name = "Friniates",
  buildings = [
    Building(id = "village_hall"),
    ...
  ]
)
```

Since this city has one "rock_outcrop", there's already one spot that can only be evolved into an "outcrop_mine". Therefore, the maximum number of "mine -> large_mine" or "lumber_mill -> large_lumber_mill" that it can build is 3. Why? Well it has a "village_hall" so max_number_of_buildings = 4, but one is already occupied by an "rock_outcrop", leaving us with three building spots available for other buildings.

Now let's look at this city with two geo features:

```yaml
  - name: Caercini
    campaign: Unification of Italy
    resource_potentials:
      food: 50
      ore: 125
      wood: 0
    geo_features:
      rock_outcrops: 1
      mountains: 1
      lakes: 0
      forests: 0
    effects:
      troop_training: 25
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Hill Tribe Warriors
```

```python
City(
  campaign = "Unification of Italy",
  name = "Caercini",
  buildings = [
    Building(id = "village_hall"),
    ...
  ]
)
```

Here the player will only be able to build 2 mines. Why? Same as before. It has a "village_hall", so the total number of supported buildings is 4. But two are already occupied with an "outcrop_rock" (which can only be evolved into an "outcrop_mine") and a "mountain" (which can only be evolved into a "mountain_mine"), leaving us with two more available spots.

One last example that has an ugly complication. Take this city:

```yaml
  - name: Sentinum
    campaign: Unification of Italy
    resource_potentials:
      food: 110
      ore: 0
      wood: 50
    geo_features:
      rock_outcrops: 1
      mountains: 0
      lakes: 0
      forests: 0
    effects:
      troop_training: 25
      population_growth: 0
      intelligence: 0
    has_supply_dump: false
    is_fort: false
    garrison: Italiot Greek Cavalry
```

The city has an "outcrop_rock". But the rss prod potential for ore is zero. This, sadly, means that this city will "loose" a building spot. There's nothing that can be done about it. There's nothing that can be done about it. The ourcrop rock is already there at the start. It cannot be deleted. But there's no rss prod pot for building mines.

I hope this helps give a better understanding of how the `allowed_count` property needs to work. But feel free to ask more questions if you need further clarifications.

I think at this point it would be best to start with some TDD. Let's create some tests scenarios that create graph objects for all these different scenarios, and then we can validate the implementation aginst the tests.
