#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Trackbar
# TODO:
# -
#####################################################################################################################################

# PYTHON
from typing import Any

# ADDONS
from imgui_bundle import imgui
from pxr import Usd as pusd
from pxr import UsdSkel as pskl

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
        self._init_time()

    def _init_time(self) -> None:
        """
        Initialize time.
        """
        self._start_time, self._end_time = self._scene_manager.get_time_range()

    def _draw_horizonal_line(self) -> None:
        window_pos = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        vertical_line_min  = imgui.ImVec2(window_pos[0], window_pos[1])
        vertical_line_max  = imgui.ImVec2(window_size[0], window_pos[1])
        self._draw_list.add_line(vertical_line_min, vertical_line_max, imgui.get_color_u32((0, 0, 0, 1)), thickness=1.0)

    def _draw_trackbar(self) -> None:
        """
        Draw the trackbar.
        """
        imgui.push_style_color(imgui.Col_.slider_grab, imgui.get_color_u32((0.15, 0.15, 0.15, 1)))
        imgui.push_style_color(imgui.Col_.slider_grab_active, imgui.get_color_u32((0.25, 0.25, 0.25, 1)))
        imgui.push_style_color(imgui.Col_.frame_bg, imgui.get_color_u32((0, 0, 0, 0)))
        imgui.push_style_color(imgui.Col_.frame_bg_active, imgui.get_color_u32((0, 0, 0, 0)))
        imgui.push_style_color(imgui.Col_.frame_bg_hovered, imgui.get_color_u32((0, 0, 0, 0)))

        imgui.push_style_var(imgui.StyleVar_.grab_rounding, 3.0)

        track_bg_width = self._cfg['detail']['width']
        window_pos = imgui.get_window_pos()
        trackbar_bg_min = imgui.get_cursor_pos() + window_pos + imgui.ImVec2(5, 5)
        trackbar_bg_max = imgui.get_content_region_avail() + window_pos - imgui.ImVec2(track_bg_width, 5)
        self._draw_list.add_rect_filled(trackbar_bg_min, trackbar_bg_max, imgui.get_color_u32((0.3, 0.3, 0.3, 1)), rounding=5.0, flags=0)
        self._draw_list.add_rect(trackbar_bg_min, trackbar_bg_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=5.0, flags=0)
        imgui.push_item_width((trackbar_bg_max - trackbar_bg_min)[0] - 10)
        imgui.set_cursor_pos((imgui.get_cursor_pos_x() + 10, imgui.get_cursor_pos_y() + 10))
        changed, value = imgui.slider_int("##trackbar", int(self._scene_manager.get_current_time()), int(self._start_time), int(self._end_time))
        if changed:
            self._scene_manager.set_current_time(value)
            for node in self._scene_manager.get_path_node_list():
                if isinstance(node, cbase.Skeleton):
                    node.update_animation()
        imgui.pop_item_width()
        imgui.pop_style_color(5)
        imgui.pop_style_var(1)

    def draw(self) -> None:
        """
        Draw the outliner panel.
        """
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        self._draw_list = imgui.get_window_draw_list()
        self._draw_trackbar()
        self._draw_horizonal_line()

    def update_usd(self):
        super().update_usd()
        self._init_time()

        