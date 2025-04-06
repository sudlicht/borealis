import logging
from typing import Optional

from borealis_logging import BorealisFormatter

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# Use custom formatter which has coloured outputs
stream_handler.setFormatter(BorealisFormatter())
logger.addHandler(stream_handler)


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
            logger.error(f"Service {self.__class__.__name__} is missing prefix")
            exit(1)

    def get_prefix(self):
        """
        Returns the prefix of this service annotation
        """

        return self.prefix
