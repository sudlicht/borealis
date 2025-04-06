from typing import Annotated
from borealis import Borealis
from borealis.widget import Window, Box, IntervalCallback, Label, Orientation
import datetime


def get_hour_min():
    return datetime.datetime.now().strftime("%H:%M:%S")


def get_date():
    return datetime.datetime.now().strftime("%a, %d %B")


# A nice little label that draws the current Hour and Minute
class MyHourMinLabel(Label):
    # We must set a label at the start so the label
    # know's what to display!
    label = get_hour_min()

    # We can use css_classes to put css classes
    # onto our widgets for styling in style.css
    css_classes = ["my-hour-min-label"]

    # Here we see we've defined update_label as an
    # interval (repeating per ms) handler. where we are calling
    # our lambda every 100ms.
    update_label: Annotated[IntervalCallback, 100] = lambda bar: bar.set_label(
        get_hour_min()
    )


# A nice label that draws the current date!
class MyDateLabel(Label):
    label = get_date()

    # We can also use this syntax, with the prefix
    # interval_<ms>
    interval_1000 = lambda label: label.set_label(get_date())


# This is the window of your application, where everything
# will be drawn!
class MyBarWindow(Window):
    # Make sure to read the different class variables you
    # can set!
    child = Box(
        css_classes=["my-box"],
        orientation=Orientation.VERTICAL,
        children=[MyHourMinLabel(), MyDateLabel()],
    )


# This subclass is the root of your application!
# It's what start's your application when you call the
# .run class method.
class MyBar(Borealis):
    # Rename this to the id of your application!
    application_id = "com.example.my_bar"

    # This is where you style your application!
    css_file = "style.css"

    # This is the root of your application, it's what
    # everything will be built off
    #
    #  Note: You are passing the class here! This is because
    #       borealis will initialise the class and set everything up
    #       when it's ready! Do not pass in an initialised class
    root = MyBarWindow


# Dont forget to run your application to see it!
MyBar.run()
