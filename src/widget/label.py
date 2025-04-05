from collections.abc import Callable
from gi.repository import Gtk
from widget.widget import Widget
from typing import Optional


class Label(Gtk.Label, Widget):
    """
    A widget used for displaying text
    """

    label: str
    """
    The text of the label
    """

    def __init__(self, label: Optional[str] = None, **kwargs):
        """
        Creates a new label for displaying text with

        Args:
            label (Optional[str], optional): the text to display inside the label

        **kwargs will be passed down to Widget**

        Args:
            label (Optional[str], optional): _description_. Defaults to None.
        """
        Gtk.Label.__init__(self)
        Widget.__init__(self, **kwargs)

        # Set instance fields based on __init__ args.
        if label is not None:
            self.label = label

        self.set_label(self.label)
