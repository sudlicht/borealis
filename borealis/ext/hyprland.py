import time
from borealis.service import BaseService, ServiceSignal, ServiceAnnotation
import os


class HyprlandCallback(ServiceAnnotation):
    prefix = "hyprland-on"


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

        # Open async connection to hyprland socket
        while True:
            time.sleep(1)
            self.emit_signal(ServiceSignal("hyprland-test", 5))

    def get_signal_arg_types(self, signal: str) -> tuple[any]:
        """
        Validation method for hyprland signals, also used for retrieving
        the arguments to a hyprland singal's callback.
        """

        match signal:
            case "hyprland-test":
                return (int,)
