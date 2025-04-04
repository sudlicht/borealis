from collections.abc import Callable
from typing import Optional
from gi.repository import Gtk

import logging

logger = logging.getLogger(__name__)


class Widget(Gtk.Widget):
    """
    Base class for Borealis-Level abstracted widgets.

    All widgets should inherit from this class (Including custom ones)
    """

    css_name: str
    """
    This will set the css name of this widget
    """

    def __init__(self, css_name: Optional[str] = None):
        """
        Create's a new Borealis Widget.
        This is primarily a class meant to be inherited from.


        Args:
            css_name (Optional[str], optional): The css_name of this class.
        """
        Gtk.Widget.__init__(self)

        # Set instance fields based on __init__ args.
        if css_name is not None:
            self.css_name = css_name

        # Attempt to set fields if passed in.
        try:
            self.b_set_css_name(self.css_name)
        except AttributeError:
            pass

        # Add signal handlers on_* callback
        for key, value in self.__class__.__dict__.items():

            # Handle signal handler.
            if key.startswith("on_"):
                key = key.lstrip("on_")

                # Single callback case or list of
                if callable(value):
                    self._register_self_signal_handler(key, value)
                elif isinstance(value, list):

                    # Register all sub-callbacks
                    for callback in value:
                        if callable(callback):
                            self._register_self_signal_handler(key, callback)
                else:
                    logging.warning(
                        f"Found on_{key} field in class, But it doesn't correspond to a proper signal handler?"
                    )

    def _self_decorator(self, callback: Callable) -> Callable:
        """
        Simple decorator that adds this widget as first argument
        to a callback

        Args:
            callback (Callable): A callback which takes any arguments

        Returns:
            Callable: The callback wrapped, with this widget as its new
            first argument.
        """

        def wrapper(*args, **kwargs):
            callback(self, *args, **kwargs)

        return wrapper

    def _register_self_signal_handler(self, signal: str, callback: Callable):
        """
        Registers a signal handler which recieves
        self as first argument

        Args:
            signal (str): The signal type
            callback (Callable): The callback for the signal
        """
        logging.debug(
            f"Registered callback for signal of type {signal} in class {self.__class__.__name__}"
        )

        self.connect(signal, self._self_decorator(callback))

    def b_set_css_name(self, css_name: str):
        """
        Set's the css_name attribute of this Widget

        Args:
            css_name (str): The new name
        """
        self.css_name = css_name
        self.add_css_class(css_name)
