import logging
from typing import Optional
from service.service_annotate import ServiceAnnotation
from service.service_signal import ServiceSignal
from widget.widget import Widget
from gi.repository import GLib


logger = logging.getLogger(__name__)


class BaseService:
    """
    Base class for all services which should
    inherit from this class
    """

    annotation: ServiceAnnotation
    """
    The annotation for this service to allow widgets
    to use it's signals
    """

    _attached_widgets: dict[Widget, list[str]]
    """
    The widgets attached to this service that will recieve
    the signals from this service
    """

    def __init__(self, annotation: Optional[ServiceAnnotation] = None):
        """
        Creates a new Service for recieving and sending signals
        from non-gtk4 things

        Args:
            annotation (Optional[ServiceAnnotation], optional): The annotation information to use for widgets for this service.
        """
        if annotation is not None:
            self.annotation = annotation

        # Make sure we have annotations! We need the prefix for our signals
        try:
            logger.debug(
                f"Initialising new service {self.__class__.__name__} with annotation {self.annotation.__class__.__name__}"
            )
        except AttributeError:
            logger.error(
                f"Service {self.__class__.__name__} is missing its annotation! Please ensure it has one."
            )
            exit(1)

        self._attached_widgets = {}

    def start_service(self):
        """
        Starting routine for this service,
        will be called when this service should
        start sending events

        This will be executed in a different thread
        """
        pass

    def emit_signal(self, signal: ServiceSignal):
        """
        Emit's a signal across all widgets which are listening
        to this signal from this service

        Args:
            signal (ServiceSignal): The signal being emitted
        """

        GLib.idle_add(self._run_signal, signal)

    def _run_signal(self, signal: ServiceSignal):
        """
        Hi

        Args:
            signal (ServiceSignal): The signal being ran
        """

        # Emit signal for all the widgets
        for widget, signals in self._attached_widgets.items():
            if signal.signal in signals:
                widget.emit(self.annotation.get_prefix() + signal.signal, *signal.args)

    def get_annotation(self):
        """
        Returns the annotation of this service
        """

        return self.annotation

    def attach_widget(self, widget: Widget, signal: str):
        """
        Adds a widget to this service, enabling for it
        to recieve this specific signal from this service

        Args:
            widget (Widget): The widget to add to this service
        """

        try:
            self._attached_widgets[widget].append(signal)
        except KeyError:
            self._attached_widgets[widget] = [signal]

    def detach_widget(self, widget: Widget):
        """
        Remove's this widget from this service
        thus stopping the widget from recieving signals from this service.

        Args:
            widget (Widget): The widget to detach
        """

        self._attached_widgets.pop(widget, None)

    def get_signal_arg_types(self, signal: str) -> tuple[any] | None:
        """
        This function should return the signal's arg types
        for registering a signal under this service

        This is also used for validation of if a signal exists for widgets!

        Args:
            signal (str): The signal

        Returns:
            tuple[any]: A tuple of the arguments to this signal's handlers
        """
        pass
