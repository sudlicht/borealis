from typing import Annotated
from borealis import Borealis
from widget.annotate import IntervalCallback
from widget.window import Window
from widget.label import Label
import datetime


def get_time():
    return str(datetime.datetime.now().strftime("%H:%M:%S - %d/%m/%Y"))


def update_time_label(mylabel: "MyTimeLabel"):
    mylabel.set_label(get_time())


class MyTimeLabel(Label):
    label = get_time()
    css_classes = ["my-label-css"]
    update_time: Annotated[IntervalCallback, 100] = update_time_label


class BarWindow(Window):
    child = MyTimeLabel()


class MyBar(Borealis):
    application_id = "com.example.my_bar"
    css_file = "style.css"
    root = BarWindow
    pass


MyBar.run()
