#####################################################################################################################################
# USD Outliner | Tool | Main
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON
from typing import Any

# ADDONS
from imgui_bundle import imgui
import glfw
import OpenGL.GL as gl
import pxr.Usd as pusd

# PROJECT
import core.static.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
#####################################################################################################################################
      


class OutlinerEntryPencil(cbase.Pencil):
    """
    Class representing a node in the outliner.
    """
    _opacity = None
    def __init__(self, node: cbase.Node, position: tuple[int, int]=None, size: tuple[int, int]=None, index: int=0):
        super().__init__(node, position, size)
        self._index = index

    def _draw_opacity(self, opacity):
        """
        Draw the opacity slider of the node.
        """
        imgui.set_next_item_width(200)
        slider_flags = imgui.SliderFlags_.always_clamp
        imgui.slider_float("Opacity", opacity, 0.0, 1.0, "%.2", slider_flags)

    def _calculate_background_rect(self, position) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Calculate the background rectangle for the node.
        """
        window_position = imgui.get_window_pos()
        content_region_avail = imgui.get_content_region_avail()
        height = cstat.LINE_HEIGHT
        rect_min = (position[0] + window_position[0], position[1] + window_position[1])
        rect_max = (rect_min[0] + content_region_avail[0], rect_min[1] + height)
        return rect_min, rect_max

    def _draw_background(self, position: tuple[int, int], index: int):
        """
        Draw the background of the node.
        """
        imgui.set_cursor_pos(position)
        rect_min, rect_max = self._calculate_background_rect()
        draw_list = imgui.get_window_draw_list()
        input_color = cstat.LINE_COLOR if index % 2 == 0 else cstat.LINE_COLOR_ALTERNATE
        color = imgui.get_color_u32(input_color)
        rounding = cstat.LINE_ROUNDING
        draw_list.add_rect_filled(rect_min, rect_max, color, rounding, flags=0)

    def _draw_node(self):
        """
        Draw the node icon and name.
        """

    def _draw_navigation(self, indent: int):
        """
        Draw the navigation of the node.
        """

    def _draw(self, position: tuple[int, int], size: tuple[int, int]):
        """
        Draw the outliner entry.
        """
        self._draw_background(position, self._index)
        if self._opacity:
            self._draw_opacity(self._opacity)
        self._draw_navigation()
        self._draw_node()
        






#####################################################################################################################################


class USDOutliner(cbase.Frame):
    """
    USD Outliner class for managing and displaying a list of items in a prototype window.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        usd_path = cstat.DEFAULT_USD_PATH
        self._scene_manger = cbase.SceneManager(usd_path)
        self._stage = self._scene_manger.get_stage()


    def _clear_usd_file(self):
        """
        Clear the USD Stage.
        """
        if self._stage:
            self._stage = None




#####################################################################################################################################

class OutlinerPanel(cbase.Panel):
    """
    Outliner class for managing and displaying a list of items in a prototype window.
    """









