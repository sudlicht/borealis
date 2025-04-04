from borealis import Borealis
from widget.window import Window
from widget.label import Label
from widget.button import Button


def clicked(self: "MyEpicButton", *args, **kwargs):
    print(self.get_child())
    self.b_set_child(Label(label="Bye!", css_name="labelymclabelface"))


class MyEpicButton(Button):
    on_clicked = clicked


class MyLabel(Label):
    label = "Hi!"


class BarWindow(Window):
    child = MyEpicButton(child=MyLabel())
    pass


# Create our borealis application
class MyBar(Borealis):
    application_id = "com.example.my_bar"
    css_file = "style.css"
    # Root window does not need to be initialised (set fields there)
    root = BarWindow
    pass


class BwaTest:
    pass


MyBar.run()
