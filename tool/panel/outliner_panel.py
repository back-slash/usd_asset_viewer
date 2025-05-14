#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Outliner
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
      
class OutlinerPanel(cbase.Panel):
    """
    Outliner panel for displaying usd contents.
    """
    def __init__(self, frame: cbase.Frame):
        super().__init__("outliner", frame)

    def _draw_vertical_separator(self) -> None:
        """
        Draw a vertical separator line.
        """
        draw_list = imgui.get_window_draw_list()
        window_pos = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        separator_min = imgui.ImVec2(window_pos[0] + window_size[0] - 1, window_pos[1])
        separator_max = imgui.ImVec2(separator_min[0] + 1, separator_min[1] + window_size[1])
        draw_list.add_rect_filled(separator_min, separator_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=0.0, flags=0)

    def _draw_tab_bar(self) -> None:
        """
        Draw the tab bar for the outliner panel.
        """
        imgui.push_style_var(imgui.StyleVar_.tab_border_size, 1.0)
        imgui.push_style_var(imgui.StyleVar_.tab_bar_border_size, 1.0)
        imgui.push_style_var(imgui.StyleVar_.tab_rounding, 0.0)
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (10, 5))
        imgui.push_style_var(imgui.StyleVar_.item_inner_spacing, (1, 1))

        imgui.push_style_color(imgui.Col_.tab, (0.2, 0.2, 0.2, 1))
        imgui.push_style_color(imgui.Col_.tab_selected, (0.3, 0.3, 0.3, 1))
        imgui.push_style_color(imgui.Col_.tab_hovered, (0.35, 0.35, 0.35, 1))
        
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        imgui.begin_tab_bar("##outliner_tab_bar")
        selected, clicked = imgui.begin_tab_item("Standard")
        if selected:
            self._draw_base_tab()
            imgui.end_tab_item()
        selected, clicked = imgui.begin_tab_item("Skeleton")
        if selected:
            self._draw_base_tab()
            imgui.end_tab_item()
        selected, clicked = imgui.begin_tab_item("Material")
        if selected:
            self._draw_base_tab()
            imgui.end_tab_item()
        imgui.end_tab_bar()
        tab_rect = imgui.get_item_rect_max()
        tab_line_min = imgui.ImVec2(0, tab_rect[1] - 1)
        tab_line_max = imgui.ImVec2(tab_line_min[0] + imgui.get_window_width(), tab_line_min[1] + 1)
        draw_list = imgui.get_window_draw_list()
        draw_list.add_rect_filled(tab_line_min, tab_line_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=0.0, flags=0)

        imgui.pop_style_var(5)
        imgui.pop_style_color(3)

    def _draw_base_tab(self) -> None:
        """
        Draw the standard tab of the outliner panel.
        """
        draw_list = imgui.get_window_draw_list()
        cursor_pos = imgui.get_cursor_pos()
        window_pos = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        bg_rect_min = imgui.ImVec2(window_pos[0], window_pos[1] + cursor_pos[1] - 5)
        bg_rect_max = imgui.ImVec2(window_size[0], window_size[1]) + window_pos
        draw_list.add_rect_filled(bg_rect_min, bg_rect_max, imgui.get_color_u32((0.15, 0.15, 0.15, 1)), rounding=0.0, flags=0)


    def draw(self) -> None:
        """
        Draw the outliner panel.
        """ 
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        self._draw_tab_bar()
        self._draw_vertical_separator()    

    


#####################################################################################################################################

class OutlinerEntryPencil(cbase.Pencil):
    """
    Pencil class drawing entries in the outliner.
    """
    _index = 0
    _indent = 0
    _opacity = None
    def __init__(self, node: cbase.Node, index: int=0, indent: int=0):
        super().__init__(node)
        self._index = index
        self._indent = indent

    def _init_node_data(self) -> None:
        return super()._init_node_data()

    def _draw_opacity(self):
        """
        Draw the opacity slider of the node.
        """
        imgui.set_next_item_width(200)
        slider_flags = imgui.SliderFlags_.always_clamp
        imgui.slider_float("Opacity", self._opacity, 0.0, 1.0, "%.2", slider_flags)

    def _calculate_background_rect(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Calculate the background rectangle for the node.
        """
        window_position = imgui.get_window_pos()
        content_region_avail = imgui.get_content_region_avail()
        height = cstat.LINE_HEIGHT
        rect_min = (self._position[0] + window_position[0], self._position[1] + window_position[1])
        rect_max = (rect_min[0] + content_region_avail[0], rect_min[1] + height)
        return rect_min, rect_max

    def _draw_background(self):
        """
        Draw the background of the node.
        """
        imgui.set_cursor_pos(self._position)
        rect_min, rect_max = self._calculate_background_rect()
        draw_list = imgui.get_window_draw_list()
        input_color = cstat.LINE_COLOR if self._index % 2 == 0 else cstat.LINE_COLOR_ALTERNATE
        color = imgui.get_color_u32(input_color)
        rounding = cstat.LINE_ROUNDING
        draw_list.add_rect_filled(rect_min, rect_max, color, rounding, flags=0)

    def _draw_navigation(self):
        """
        Draw the navigation of the node.
        """
        for entry in range(self._indent):
            pass

    def _draw_node(self):
        """
        Draw the node icon and name.
        """
        imgui.set_cursor_pos(self._position)
        imgui.text(self._node_name)
        if self._node_icon:
            imgui.image(self._node_icon, size=(16, 16), uv_min=(0, 0), uv_max=(1, 1))

    def _draw(self):
        """
        Draw the outliner entry.
        """
        self._draw_background(self._position, self._index)
        if self._opacity:
            self._draw_opacity()
        self._draw_navigation()
        self._draw_node()


class OutlinerPropertyPencil(cbase.Pencil):
    """
    Class representing a node in the outliner.
    """
    _index = 0
    _indent = 0
    _opacity = None
    def __init__(self, node: cbase.Node, index: int=0, indent: int=0):
        super().__init__(node)
        self._index = index
        self._indent = indent

    def _draw_navigation(self):
        """
        Draw the navigation of the node.
        """
        for entry in range(self._indent):
            pass

    def _draw_node(self):
        """
        Draw the node icon and name.
        """
        imgui.set_cursor_pos(self._position)
        imgui.text(self._node_name)
        if self._node_icon:
            imgui.image(self._node_icon, size=(16, 16), uv0=(0, 0), uv1=(1, 1))

    def _draw(self):
        """
        Draw the outliner entry.
        """
        self._draw_navigation()
        self._draw_node()






#####################################################################################################################################



