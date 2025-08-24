from modules.building import Building

city_hall: Building = Building(id = "city_hall")
city_hall.show()

print()

mountain_mine: Building = Building(id = "mountain_mine", workers = 1)
mountain_mine.show()

print()

large_mine: Building = Building(id = "large_mine", workers = 0)
print(large_mine)
print(f"Workers: {large_mine.workers}")

print(f"Adding 2 workers to the mine...")
large_mine.add_workers(qty = 2)
print(f"Workers: {large_mine.workers}")

print(f"Removing 1 worker from the mine...")
large_mine.remove_workers(qty = 1)
print(f"Workers: {large_mine.workers}")

print(f"Setting the number of workers to 3...")
large_mine.set_workers(qty = 3)
print(f"Workers: {large_mine.workers}")
