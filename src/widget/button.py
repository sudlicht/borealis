from typing import Optional
from gi.repository import Gtk
from widget.widget import Widget


class Button(Gtk.Button, Widget):
    """
    A simple Gtk4 button that can respond to click events
    and such.
    """

    child: Widget
    """
    The sole child of this button.
    """

    def __init__(self, child: Optional[Widget] = None, **kwargs):
        """
        Create's a new button

        Args:
            child (Optional[Widget], optional): The child of this button
        """
        Gtk.Button.__init__(self)
        Widget.__init__(self, **kwargs)

        if child is not None:
            self.child = child

        self.b_set_child(self.child)

    def b_set_child(self, child: Widget):
        """
        Set's the child of this button to a new
        Widget node.

        Args:
            child (Widget): The new child of this button
        """
        self.child = child
        self.set_child(child)
