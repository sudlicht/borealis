from enum import Enum
from gi.repository import Gtk4LayerShell


class LayerShellLayer(Enum):
    """
    gtk4-layer-shell Layer abstraction for proper
    typing/IDE support
    """

    TOP = Gtk4LayerShell.Layer.TOP
    """
    The top layer.
    """

    BACKGROUND = Gtk4LayerShell.Layer.BACKGROUND
    """
    The background layer.
    """

    BOTTOM = Gtk4LayerShell.Layer.BOTTOM
    """
    The bottom layer.
    """

    OVERLAY = Gtk4LayerShell.Layer.OVERLAY
    """
    The overlay layer.
    """


class LayerShellEdge(Enum):
    """
    gtk4-layer-shell Edge abstraction for proper
    typing/IDE support
    """

    LEFT = Gtk4LayerShell.Edge.LEFT
    """
    The left edge of the screen.
    """

    RIGHT = Gtk4LayerShell.Edge.RIGHT
    """
    The right edge of the screen.
    """

    TOP = Gtk4LayerShell.Edge.TOP
    """
    The top edge of the screen.
    """

    BOTTOM = Gtk4LayerShell.Edge.BOTTOM
    """
    The bottom edge of the screen.
    """
