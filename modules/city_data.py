from typing import TypedDict, TypeAlias, Literal


class CityResourcePotentialsData(TypedDict):
    food: int
    ore: int
    wood: int

class CityGeoFeaturesData(TypedDict):
    rock_outcrops: int
    mountains: int
    lakes: int
    forests: int


class CityEffectsData(TypedDict):
    troop_training: int
    population_growth: int
    intelligence: int


class CityData(TypedDict):
    name: str
    campaign: str
    resource_potentials: CityResourcePotentialsData
    geo_features: CityGeoFeaturesData
    effects: CityEffectsData
    garrison: str


CitiesData: TypeAlias = dict[Literal["cities"], list[CityData]]
