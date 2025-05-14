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

    def _draw_vertical_separator(self) -> None:
        """
        Draw a vertical separator line.
        """
        draw_list = imgui.get_window_draw_list()
        window_pos = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        separator_min = imgui.ImVec2(window_pos[0], window_pos[1])
        separator_max = imgui.ImVec2(separator_min[0] + 1, separator_min[1] + window_size[1])
        draw_list.add_rect_filled(separator_min, separator_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=0.0, flags=0)

    def draw(self) -> None:
        """
        Draw the outliner panel.
        """ 
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        self._draw_vertical_separator()
        