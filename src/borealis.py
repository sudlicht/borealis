import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

class Borealis():
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
        self.app = Gtk.Application()

    def run(self):
        """
        Run's the application displaying the widgets created.
        """
        pass

