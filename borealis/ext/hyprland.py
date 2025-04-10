import socket
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

    socket2_recv_bytes: int = 1024
    """
    The amount of bytes to recieve from socket2 at a time, this should be set
    such that all possible messages can fit into this size
    """

    socket2_path: str = os.path.abspath(
        f"{xdg_runtime_dir}/hypr/{hyprland_instance_signature}/.socket2.sock"
    )
    """
    Path to the hyprland socket2 (used for recieving events)
    """

    def send_hyprland_event(self, event: str):
        """
        Parses and sends events to borealis from hyprland by the string
        of the event

        None of the event data is type cast and all will be sent through the
        event as a string.

        Args:
            event (str): The stringified version of the event, Currently this format is EVENT>>DATA
        """

        # Split on the event name/data delimiter
        (event_name, event_data) = event.split(">>")

        # Data is delimited by commas (for now..)
        signal_args = event_data.split(",")

        # Send signal
        self.emit_signal(ServiceSignal(event_name, *signal_args))

    def start_service(self):
        """
        Start's the hyprland service
        """

        # Use socket context manager since it's simpler and more clean.
        hyprland_client: socket.socket
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as hyprland_client:

            # Connect to hyprland socket and recieve events
            hyprland_client.connect(self.socket2_path)
            while True:
                socket2_event = hyprland_client.recv(self.socket2_recv_bytes)

                # Every event is in a string format, so decode from bytes
                decoded_events = socket2_event.decode()

                # Hyprland sends multiple events at once, each event ends with a new line.
                events_list = decoded_events.splitlines()

                for event in events_list:
                    self.send_hyprland_event(event)

    def get_signal_arg_types(self, signal: str) -> tuple[any]:
        """
        Validation method for hyprland signals, also used for retrieving
        the arguments to a hyprland singal's callback.

        (Also all events and their types if you are reading this!)
        """

        match signal:
            # WORKSPACENAME
            case "workspace":
                return (str,)

            # WORKSPACEID,WORKSPACENAME
            case "workspacev2":
                return (
                    str,
                    str,
                )

            # MONNAME,WORKSPACENAME
            case "focusedmon":
                return (
                    str,
                    str,
                )

            # MONNAME,WORKSPACEID
            case "focusedmonv2":
                return (
                    str,
                    str,
                )

            # WINDOWCLASS,WINDOWTITLE
            case "activewindow":
                return (
                    str,
                    str,
                )

            # WINDOWADDRESS
            case "activewindowv2":
                return (str,)

            # 0/1 ( EXIT / ENTER )
            case "fullscreen":
                return (str,)

            # MONITORNAME
            case "monitorremoved":
                return (str,)

            # MONITORNAME
            case "monitoradded":
                return (str,)

            # MONITORID,MONITORNAME,MONITORDESCRIPTION
            case "monitoraddedv2":
                return (
                    str,
                    str,
                    str,
                )

            # WORKSPACENAME
            case "createworkspace":
                return (str,)

            # WORKSPACEID,WORKSPACENAME
            case "createworkspacev2":
                return (
                    str,
                    str,
                )

            # WORKSPACENAME
            case "destroyworkspace":
                return (str,)

            # WORKSPACEID,WORKSPACENAME
            case "destroyworkspacev2":
                return (str, str)

            # WORKSPACENAME,MONNAME
            case "moveworkspace":
                return (
                    str,
                    str,
                )

            # WORKSPACEID,WORKSPACENAME,MONNAME
            case "moveworkspacev2":
                return (
                    str,
                    str,
                    str,
                )

            # WORKSPACEID,NEWNAME
            case "renameworkspace":
                return (
                    str,
                    str,
                )

            # WORKSPACENAME,MONNAME
            case "activespecial":
                return (str,)

            # WORKSPACEID,WORKSPACENAME,MONNAME
            case "activespecialv2":
                return (
                    str,
                    str,
                    str,
                )

            # KEYBOARDNAME,LAYOUTNAME
            case "activelayout":
                return (
                    str,
                    str,
                )

            # WINDOWADDRESS,WORKSPACENAME,WINDOWCLASS,WINDOWTITLE
            case "openwindow":
                return (
                    str,
                    str,
                    str,
                    str,
                )

            # WINDOWADDRESS
            case "closewindow":
                return (str,)

            # WINDOWADDRESS,WORKSPACENAME
            case "movewindow":
                return (
                    str,
                    str,
                )

            # WINDOWADDRESS,WORKSPACEID,WORKSPACENAME
            case "movewindowv2":
                return (
                    str,
                    str,
                    str,
                )

            # NAMESPACE
            case "openlayer":
                return (str,)

            # NAMESPACE
            case "closelayer":
                return (str,)

            # SUBMAPNAME
            case "submap":
                return (str,)

            # WINDOWADDRESS,FLOATING (0 or 1)
            case "changefloatingmode":
                return (
                    str,
                    str,
                )

            # WINDOWADDRESS
            case "urgent":
                return (str,)

            # STATE,OWNER
            case "screencast":
                return (
                    str,
                    str,
                )

            # WINDOWADDRESS
            case "windowtitle":
                return (str,)

            # WINDOWADDRESS,WINDOWTITLE
            case "windowtitlev2":
                return (
                    str,
                    str,
                )

            # 0/1, WINDOWADDRESSES
            case "togglegroup":
                return (
                    str,
                    str,
                )

            # WINDOWADDRESS
            case "moveintogroup":
                return (str,)

            # WINDOWADDRESS
            case "moveoutofgroup":
                return (str,)

            # 0/1
            case "ignoregrouplock":
                return (str,)

            # 0/1
            case "lockgroups":
                return (str,)

            # empty
            case "configreloaded":
                return ()

            # WINDOWADDRESS,PINSTATE
            case "pin":
                return (
                    str,
                    str,
                )

            # WINDOWADDRESS,0/1
            case "minimized":
                return (
                    str,
                    str,
                )
