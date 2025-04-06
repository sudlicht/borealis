from typing import Annotated
from borealis import Borealis
from widget.annotate import IntervalCallback, OneshotCallback, SignalCallback
from widget.box import Box
from widget.button import Button
from widget.centerbox import CenterBox
from widget.enums import Orientation
from widget.separator import Separator
from widget.window import Window
from widget.label import Label
import datetime
import subprocess
import json


def get_hour_min():
    return datetime.datetime.now().strftime("%H:%M")


def get_date():
    return datetime.datetime.now().strftime("%a, %d %B")


def workspace_sender(this_button: "MyWorkspaceButton", *args, **kwargs):
    subprocess.run(
        ["hyprctl", "dispatch", "workspace", str(this_button.get_parent().workspace)]
    )


def set_workspace_label(this_button: "MyWorkspaceButton", *args, **kwargs):
    button_label: Label = this_button.get_child()

    button_label.set_label(str(this_button.get_parent().workspace % 10))


class MyWorkspaceButton(Button):
    css_classes = ["workspace-button"]
    child = Label(label="N/A")
    set_workspace: Annotated[OneshotCallback, 0] = set_workspace_label
    jump_workspace: Annotated[SignalCallback, "clicked"] = workspace_sender


class MyWorkspaceElement(CenterBox):
    css_classes = ["workspace-box"]
    orientation = Orientation.VERTICAL
    center = MyWorkspaceButton()
    end = Separator(css_classes=["workspace-indicator"])


class MyWorkspacesWidget(Box):
    children = [
        MyWorkspaceElement(workspace=1),
        MyWorkspaceElement(workspace=2),
        MyWorkspaceElement(workspace=3),
        MyWorkspaceElement(workspace=4),
        MyWorkspaceElement(workspace=5),
        MyWorkspaceElement(workspace=6),
        MyWorkspaceElement(workspace=7),
        MyWorkspaceElement(workspace=8),
        MyWorkspaceElement(workspace=9),
        MyWorkspaceElement(workspace=10),
    ]


class MyHourMinLabel(Label):
    css_classes = ["hour-label"]
    label = get_hour_min()
    update_label: Annotated[IntervalCallback, 100] = lambda bar: bar.set_label(
        get_hour_min()
    )


class MyDateLabel(Label):
    css_classes = ["date-label"]
    label = get_date()
    update_label: Annotated[IntervalCallback, 100] = lambda bar: bar.set_label(
        get_date()
    )


class MyTimeWidget(CenterBox):
    css_classes = ["time-widget"]
    orientation = Orientation.VERTICAL
    center = Box(
        orientation=Orientation.VERTICAL, children=[MyHourMinLabel(), MyDateLabel()]
    )


class BarWindow(Window):
    css_classes = ["root"]
    child = Box(
        children=[MyWorkspacesWidget(), Separator(css_classes=["sep"]), MyTimeWidget()]
    )
    pass


class MyBar(Borealis):
    application_id = "com.example.my_bar"
    css_file = "style.css"
    root = BarWindow
    pass


MyBar.run()
