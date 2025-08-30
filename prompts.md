# Prompts

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
class _BuldingNode:

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
