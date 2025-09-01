<!-- markdownlint-disable MD013 -->
<!-- markdownlint-disable MD029 -->
# Prompts

I am affraid the whole algo might have issues in its conception. This is why I insisted so much on the topic of graph
initialization. On a simple graph, when we initialize it we create the adj_list. When we do things like DFS, we only visit the nodes to which another node is connected to.

The problem with our algo is that when traversing forward (i.e. deep) the traversal should not be alowed to progress when a node with current_count == 0 is met. That means that that building is missing.

But this introduces a problem. Take for example the following city

```python
city: City = City(
    campaign = "Hispania",
    name = "Biskargis",
    buildings = [
        Building(id = "town_hall"),
        Building(id = "training_ground"),
    ]
)
```

If the order of traversals is "town_hall" -> "training_ground", there's no problem. But if it is "training_ground" -> "town_hall", then we have a problem. The first traversal, when the algo is seeking for the "training_ground" node, will fail.
