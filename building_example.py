from modules.building import Building


city_hall: Building = Building(id = "city_hall")
city_hall.display_building()

print()

mountain_mine: Building = Building(id = "mountain_mine", workers = 1)
mountain_mine.display_building()

print()

large_mine: Building = Building(id = "large_mine", workers = 0)
large_mine.display_building()

print(large_mine.required_building)

print()

stables: Building = Building(id = "stables", workers = 0)
# stables.display_building()

print(stables.required_building)

print()

carpenters_guild: Building = Building(id = "carpenters_guild", workers = 0)
# carpenters_guild.display_building()

print(carpenters_guild.required_building)


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
