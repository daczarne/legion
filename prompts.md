<!-- markdownlint-disable MD013 -->
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
