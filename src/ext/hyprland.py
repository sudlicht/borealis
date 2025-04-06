import threading
import time
from service.base_service import BaseService, ServiceSignal
import os

from service.service_annotate import ServiceAnnotation


class HyprlandCallback(ServiceAnnotation):
    prefix = "hyprland_on"


class HyprlandService(BaseService):
    """
    A service for Hyprland events.
    """

    annotation = HyprlandCallback()
    """
    Use this annotation when registering handlers for the Hyprland service.
    """

    xdg_runtime_dir: str = os.environ["XDG_RUNTIME_DIR"]
    """
    Hyprland sockets exists in $XDG_RUNTIME_DIR/hypr
    """

    hyprland_instance_signature: str = os.environ["HYPRLAND_INSTANCE_SIGNATURE"]
    """
    Required for finding location of socket2, exists as a directory under
    $XDG_RUNTIME_DIR/hypr
    """

    socket2_path: str = os.path.abspath(
        f"{xdg_runtime_dir}/hypr/{hyprland_instance_signature}/.socket2.sock"
    )
    """
    Path to the hyprland socket2 (used for recieving events)
    """

    def start_service(self):
        """
        Start's the hyprland service
        """
        print("Starting hyprland service")
        print(f"Hyprland thread: {threading.get_ident()}")

        # Open async connection to hyprland socket
        while True:
            time.sleep(10)
            self.emit_signal(ServiceSignal(signal="hyprland_test"))
