import asyncio
import logging
from queue import Queue
import threading
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

    _attached_widgets: list[Widget]
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

        self._attached_widgets = []

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
        for widget in self._attached_widgets:
            widget.emit(signal.signal, *signal.args)

    def get_annotation(self):
        """
        Returns the annotation of this service
        """

        try:
            return self.annotation
        except AttributeError:
            return None
