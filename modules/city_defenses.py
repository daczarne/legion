from dataclasses import dataclass


@dataclass
class CityDefenses:
    garrison: str
    squadrons: int = 1
    squadron_size: str = "Small"
