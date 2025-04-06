import logging

logger = logging.getLogger(__name__)


class ServiceAnnotation:
    """
    Represents information relating to the annotation
    of widgets in order to hook into your service
    """

    prefix: str
    """
    Required prefix, which can be used as an argument/classvar
    for widgets to hook into your service signals.

    such that prefix_<signal> will automatically register that
    widget for this service's signal of that name

    Note that "interval", "oneshot" is already used as a prefix for intervals
    and "on" is taken by Gtk4 signals.

    Do not use '_' as a separator, Use '-' only.
    """

    def __init__(self):
        """
        Initialises this service annotation and does some useful
        checking to ensure the correct functionality
        """

        # Definitely dont want people to be using ServiceAnnotation directly
        if self.__class__ is ServiceAnnotation:
            logger.error(
                f"Please subclass ServiceAnnotation instead of using it directly in {self.__class__.__name__}"
            )
            exit(1)

        # Ensure we have a prefix! Else this wont work properly.
        try:
            logger.debug(f"Initialising service annotation with prefix {self.prefix}")
        except AttributeError:
            logger.error(
                f"Service {self.__class__.__name__} is missing its prefix, Please insure it has one!"
            )
            exit(1)

    def get_prefix(self):
        """
        Returns the prefix of this service annotation
        """

        return self.prefix
