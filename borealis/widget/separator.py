from typing import Optional
from gi.repository import Gtk
from widget.b_orientable import B_Orientable
from widget import Orientation, Widget


class Separator(Gtk.Separator, Widget, B_Orientable):
    """
    A horizontal or vertical line to separate other widgets.
    """

    orientation: Orientation = Orientation.VERTICAL
    """
    The orientation of the box, this is the plane of
    which the children will be in
    """

    def __init__(self, orientation: Optional[Orientation] = None, **kwargs):
        """
        Create a new separator element

        Args:
            orientation (Optional[Orientation], optional): The orientation of the separator (whether it should run horizontal or vertical)
        """

        Gtk.Separator.__init__(self)
        Widget.__init__(self, **kwargs)

        # Set instance fields based on __init__ args.
        if orientation is not None:
            self.orientation = orientation

        self.b_set_orientation(self.orientation)
