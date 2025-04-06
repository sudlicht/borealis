from borealis import Borealis
from borealis.widget import Window


# This is the window of your application, where everything
# will be drawn!
class MyBarWindow(Window):
    pass


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
