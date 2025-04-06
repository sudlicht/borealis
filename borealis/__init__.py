"""
borealis

Gtk4 wrapper and helper for building applications
notably using layer-shell
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

from .ext import *
from .service import *
from .widget import *

# Root borealis instance.
from .borealis import Borealis
