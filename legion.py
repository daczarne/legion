from modules.city import City


City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "hospital": 1,
        "training_ground": 1,
        "gladiator_school": 1,
        "stables": 1,
        "bordello": 1,
        "quartermaster": 1,
        "large_fort": 1,
    },
).display_results()

# City(
#     campaign = "Unification of Italy",
#     name = "Clusium",
#     buildings = {
#         "city_hall": 1,
#         "basilica": 1,
#         "warehouse": 1,
#         "large_lumber_mill": 6,
#     },
# ).display_results()
