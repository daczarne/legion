from modules.city import City, CityBuildings, RssCollection


scenario_1: City = City(
    campaign = "Unification of Italy",
    name = "Roma",
    buildings = CityBuildings(
        buildings = {
            "large_fort": 1,
            "basilica": 1,
            "miners_guild": 1,
        },
    ),
)

scenario_1.display_results(
    include_city_information = True,
    include_city_effects = True,
)

print(f"City effects: {scenario_1.city_effects}")

# scenario_2: City = City(
#     campaign = "Unification of Italy",
#     name = "Roma",
#     buildings = CityBuildings(
#         buildings = {
#             "farm": 4,
#             "vineyard": 1,
#             "outcrop_mine": 1,
#             "basilica": 1,
#             "farmers_guild": 1,
#         },
#     ),
# )

# scenario_2.display_results()
