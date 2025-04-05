from collections.abc import Callable, Sequence
import inspect
from typing import Generic, Optional, TypeVar, get_type_hints
import typing
from gi.repository import Gtk, GLib

import logging

from widget.annotate import IntervalCallback, SignalCallback

logger = logging.getLogger(__name__)


class Widget(Gtk.Widget):
    """
    Base class for Borealis-Level abstracted widgets.

    All widgets should inherit from this class (Including custom ones)
    """

    css_classes: Sequence[str]
    """
    This will set the css classes of this widget

    Note that css classes should not be updated after construction, as the provider
    will have already loaded and thus changes to css_classes may not propagate as expected.
    """

    def __init__(self, css_classes: Optional[Sequence[str]] = None, **kwargs):
        """
        Create's a new Borealis Widget.
        This is primarily a class meant to be inherited from.


        Args:
            css_classes (Optional[str], optional): The css_classes of this class.
        """
        Gtk.Widget.__init__(self)

        # Set instance fields based on __init__ args.
        if css_classes is not None:
            self.css_classes = css_classes

        # Attempt to set fields if passed in.
        try:
            self.set_css_classes(self.css_classes)
        except AttributeError:
            pass

        # Add handlers from __dict__ and kwargs
        self._add_signal_handlers(
            list(self.__class__.__dict__.items()) + list(kwargs.items())
        )

        self._add_interval_handlers(
            list(self.__class__.__dict__.items()) + list(kwargs.items())
        )

        self._process_annotations()

    def _process_annotations(self):
        """
        Processes the type annotations of this class,
        Adding handlers when necessary
        """

        # Process annotations for type annotation defined handlers
        for key, value in get_type_hints(self.__class__, include_extras=True).items():
            if isinstance(value, typing._AnnotatedAlias):

                # Get callback from this value
                callback = self.__class__.__dict__[key]

                # Handle signal callbacks
                if value.__origin__ == SignalCallback:
                    for signal_type in value.__metadata__:
                        self._add_signal_handlers(
                            [("on_" + str(signal_type), callback)]
                        )

                # Handle interval callbacks
                if value.__origin__ == IntervalCallback:
                    for interval in value.__metadata__:
                        self._add_interval_handlers(
                            [("interval_" + str(interval), callback)]
                        )

    def _add_interval_handlers(
        self, handlers: list[tuple[str, Callable | Sequence[Callable]]]
    ):
        """
        Adds interval handlers from a list of tuples of intervals (should be convertable to integer)
        to it's handlers

        Args:
             (list[(str, Callable  |  Sequence[Callable])]): The handlers to add.
        """
        for key, value in handlers:

            # Handle interval handler from interval_ vars
            if key.startswith("interval_"):

                # Attempt to convert the remaining bit to the interval
                try:
                    interval = int(key.lstrip("interval_"))
                except ValueError:
                    logging.warning(
                        f"Invalid interval value in class {self.__class__.__name__} for interval handler {key}"
                    )
                    continue

                # Single callback case or list of
                if callable(value):
                    self._register_interval_handler(interval, value)
                elif isinstance(value, list):

                    # Register all sub-callbacks
                    for single_callback in value:
                        if callable(single_callback):
                            self._register_interval_handler(interval, single_callback)
                else:
                    logging.warning(
                        f"Found {key} field in class, But it doesn't correspond to a proper interval handler?"
                    )

    def _add_signal_handlers(
        self, handlers: list[tuple[str, Callable | Sequence[Callable]]]
    ):
        """
        Adds signal handlers from a list of tuples of signal (kebab/snake case) to its handlers

        This does validation on the callbacks, ensuring it is either a Sequence or singular
        callable. If the input passed in is neither, a warning is emitted through the logger.

        Args:
            handlers (list[(str, Callable  |  Sequence[Callable])]): The handlers to add.
        """
        for key, value in handlers:

            # Handle signal handler from on_ vars
            if key.startswith("on_"):

                # Kebab-caseify
                key = key.lstrip("on_").replace("_", "-")

                # Single callback case or list of
                if callable(value):
                    self._register_self_signal_handler(key, value)
                elif isinstance(value, list):

                    # Register all sub-callbacks
                    for single_callback in value:
                        if callable(single_callback):
                            self._register_self_signal_handler(key, single_callback)
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
            return callback(self, *args, **kwargs)

        return wrapper

    def _register_self_signal_handler(self, signal: str, callback: Callable):
        """
        Registers a signal handler which recieves
        self as first argument

        Args:
            signal (str): The signal type
            callback (Callable): The callback for the signal
        """

        try:
            self.connect(signal, self._self_decorator(callback))
        except TypeError:
            logging.error(
                f"No signal of type {signal} exists for class {self.__class__.__name__} with handler name {callback.__name__}"
            )
        else:
            logging.debug(
                f"Registered callback for signal of type {signal} in class {self.__class__.__name__} with name {callback.__name__}"
            )

    def _register_interval_handler(self, interval: int, callback: Callable):
        """
        Registers an interval handler which recieves
        self as first argument

        Args:
            interval (int): The interval in milliseconds to invoke the function
            callback (Callable): The handler
        """

        # Another decorator, this one wraps self decorator
        # so that if the wrapper has no return, we return True instead.
        # allowing interval to repeat without having to explicitly return True
        def interval_wrapper(*args, **kwargs):
            callback_return = self._self_decorator(callback)(*args, **kwargs)

            if callback_return is None:
                return True

            return callback_return

        logging.debug(
            f"Registered callback for interval of length {interval} in class {self.__class__.__name__} with name {callback.__name__}"
        )

        GLib.timeout_add(interval, interval_wrapper)
