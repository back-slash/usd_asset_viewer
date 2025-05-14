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
        window_pos = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        draw_list = imgui.get_window_draw_list()
        vertical_line_min  = imgui.ImVec2(window_pos[0], window_pos[1])
        vertical_line_max  = imgui.ImVec2(window_size[0], window_pos[1])
        draw_list.add_line(vertical_line_min, vertical_line_max, imgui.get_color_u32((0, 0, 0, 1)), thickness=1.0)
        trackbar_bg_min = imgui.get_cursor_pos() + window_pos + imgui.ImVec2(5, 5)
        track_bg_width = self._cfg['detail']['width']
        trackbar_bg_max = imgui.get_content_region_avail() + window_pos - imgui.ImVec2(track_bg_width, 5)
        draw_list.add_rect_filled(trackbar_bg_min, trackbar_bg_max, imgui.get_color_u32((0.3, 0.3, 0.3, 1)), rounding=5.0, flags=0)
        draw_list.add_rect(trackbar_bg_min, trackbar_bg_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=5.0, flags=0)