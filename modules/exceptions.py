"""
A collection of simple exceptions for the program. These exceptions are used just so that the errors being raised are
clearer and more specific to the isssue.
"""


class LegionError(Exception):
    """Base class for all errors in the project."""
    
    pass


# * ******** * #
# * BUILDING * #
# * ******** * #

class BuildingError(LegionError):
    """Base class for all errors in the `building` module."""
    
    pass


class UnknownBuildingError(BuildingError):
    """Unknown building error."""
    
    pass


class TooManyWorkersError(BuildingError):
    """Too many workers error."""
    
    pass


class InsufficientNumberOfWorkersError(BuildingError):
    """Insufficient number of workers error."""
    
    pass


class NegativeNumberOfWorkersError(BuildingError):
    """Negative number of workers error."""
    
    pass



# * **** * #
# * CITY * #
# * **** * #

class CityError(LegionError):
    """Base class for all errors in the `city` module."""
    
    pass


class CityNotFoundError(CityError):
    """City not found error."""
    
    pass


class NoCityHallError(CityError):
    """No city hall error."""
    
    pass


class MoreThanOneHallTypeError(CityError):
    """More than one hall type error."""
    
    pass


class TooManyHallsError(CityError):
    """Too many halls error."""
    
    pass


class FortsCannotHaveBuildingsError(CityError):
    """Forts cannot have buildings error."""
    
    pass


class TooManyBuildingsError(CityError):
    """Too many buildings error."""
    
    pass


class MoreThanOneGuildTypeError(CityError):
    """More than one guild type error."""
    
    pass


class TooManyGuildsError(CityError):
    """Too many guilds error."""
    
    pass


class InvalidBuidlingConfigurationError(CityError):
    """Invalid building configuration error."""
    
    pass


class UnknownBuildingStaffingStrategyError(CityError):
    """Unknown building staffing strategy error."""
    
    pass


# * ******* * #
# * DISPLAY * #
# * ******* * #

class DisplayError(LegionError):
    """Base class for all errors in the `display` module."""
    
    pass


# * ******* * #
# * EFFECTS * #
# * ******* * #

class EffectsError(LegionError):
    """Base class for all errors in the `effects` module."""
    
    pass


# * ************ * #
# * GEO FEATURES * #
# * ************ * #

class GeoFeaturesError(LegionError):
    """Base class for all errors in the `geo_features` module."""
    
    pass


# * ******* * #
# * KINGDOM * #
# * ******* * #

class KingdomError(LegionError):
    """Base class for all errors in the `kingdom` module."""
    
    pass


class DuplicatedCityError(KingdomError):
    """Duplicated city error."""
    
    pass


class CitiesFromMultipleCampaignsError(KingdomError):
    """Cities from multiple campaigns error."""
    
    pass


# * ********* * #
# * RESOURCES * #
# * ********* * #

class ResourcesError(LegionError):
    """Base class for all errors in the `resources` module."""
    
    pass


# * ******** * #
# * SCENARIO * #
# * ******** * #

class ScenarioError(LegionError):
    """Base class for all errors in the `scenario` module."""
    
    pass
