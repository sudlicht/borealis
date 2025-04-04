import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from collections.abc import Callable


class Borealis:
    """
    A widget and such construction system based off of PyGobject and Gtk4.0

    Aims to abstract away further while providing many useful helpers and providing
    documentation on arguments/types in python.
    """

    def __init__(self, application_id: str):
        """
        Create a new instance of Borealis.

        Args:
            application_id (str): The id of your application e.g com.example.app
        """
        self.app = Gtk.Application(application_id=application_id)

    def on_activate(self, activate_fn: Callable[["Borealis"], None]):
        """
        A decorator for a function which will be called on the GtkApplication
        activate event, This corresponds to the application being launched by the desktop environment.

        Args:
            activate_fn (Callable[["Borealis"]]): A function which takes in this application as its only argument
        """

        # Abstract handler, to use this class instead of the inner app.
        def wrapper(_):
            activate_fn(self)

        self.app.connect("activate", wrapper)
        return wrapper

    def run(self):
        """
        Run's the application displaying the widgets created.
        """
        self.app.run(None)
