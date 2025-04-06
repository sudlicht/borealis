from enum import Enum
from gi.repository import Gtk


class Orientation(Enum):
    """
    Represents the orientation of widgets and other objects.
    """

    HORIZONTAL = Gtk.Orientation.HORIZONTAL
    """
    The element is in horizontal orientation.
    """

    VERTICAL = Gtk.Orientation.VERTICAL
    """
    The element is in vertical orientation.
    """
