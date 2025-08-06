from dataclasses import dataclass
from enum import Enum
from typing import TypedDict


class GeoFeature(Enum):
    LAKE = "lake"
    OUTCROP_ROCK = "outcrop_rock"
    MOUNTAIN = "mountain"
    FOREST = "forest"


class GeoFeaturesData(TypedDict):
    rock_outcrops: int
    mountains: int
    lakes: int
    forests: int


@dataclass
class GeoFeatures:
    rock_outcrops: int = 0
    mountains: int = 0
    lakes: int = 0
    forests: int = 0
