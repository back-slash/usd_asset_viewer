#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Detail
# TODO:
# 
#####################################################################################################################################

# PYTHON
from typing import Any
import os

# ADDONS
from imgui_bundle import imgui

# PROJECT
import core.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
#####################################################################################################################################
      
class DetailPanel(cbase.Panel):
    """
    Detail panel class for display selection details.
    """
    def __init__(self, frame: cbase.Frame):
        super().__init__("detail", frame)

    def draw(self, position: tuple[int, int]) -> None:
        """
        Draw the outliner panel.
        """ 
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(position)
        imgui.begin(self._name, True, self._window_flags)