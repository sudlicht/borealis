import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

from typing import Annotated
from borealis import Borealis
from borealis_logging import BorealisFormatter
from ext.hyprland import HyprlandCallback, HyprlandService
from widget.annotate import IntervalCallback, SignalCallback
from widget.box import Box
from widget.button import Button
from widget.centerbox import CenterBox
from widget.label import Label
from widget.window import Window

import logging
import json

import gc


def test_disconnect(button: "DisconnectButtonTest", *args, **kwargs):
    print(f"clicked! {button}")
    window: "CenterBox" = button.get_parent()
    window.b_set_center_widget(DisconnectButtonTest())
    window.b_set_end_widget(DisconnectButtonTest())


def hi(self, *args, **kwargs):
    print("bwubuwubwu")
    self.get_child().set_label("Clickbkbe")


def changed_workspace_hyprland(self, *args):
    print(args, self)


class DisconnectButtonTest(Button):
    child = Label(label="Click me!")
    disconnect_tester: Annotated[SignalCallback, "clicked"] = test_disconnect
    test_interval: Annotated[IntervalCallback, 1000] = hi
    changed_workspace: Annotated[HyprlandCallback, "workspacev2"] = (
        changed_workspace_hyprland
    )


class TestWindow(Window):
    css_classes = ["root"]
    child = Box(children=[CenterBox(center=DisconnectButtonTest())])
    pass


class MyBar(Borealis):
    application_id = "com.example.my_bar"
    root = TestWindow
    services = [HyprlandService()]
    pass


MyBar.run()
