class LegionError(Exception):
    """
    Base class for all errors in the project.
    """
    pass


# * ******** * #
# * BUILDING * #
# * ******** * #

class BuildingError(LegionError):
    """
    Base class for all errors in the `building` module.
    """
    pass


# * **** * #
# * CITY * #
# * **** * #

class CityError(LegionError):
    """
    Base class for all errors in the `city` module.
    """
    pass


# * ******* * #
# * DISPLAY * #
# * ******* * #

class DisplayError(LegionError):
    """
    Base class for all errors in the `display` module.
    """
    pass


# * ******* * #
# * EFFECTS * #
# * ******* * #

class EffectsError(LegionError):
    """
    Base class for all errors in the `effects` module.
    """
    pass


# * ************ * #
# * GEO FEATURES * #
# * ************ * #

class GeoFeaturesError(LegionError):
    """
    Base class for all errors in the `geo_features` module.
    """
    pass


# * ******* * #
# * KINGDOM * #
# * ******* * #

class KingdomError(LegionError):
    """
    Base class for all errors in the `kingdom` module.
    """
    pass


# * ********* * #
# * RESOURCES * #
# * ********* * #

class ResourcesError(LegionError):
    """
    Base class for all errors in the `resources` module.
    """
    pass


# * ******** * #
# * SCENARIO * #
# * ******** * #

class ScenarioError(LegionError):
    """
    Base class for all errors in the `scenario` module.
    """
    pass
