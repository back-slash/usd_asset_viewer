#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Trackbar
# TODO:
# -
#####################################################################################################################################

# PYTHON
from typing import Any

# ADDONS
from imgui_bundle import imgui

# PROJECT
import core.static.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
#####################################################################################################################################
      
class TrackbarPanel(cbase.Panel):
    """
    Trackbar for scrubbing usd scene time.
    """
    def __init__(self, frame: cbase.Frame):
        super().__init__("Trackbar", frame)