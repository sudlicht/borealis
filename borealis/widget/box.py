from gi.repository import Gtk
from borealis.widget.b_orientable import B_Orientable
from borealis.widget.widget import Widget
from borealis.widget.enums import Orientation
from typing import Optional


class Box(Gtk.Box, Widget, B_Orientable):
    """
    A simple container box widget which can store
    widgets in either the horizontal or vertical direction (row/column)
    """

    children: list[Widget] | Widget = []
    """
    The children of this box.
    """

    def __init__(
        self,
        orientation: Optional[Orientation] = None,
        children: Optional[list[Widget] | Widget] = None,
        **kwargs
    ):
        """
        Create a new box container element

        Args:
            orientation (Optional[Orientation], optional): The orientation of the box (direction of children)
            children (Optional[list[Widget] | Widget], optional): The children of the box
        """

        Gtk.Box.__init__(self)
        Widget.__init__(self, **kwargs)

        # Set instance fields based on __init__ args.

        # Allow support for passing in a single widget as children.
        if isinstance(self.children, Widget):
            self.children = [self.children]

        if children is not None:
            if isinstance(children, Widget):
                children = [children]

            self.children = self.children + children

        if orientation is not None:
            self.orientation = orientation

        self.b_add_children(self.children)
        self.b_set_orientation(self.orientation)

    def b_add_children(self, children: list[Widget]):
        """
        Adds a list of widgets to this box as its children

        Args:
            children (list[Widget]): The widgets to add
        """

        for child in children:
            self.append(child._reinitialise_widget())
