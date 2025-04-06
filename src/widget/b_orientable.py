from gi.repository import Gtk
from widget.enums import Orientation


class B_Orientable(Gtk.Widget, Gtk.Orientable):
    """
    Orientable from GTK but with support for
    borealis Orientation
    """

    orientation: Orientation = Orientation.HORIZONTAL
    """
    The orientation of the box, this is the plane of
    which the children will be in
    """

    def b_set_orientation(self, orientation: Orientation):
        """
        Set's the orientation of this box to a certain orientation

        Args:
            orientation (Orientation): The new orientation of the box
        """
        self.set_orientation(orientation.value)
