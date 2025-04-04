from gi.repository import Gtk
from gi.repository import Gtk4LayerShell as LayerShell
from widget import Widget


class Window(Gtk.Window, Widget):
    """
    The basic window of which all widgets should be constructed
    inside of to be presented.
    """

    def __init__(self):
        Gtk.Window.__init__()
