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
import core.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
#####################################################################################################################################
      
class TrackbarPanel(cbase.Panel):
    """
    Trackbar for scrubbing usd scene time.
    """
    def __init__(self, frame: cbase.Frame):
        super().__init__("trackbar", frame)
    
    def draw(self) -> None:
        """
        Draw the outliner panel.
        """ 
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        imgui.text("Trackbar")