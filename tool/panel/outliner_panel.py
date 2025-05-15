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
import pxr.Usd as pusd
import pxr.UsdGeom as pgeo
import pxr.UsdShade as pshd


# PROJECT
import core.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
#####################################################################################################################################
      
class OutlinerPanel(cbase.Panel):
    """
    Outliner panel for displaying usd contents.
    """
    _internal_test_node_dict = {}
    _internal_test_icon_dict = {}
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
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (5, 0))

        imgui.push_style_color(imgui.Col_.tab, (0.2, 0.2, 0.2, 1))
        imgui.push_style_color(imgui.Col_.tab_selected, (0.3, 0.3, 0.3, 1))
        imgui.push_style_color(imgui.Col_.tab_hovered, (0.35, 0.35, 0.35, 1))
        
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        imgui.begin_tab_bar("##outliner_tab_bar")
        selected, clicked = imgui.begin_tab_item("Standard")
        if selected:
            self._draw_base_tab()
            imgui.set_cursor_pos_y(imgui.get_cursor_pos_y())
            if imgui.begin_child("##outliner_standard", (0, 0)):
                imgui.new_line()
                imgui.set_cursor_pos_y(imgui.get_cursor_pos_y())
                self._draw_standard_tab()
                imgui.end_child()
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
        imgui.pop_style_var(6)
        imgui.pop_style_color(3)

    def _draw_base_tab(self) -> None:
        """
        Draw the standard tab of the outliner panel.
        """
        draw_list = imgui.get_window_draw_list()
        cursor_pos = imgui.get_cursor_pos()
        window_pos = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        bg_rect_min = imgui.ImVec2(window_pos[0], window_pos[1] + cursor_pos[1])
        bg_rect_max = imgui.ImVec2(window_size[0], window_size[1]) + window_pos
        draw_list.add_rect_filled(bg_rect_min, bg_rect_max, imgui.get_color_u32((0.15, 0.15, 0.15, 1)), rounding=0.0, flags=0)

    def _draw_standard_tab(self) -> None:
        if self._stage:
            root = self._scene_manager.get_root()
            self._node_index = 0
            self._recursive_node_draw(root, 0)
                
    def _recursive_node_draw(self, node: pusd.Prim, indent: int) -> None:
        """
        Recursively traverse the USD stage and draw the nodes.
        """
        if node.IsValid():
            self._draw_test_node(node, indent)
            node_children = node.GetChildren()
            if node_children:
                for child in node_children:
                    self._recursive_node_draw(child, indent + 1)
            
    def _draw_test_node(self, node: pusd.Prim, indent: int) -> None:
        """
        Draw a test node in the outliner.
        """
        if node not in self._internal_test_node_dict:
            self._internal_test_node_dict[node] = self._scene_manager.init_path_node(node)
        internal_node: cbase.Pathed = self._internal_test_node_dict[node]
        if not internal_node:
            return
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 22 + 10)
        indent_size_x = 20
        odd_index = self._node_index % 2 == 0
        draw_list = imgui.get_window_draw_list()
        node_name = node.GetName()
        node_type = node.GetTypeName()
        indent_cursor_pos_x = indent * indent_size_x
        imgui.set_cursor_pos_x(0)
        bg_max_x = imgui.get_content_region_avail()[0] - 2
        bg_rect_min = imgui.ImVec2(imgui.get_cursor_pos_x(), imgui.get_cursor_pos_y())
        bg_rect_max = imgui.ImVec2(bg_max_x, bg_rect_min[1] + 22)
        bg_color = (0.1, 0.1, 0.1, 1) if odd_index else (0.12, 0.12, 0.12, 1)
        draw_list.add_rect_filled(bg_rect_min, bg_rect_max, imgui.get_color_u32(bg_color), rounding=2.0)
        
        node_rect_min = (indent_cursor_pos_x + 2, imgui.get_cursor_pos_y() + 1)
        node_rect_max = (node_rect_min[0] +  250, node_rect_min[1] + 20)
        node_base_color = (0.25, 0.25, 0.25, 1)
        draw_list.add_rect_filled(node_rect_min, node_rect_max, imgui.get_color_u32(node_base_color), rounding=2.0)
        draw_list.add_rect(node_rect_min, node_rect_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0)
        icon_bg_min = node_rect_min
        icon_bg_max = (node_rect_min[0] + 20, node_rect_min[1] + 20)
        internal_color = internal_node.get_color()
        internal_icon = internal_node.get_icon()
        draw_list.add_rect_filled(icon_bg_min, icon_bg_max, imgui.get_color_u32(internal_color), rounding=2.0)
        draw_list.add_rect(icon_bg_min, icon_bg_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0)
        if internal_icon not in self._internal_test_icon_dict:
            self._internal_test_icon_dict[internal_icon] = cutils.FileHelper.read(cstat.Filetype.ICON, internal_icon, (20, 20))
        internal_icon_id = self._internal_test_icon_dict[internal_icon]
        icon_min = (icon_bg_min[0], icon_bg_min[1])
        icon_max = (icon_min[0] + 20, icon_min[1] + 20)
        draw_list.add_image(internal_icon_id, icon_min, icon_max, col=imgui.get_color_u32((0, 0, 0, 1)))
        imgui.push_style_color(imgui.Col_.text, (0.66, 0.66, 0.66, 1))
        imgui.same_line()
        imgui.set_cursor_pos_x(indent_cursor_pos_x + 25)
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 10)
        imgui.text(node_name)
        imgui.get_text_line_height()
        imgui.set_cursor_pos_x(0)
        
        imgui.pop_style_color(1)
        imgui.new_line()
        self._node_index += 1

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

class OutlinerEntryPencil(cbase.NodePencil):
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


class OutlinerPropertyPencil(cbase.NodePencil):
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



