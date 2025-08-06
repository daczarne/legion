from modules.city import City


City(
    campaign = "Unification of Italy",
    name = "Clusium",
    buildings = {
        "city_hall": 1,
        "basilica": 1,
        "carpenters_guild": 1,
        "large_lumber_mill": 6,
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
