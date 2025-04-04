from gi.repository import Gtk
from widget import Widget
from enums.orientation import Orientation


class Box(Widget, Gtk.Box):
    """
    Arranges child widgets into a single row or column
    """

    def __init__(
        self, orientation: Orientation = Orientation.HORIZONTAL, *args: Widget
    ):
        """
        Create a new Box widget

        Args:
            orientation (Orientation, optional): The orientation of the box, Horizontal for row, Vertical for column. Defaults to Orientation.HORIZONTAL.
            *args (Widget): The children of the box, pass in any widgets to add it to this box.
        """
        Gtk.Box.__init__(orientation=orientation.value)

        # Add all passed in widgets to this box.
        for widget in args:
            self.append(widget)
