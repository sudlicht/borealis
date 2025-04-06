from collections.abc import Callable, Sequence
import inspect
from typing import Generic, Optional, TypeVar, get_type_hints
import typing
from gi.repository import Gtk, GLib, GObject

import logging
from service.service_annotate import ServiceAnnotation
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
    This will automatically remove all interval, services and oneshot
    handlers on the unmap event
    """

    services_map: bool = True
    """
    Flag that determines if on the map event the service handlers
    should be setup for this widget
    """

    _attached_services: set
    """
    A list of services this widget is attached to.
    Used for keeping track for unmapping this widget from them later.
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
        self._attached_services = set()

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

        self._process_base_annotations()

        # Auto unmapping of interval handlers when widget
        # goes out of tree
        if self.auto_unmap:
            self.connect("unmap", self._self_decorator(self._unmap))

        # Mapping for services setup for this widget
        if self.services_map:
            self.connect(
                "map",
                lambda _: self._map_services_setup(
                    list(self.__class__.__dict__.items()) + list(kwargs.items())
                ),
            )

        # Allow passing kwargs down through widget for use by the user.
        for key, value in kwargs.items():
            setattr(self, key, value)

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

    def _process_base_annotations(self):
        """
        Processes the type annotations of this class,
        Adding handlers for base non-service handlers when necessary
        """

        # Process annotations for type annotation defined handlers
        for key, value in get_type_hints(self.__class__, include_extras=True).items():
            if isinstance(value, typing._AnnotatedAlias):

                # Get callback from this value
                callback = self.__class__.__dict__[key]
                origin = value.__origin__

                # Handle signal callbacks (Gtk4)
                if origin == SignalCallback:
                    for signal_type in value.__metadata__:
                        self._add_signal_handler("on_" + str(signal_type), callback)

                # Handle interval callbacks
                if origin == IntervalCallback:
                    for interval in value.__metadata__:
                        self._add_interval_handler(
                            "interval_" + str(interval), callback
                        )

                if origin == OneshotCallback:
                    for interval in value.__metadata__:
                        self._add_oneshot_handler("oneshot_" + str(interval), callback)

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
            interval = int(key_oneshot.removeprefix("oneshot_"))
        except ValueError:
            logging.warning(
                f"Invalid oneshot interval value in {self.__class__.__name__} for oneshot handler {key_oneshot}"
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
                f"Found {key_oneshot} field in {self.__class__.__name__}, But it's value is not a list of or a single callable oneshot handler?"
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
            interval = int(key_interval.removeprefix("interval_"))
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
                f"Found {key_interval} field in {self.__class__.__name__}, But it's value is not a list of or a single callable interval handler?"
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
        signal = signal.removeprefix("on_").replace("_", "-")

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
                f"Found on_{signal} field in {self.__class__.__name__}, But it's value is not a list of or a single callable signal handler?"
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

        self.connect(signal, self._self_decorator(callback))

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

    def _destroy_services(self):
        """
        This will destroy all of the service emitters
        related to this widget
        """

        for service in self._attached_services:
            service.detach_widget(self)

    def _unmap(self, *args, **kwargs):
        """
        This function will remove all this
        widgets mapped handlers
        """

        logging.debug(f"Automatically unmapping for widget {self.__class__.__name__}")

        self._destroy_services()
        self._destroy_intervals()

    def _map_services_setup(
        self, handlers: list[tuple[str, Callable | Sequence[Callable]]]
    ):
        """
        Set's up the service handlers for this widget

        Args:
            handlers (list[tuple[str, Callable  |  Sequence[Callable]]]): The handlers to add
        """
        self._add_service_handlers(handlers)
        self._process_service_annotations()

    def _add_service_handlers(
        self, handlers: list[tuple[str, Callable | Sequence[Callable]]]
    ):
        """
        This will add all the handlers for all services in the provided list
        to this widget, processing all the ones that match a service.

        Args:
            handlers (list[tuple[str, Callable  |  Sequence[Callable]]]): The handlers to add
        """
        # The borealis instance
        borealis = self.b_get_borealis()

        # Get all the service prefixes
        service_prefixes = borealis.get_services_prefix_list()

        # Process all handlers
        for key, value in handlers:

            # Convert key from snake to kebab case
            kebab_key = key.replace("_", "-")

            # Find a match
            for service in service_prefixes:
                if not kebab_key.startswith(service):
                    continue

                # We found a match so now process it

                # Signal that we are attaching to
                key_signal = kebab_key.removeprefix(service + "-")

                # Get it's corresponding service
                service = borealis.get_service_from_prefix(service)

                # Now add all of the callbacks
                if callable(value):
                    self._register_service_callback(service, key_signal, value)
                elif isinstance(value, list):

                    # Register all sub-callbacks
                    for single_callback in value:
                        if callable(single_callback):
                            self._register_service_callback(
                                service, key_signal, single_callback
                            )
                else:
                    logging.warning(
                        f"Found {key} field in {self.__class__.__name__}, But it's value is not a list of or a single callable service handler?"
                    )

    def _process_service_annotations(self):
        """
        Processes the type annotations of this class,
        Adding handlers for service handlers when necessary

        This should only be ran when the borealis
        instance of this widget is clear.
        """

        # The borealis instance
        borealis = self.b_get_borealis()

        # Process annotations for type annotation defined handlers
        for key, value in get_type_hints(self.__class__, include_extras=True).items():
            if isinstance(value, typing._AnnotatedAlias):

                # Get callback from this value
                callback = self.__class__.__dict__[key]
                origin = value.__origin__

                # Quick check to get rid of all the non-service ones
                if (
                    origin == SignalCallback
                    or origin == IntervalCallback
                    or origin == OneshotCallback
                ):
                    continue

                service: Optional[any] = borealis.get_service(origin)

                # Warn user about a non-existant service
                if service is None:
                    logging.warning(
                        f"No service exists for annotation {origin.__name__} when attempting to add services for {self.__class__.__name__}"
                    )
                    continue

                # Register the callback/signal
                for signal in value.__metadata__:
                    self._register_service_callback(service, signal, callback)

    def _register_service_callback(self, service, signal: str, callback: Callable):
        """
        Registers a handler from this widget under a certain signal
        to a service

        Args:
            service (BaseService): The service to attach this widget to
            signal (str): The name of the signal from the service
            callback (Callable): The handler of this signal
        """
        # Validation/getting args from this service.
        signal_args = service.get_signal_arg_types(signal)

        # Validation on signal existing.
        if signal_args is None:
            logging.warning(
                f"No signal exists under name {signal} for service "
                f"{service.__class__.__name__} when attempting to register "
                f"callback for {self.__class__.__name__} with callback {callback.__name__}"
            )
            return

        # All service signals start with their prefix for uniqueness.
        service_prefix = service.get_annotation().get_prefix()

        # Add signal handler (or make signal if it doesnt exist)
        try:
            self._register_self_signal_handler(service_prefix + signal, callback)
        except TypeError:
            # Create signal on our widget if it doesn't have the signal
            GObject.signal_new(
                service_prefix + signal,
                self,
                GObject.SignalFlags.RUN_FIRST,
                None,  # Return type of signal
                signal_args,
            )

            self._register_self_signal_handler(service_prefix + signal, callback)

        # Register service to emit signals through this widget
        if service not in self._attached_services:
            self._attached_services.add(service)

        service.attach_widget(self, signal)
