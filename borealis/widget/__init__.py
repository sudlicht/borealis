"""
borealis.widget

Contains higher level abstractions over Gtk4's widget's
which are used to build applications using borealis
"""

# Abstracted widgets, prefer b_<method>
from .box import Box
from .button import Button
from .centerbox import CenterBox
from .label import Label
from .separator import Separator
from .window import Window

# Base borealis widget class
from .widget import Widget

# Annotations, used for registering signals/oneshots/intervals etc.
from .annotate import *

# Misc
from .enums import *
from .layer_shell import *
