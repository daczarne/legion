from modules.building import Building


# city_hall: Building = Building(id = "city_hall")
# city_hall.display_building()

# print()

# mountain_mine: Building = Building(id = "mountain_mine", workers = 1)
# mountain_mine.display_building()

village_hall: Building = Building(id = "village_hall")
village_hall.display_building()

print()

large_mine: Building = Building(id = "large_mine")
large_mine.display_building()

print()

stables: Building = Building(id = "stables")
stables.display_building()

print()

carpenters_guild: Building = Building(id = "carpenters_guild", workers = 0)
carpenters_guild.display_building()

"""
[
    ("elem_1", "elem_2"),
    ("elem_3", "elem_4"),
    ("elem_5", "elem_6"),
]

    elem_1 AND elem_2
    OR: elem_3 AND elem_4
    OR: elem_5 AND elem_6
"""



# print()
# print(f"Adding 2 workers to the mine...")
# print("large_mine.add_workers(qty = 2)")
# large_mine.add_workers(qty = 2)
# large_mine.display_building()

# print()
# print(f"Removing 1 worker from the mine...")
# print("large_mine.remove_workers(qty = 1)")
# large_mine.remove_workers(qty = 1)
# large_mine.display_building()

# print()
# print(f"Setting the number of workers to 3...")
# print("large_mine.set_workers(qty = 3)")
# large_mine.set_workers(qty = 3)
# large_mine.display_building()
