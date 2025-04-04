from typing import Optional
from borealis_logging import BorealisFormatter
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gtk, Gdk
from widget.window import Window

import logging

# Setup library level logging for the end-user
logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# Use custom formatter which has coloured outputs
stream_handler.setFormatter(BorealisFormatter())
logger.addHandler(stream_handler)


class Borealis:
    """
    A widget and such construction system based off of PyGobject and Gtk4.0

    Aims to abstract away further while providing many useful helpers and providing
    documentation on arguments/types in python.
    """

    DEFAULT_APPLICATION_ID: str = "com.example.app"

    application_id: str
    """
    The application id of this Borealis application. e.g com.example.app
    """

    root: Window
    """
    The root window belonging to this application

    Will automatically be initialised on the activate signal from gtk.
    """

    css_file: Optional[str]
    """
    The path to a css file that will be used for styling this borealis
    instance.
    """

    _app: Gtk.Application
    """
    The internal Gtk Application this Borealis application is using for Gtk4
    """

    _css_provider: Gtk.CssProvider
    """
    Underlying provider for css to the GTK4 side of Borealis
    """

    def __init__(self):
        """
        Create a new instance of Borealis.
        """

        # Create underlying Gtk Application with the passed in application id.
        try:
            self._app = Gtk.Application(application_id=self.application_id)
        except:
            logger.warning(
                f"Missing application_id field in {self.__class__.__name__}, using default"
            )
            self._app = Gtk.Application(application_id=self.DEFAULT_APPLICATION_ID)

        # Create css provider
        self._css_provider = Gtk.CssProvider()

        if hasattr(self, "css_file"):
            # Add our style.css file.
            self._css_provider.load_from_path(self.css_file)

            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                self._css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )
        else:
            logger.info(
                f"No css_file field in {self.__class__.__name__}, No css will be used."
            )

    def _activate(self):
        """
        Creates a handler to initialise the root window.

        This returns a handler that should be called on the gtk application activate signal.
        """

        def activate_handler(_):
            try:
                self.root(self._app)
            except AttributeError as e:
                logger.critical(
                    f"Borealis application is missing a required field! {e}"
                )
                exit(1)

        return activate_handler

    @classmethod
    def run(cls):
        """
        Run's the application displaying the widgets created.
        """

        # Create and run our class
        self: Borealis = cls()
        self._app.connect("activate", self._activate())
        self._app.run(None)
