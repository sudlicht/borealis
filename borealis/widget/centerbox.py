from gi.repository import Gtk
from widget.b_orientable import B_Orientable
from widget import Widget, Orientation
from typing import Optional


class CenterBox(Gtk.CenterBox, Widget, B_Orientable):
    """
    Arranges three children in a row, keeping the middle child centered as well as possible.
    """

    start: Widget
    """
    The widget at the start
    """

    center: Widget
    """
    The widget in the middle
    """

    end: Widget
    """
    The widget at the end
    """

    def __init__(
        self,
        orientation: Optional[Orientation] = None,
        start: Optional[Widget] = None,
        center: Optional[Widget] = None,
        end: Optional[Widget] = None,
        **kwargs
    ):
        """
        Creates a new centerbox container element

        Args:
            orientation (Optional[Orientation], optional): The orientation of the centerbox, column vs row
            start (Optional[Widget], optional): The widget at the start of the centerbox
            center (Optional[Widget], optional): The centred widget in the centerbox
            end (Optional[Widget], optional): The widget at the end.
        """

        Gtk.CenterBox.__init__(self)
        Widget.__init__(self, **kwargs)

        # Set instance fields based on __init__ args.
        if orientation is not None:
            self.orientation = orientation

        if start is not None:
            self.start = start

        if center is not None:
            self.center = center

        if end is not None:
            self.end = end

        self.b_set_orientation(self.orientation)

        # Set widgets
        if hasattr(self, "start"):
            self.b_set_start_widget(self.start)

        if hasattr(self, "center"):
            self.b_set_center_widget(self.center)

        if hasattr(self, "end"):
            self.b_set_end_widget(self.end)

    def b_set_start_widget(self, widget: Widget):
        """
        Set's the start widget of this centerbox to a new widget

        Args:
            widget (Widget): The widget
        """
        self.start = widget._reinitialise_widget()
        self.set_start_widget(self.start)

    def b_set_center_widget(self, widget: Widget):
        """
        Set's the center widget of this centerbox to a new widget

        Args:
            widget (Widget): The widget
        """
        self.center = widget._reinitialise_widget()
        self.set_center_widget(self.center)

    def b_set_end_widget(self, widget: Widget):
        """
        Set's the end widget of this centerbox to a new widget

        Args:
            widget (Widget): The widget
        """

        self.end = widget._reinitialise_widget()
        self.set_end_widget(self.end)
