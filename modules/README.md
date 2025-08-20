# The `City` class fields

```txt
City
  |_ campaign
  |_ name
  |_ buildings (BuildingsCount)
  |_ resource_potentials (ResourceCollection)
  |_ geo_features (GeoFeatures)
  |_ effects
  |    |_ city (EffectBonuses)
  |    |_ buildings (EffectBonuses)
  |    |_ workers (EffectBonuses)
  |    |_ total (EffectBonuses)
  |_ production
  |    |_ base (ResourceCollection)
  |    |_ productivity_bonuses (ResourceCollection)
  |    |_ total (ResourceCollection)
  |    |_ maintenance_costs (ResourceCollection)
  |    |_ balance (ResourceCollection)
  |_ storage
  |    |_ city (ResourceCollection)
  |    |_ buildings (ResourceCollection)
  |    |_ warehouse (ResourceCollection)
  |    |_ supply_dump (ResourceCollection)
  |    |_ total (ResourceCollection)
  |_ defenses (CityDefenses)
  |_ focus (Resource)
  |_ MAX_WORKERS
  |_ POSSIBLE_CITY_HALLS
  |_ MAX_BUILDINGS_PER_CITY
```
