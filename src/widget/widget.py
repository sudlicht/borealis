from collections.abc import Callable, Sequence
import inspect
from typing import Generic, Optional, TypeVar, get_type_hints
import typing
from gi.repository import Gtk, GLib

import logging
from widget.annotate import IntervalCallback, OneshotCallback, SignalCallback
from widget.copy_widget import CopyWidget

logger = logging.getLogger(__name__)


class Widget(Gtk.Widget, CopyWidget):
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

    _intervals: list[int]
    """
    Internal map of all the intervals belonging
    to this widget
    """

    auto_unmap: bool = True
    """
    This will automatically remove all interval and oneshot
    handlers on the unmap event
    """

    services_map: bool = True
    """
    Flag that determines if on the map event the service handlers
    should be setup for this widget
    """

    def __init__(self, css_classes: Optional[Sequence[str]] = None, **kwargs):
        """
        Create's a new Borealis Widget.
        This is primarily a class meant to be inherited from.


        Args:
            css_classes (Optional[str], optional): The css_classes of this class.
        """
        Gtk.Widget.__init__(self)
        self._intervals = []

        # Set instance fields based on __init__ args.
        if css_classes is not None:
            self.css_classes = css_classes

        # Attempt to set fields if passed in.
        try:
            self.set_css_classes(self.css_classes)
        except AttributeError:
            pass

        # Add handlers from __dict__
        self._add_base_handlers(
            list(self.__class__.__dict__.items()) + list(kwargs.items())
        )

        self._process_annotations()

        # Auto unmapping of interval handlers when widget
        # goes out of tree
        if self.auto_unmap:
            self.connect("unmap", self._self_decorator(self._unmap))

        if self.services_map:
            self.connect("map", self._self_decorator(self._map_services_setup))

        # Allow passing kwargs down through widget for use by the user.
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Store kwargs for later processing by services
        self._kwargs = kwargs

    def _add_base_handlers(
        self, handlers: list[tuple[str, Callable | Sequence[Callable]]]
    ):
        """
        Adds all of the base widget handlers from a list of handlers
        (Base handlers are oneshot_, on_, interval_)

        Args:
            handlers (list[tuple[str, Callable  |  Sequence[Callable]]]): The handlers to add
        """

        # Add all appropriate handlers for each key
        for key, value in handlers:

            if key.startswith("on_"):
                self._add_signal_handler(key, value)

            if key.startswith("oneshot_"):
                self._add_oneshot_handler(key, value)

            if key.startswith("interval_"):
                self._add_interval_handler(key, value)

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

                # Handle signal callbacks (Gtk4)
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

                if value.__origin__ == OneshotCallback:
                    for interval in value.__metadata__:
                        self._add_oneshot_handlers(
                            [("oneshot_" + str(interval), callback)]
                        )

    def _add_oneshot_handler(
        self, key_oneshot: str, handlers: Callable | Sequence[Callable]
    ):
        """
        Adds a oneshot handler from a oneshot key and it's handlers, doing
        validation on both the oneshot interval and handlers.

        Args:
            key_oneshot (str): The with-prefix interval being added
            handlers (Callable | Sequence[Callable]): A singular or list of callbacks that will be triggered by the interval timeout
        """

        # Oneshot wrapper around intervals
        def get_oneshot_wrapper(callback):

            # Returning False in our wrapper will cancel it 100% of the time.
            def oneshot_wrapper(self, *args, **kwargs):
                callback(self, *args, **kwargs)
                return False

            return oneshot_wrapper

        # Attempt to convert the remaining bit to the interval
        try:
            interval = int(key_oneshot.lstrip("oneshot_"))
        except ValueError:
            logging.warning(
                f"Invalid oneshot interval value in class {self.__class__.__name__} for oneshot handler {key_oneshot}"
            )
            return

        # Single callback case or list of
        if callable(handlers):
            self._register_interval_handler(interval, get_oneshot_wrapper(handlers))
        elif isinstance(handlers, list):

            # Register all sub-callbacks
            for single_callback in handlers:
                if callable(single_callback):
                    self._register_interval_handler(
                        interval, get_oneshot_wrapper(single_callback)
                    )
        else:
            logging.warning(
                f"Found {key_oneshot} field in class, But it doesn't correspond to a proper oneshot handler?"
            )

    def _add_interval_handler(
        self, key_interval: str, handlers: Callable | Sequence[Callable]
    ):
        """
        Adds a interval handler from an interval and it's handlers, doing
        validation on both the interval and handlers.

        Args:
            key_interval (str): The with-prefix interval being added
            handlers (Callable | Sequence[Callable]): A singular or list of callbacks that will be triggered by the interval timeout
        """

        # Attempt to convert the remaining bit to the interval
        try:
            interval = int(key_interval.lstrip("interval_"))
        except ValueError:
            logging.warning(
                f"Invalid interval value {key_interval} in class {self.__class__.__name__} for interval handler {key_interval}"
            )
            return

        # Single callback case or list of
        if callable(handlers):
            self._register_interval_handler(interval, handlers)
        elif isinstance(handlers, list):

            # Register all sub-callbacks
            for single_callback in handlers:
                if callable(single_callback):
                    self._register_interval_handler(interval, single_callback)
        else:
            logging.warning(
                f"Found {key_interval} field in class, But it doesn't correspond to a proper interval handler?"
            )

    def _add_signal_handler(self, signal: str, handlers: Callable | Sequence[Callable]):
        """
        Adds a signal handler to this widget, with validation on the signal and the
        callback.

        Args:
            signal (str): The with-prefix name of the signal being added
            handlers (Callable | Sequence[Callable]): A singular or list of callbacks that will be triggered by the signal as its handler.
        """

        # Kebab-caseify
        signal = signal.lstrip("on_").replace("_", "-")

        # Single callback case or list of
        if callable(handlers):
            self._register_self_signal_handler(signal, handlers)
        elif isinstance(handlers, list):

            # Register all sub-callbacks
            for single_callback in handlers:
                if callable(single_callback):
                    self._register_self_signal_handler(signal, single_callback)
        else:
            logging.warning(
                f"Found on_{signal} field in class, But it doesn't correspond to a proper signal handler?"
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

        self._intervals.append(GLib.timeout_add(interval, interval_wrapper))

    def b_get_borealis(self) -> Optional[any]:
        """
        Get's the borealis instance this widget
        is associated with.
        """

        try:
            return self.get_root().b_root
        except AttributeError:
            return

    def _destroy_intervals(self):
        """
        This will destroy all of the intervals
        associated with this widget.
        """
        for interval in self._intervals:
            GLib.source_remove(interval)

    def _unmap(self, *args, **kwargs):
        """
        This function will remove all this
        widgets mapped handlers
        """

        logging.debug(f"Automatically unmapping for widget {self.__class__.__name__}")

        self._destroy_intervals()

    def _map_services_setup(self, *args, **kwargs):
        """
        Set's up the service handlers for this widget
        Since we require communicating with the borealis instance
        this belongs with.
        """
