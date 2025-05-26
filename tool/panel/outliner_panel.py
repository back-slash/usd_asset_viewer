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

#####################################################################################################################################      
class OutlinerPanel(cbase.Panel):
    """
    Outliner panel for displaying usd contents.
    """
    def __init__(self, frame: cbase.Frame):
        super().__init__("outliner", frame)
        self._node_index = 0

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

    def _draw_skeleton_tab(self) -> None:
        """
        Draw the skeleton tab.
        """
        if self._stage:
            pass

    def _draw_material_tab(self) -> None:
        """
        Draw the material tab.
        """
        if self._stage:
            pass
    def _draw_standard_tab(self) -> None:
        if not self._stage:
            return
        root_prim = self._sm.get_root()
        root_node = self._sm.get_path_node(root_prim)
        if root_node:
            self._recursive_node_draw(root_node, 1)

    def _recursive_node_draw(self, node: cbase.Primative, indent: int) -> None:
        """
        Recursively traverse the USD stage and draw the nodes.
        """
        self._node_index += 1
        if not hasattr(node, "outliner_pencil"):
            node.outliner_pencil = OutlinerEntryPencil(node, indent)
        node.outliner_pencil.set_index(self._node_index)
        node.outliner_pencil.update_draw()
        if node.get_expanded():
            node_children = node.get_child_nodes()
            if node_children:
                for child in node_children:
                    self._recursive_node_draw(child, indent + 1)
            
    def draw(self) -> None:
        """
        Draw the outliner panel.
        """ 
        self._node_index = 0
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        tab_dict = {
            "standard" : self._draw_standard_tab,
            "skeleton" : self._draw_skeleton_tab,
            "material" : self._draw_material_tab,
        }
        cutils.draw_tab_bar("outliner", tab_dict)
        self._draw_vertical_separator()
  
#####################################################################################################################################

class OutlinerEntryPencil(cbase.NodePencil):
    """
    Pencil class drawing entries in the outliner.
    """
    
    def __init__(self, node: cbase.Node, indent: int=0):
        super().__init__(node)
        self._index = 0
        self._indent = indent
        self._indent_size_x = 20

    def _init_node_data(self) -> None:
        return super()._init_node_data()

    def _draw_visibility(self):
        """
        Draw the visbility switch of the node.
        """
        
    def _draw_background(self):
        """
        Draw the background of the outliner entry.
        """
        odd_index = self._index % 2 == 0
        imgui.set_cursor_pos_x(0)
        bg_max_x = imgui.get_content_region_avail()[0] - 2
        self._draw_y_pos = imgui.get_cursor_pos_y() + imgui.get_text_line_height_with_spacing() + 15
        bg_rect_min = imgui.ImVec2(imgui.get_cursor_pos_x(), self._draw_y_pos) - imgui.ImVec2(0, self._scroll[1])
        bg_rect_max = imgui.ImVec2(bg_max_x, self._draw_y_pos + 22) - imgui.ImVec2(0, self._scroll[1])
        bg_color = (0.1, 0.1, 0.1, 1) if odd_index else (0.12, 0.12, 0.12, 1)
        self._draw_list.add_rect_filled(bg_rect_min, bg_rect_max, imgui.get_color_u32(bg_color), rounding=2.0)

    def _draw_navigation(self):
        """
        Draw the navigation of the node.
        """
        nav_color = (0.33, 0.33, 0.33, 1)
        for segment in range(0, self._indent):
            if segment == self._indent - 1:
                if not hasattr(self._node, "get_child_nodes") or not self._node.get_child_nodes():
                    nav_color = (0.0, 0.0, 0.0, 0.0)
                if self._node.get_expanded() and self._node.get_parent_node():
                    nav_icon = cstat.Icon.ICON_NAV_OPEN
                elif self._node.get_expanded() and not self._node.get_parent_node():
                    nav_icon = cstat.Icon.ICON_NAV_OPEN_NOP
                elif not self._node.get_expanded() and self._node.get_parent_node():
                    nav_icon = cstat.Icon.ICON_NAV_CLOSED_NOS            
                else:
                    nav_icon = cstat.Icon.ICON_NAV_CLOSED_NOP_NOS
                nav_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, nav_icon, (22, 22))
                imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
                imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
                imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
                imgui.push_style_var(imgui.StyleVar_.frame_padding, (0, 0))
                imgui.same_line()
                imgui.set_cursor_pos_x(self._indent_size_x * segment)
                if imgui.image_button(f"##nav_{self._node.get_data_object()}", nav_icon_id, image_size=(22, 22), bg_col=(0.0, 0.0, 0.0, 0.0), tint_col=nav_color):
                    if self._node.get_expanded():
                        self._node.set_expanded(False)
                    else:
                        self._node.set_expanded(True)
                imgui.pop_style_color(3)
                imgui.pop_style_var(1)
            elif segment < self._indent - 2:
                pass

    def deselect_all(self):
        """
        Deselect all nodes in the outliner.
        """
        for path_node in self._node.get_sm().get_path_node_list():
            path_node.set_selected(False)
        for data_node in self._node.get_sm().get_data_node_list():
            data_node.set_selected(False)

    def _draw_node(self):
        """
        Draw the node icon, name and selectable.
        """       
        imgui.same_line()
        indent_cursor_pos_x = self._indent * self._indent_size_x 
        imgui.set_cursor_pos_x(indent_cursor_pos_x + 25)
        remaining_x = imgui.get_content_region_avail()[0] + 15
        text_width = imgui.calc_text_size(self._node.get_name())[0]
        node_width = 225
        if remaining_x < node_width:
            node_width = remaining_x
            if node_width < text_width + 100:
                node_width = text_width + 100
        node_rect_min = imgui.ImVec2(indent_cursor_pos_x + 2, self._draw_y_pos + 1) - self._scroll
        node_rect_max = (node_rect_min[0] + node_width, node_rect_min[1] + 20)
        node_base_color = (0.35, 0.35, 0.35, 1.0) if self._node.get_selected() else (0.25, 0.25, 0.25, 1.0)
        self._draw_list.add_rect_filled(node_rect_min, node_rect_max, imgui.get_color_u32(node_base_color), rounding=2.0)
        self._draw_list.add_rect(node_rect_min, node_rect_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0)
        hovered = imgui.is_mouse_hovering_rect(node_rect_min, node_rect_max)
        if hovered:
            if imgui.is_mouse_clicked(imgui.MouseButton_.left):
                if imgui.get_io().key_shift or imgui.get_io().key_ctrl:
                    self._node.set_selected(not self._node.get_selected())
                else:
                    self.deselect_all()
                    self._node.set_selected(True)
        icon_bg_min = node_rect_min
        icon_bg_max = (node_rect_min[0] + 20, node_rect_min[1] + 20)
        node_color = imgui.ImVec4(self._node_color) * 1.5 if self._node.get_selected() else self._node_color
        self._draw_list.add_rect_filled(icon_bg_min, icon_bg_max, imgui.get_color_u32(node_color), rounding=2.0)
        self._draw_list.add_rect(icon_bg_min, icon_bg_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0)
        internal_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, self._node_icon, (20, 20))
        icon_min = (icon_bg_min[0], icon_bg_min[1])
        icon_max = (icon_min[0] + 20, icon_min[1] + 20)
        self._draw_list.add_image(internal_icon_id, icon_min, icon_max, col=imgui.get_color_u32((0, 0, 0, 1)))
        imgui.push_style_color(imgui.Col_.text, (0.66, 0.66, 0.66, 1))
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 4)
        imgui.text(self._node.get_name())
        imgui.pop_style_color(1)
        if issubclass(self._node.__class__, cbase.Primative):
            self._node: cbase.Primative
            imgui.same_line()
            imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + 10)
            imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
            imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
            imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
            imgui.push_style_var(imgui.StyleVar_.frame_padding, (0, 0))
            if not self._node.get_expanded():
                if imgui.button(f"◀##{self._node.get_data_object()}", size=(22, 22)):
                    self._node.set_expanded(False)
            else:
                if imgui.button(f"▼##{self._node.get_data_object()}", size=(22, 22)):
                    pass
            imgui.pop_style_color(3)
            imgui.pop_style_var(1)
            if self._node.has_visibility():
                imgui.same_line()
                imgui.set_cursor_pos_x(node_rect_max[0] - 28)
                imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
                imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
                imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
                imgui.push_style_var(imgui.StyleVar_.frame_padding, (3, 3))
                visibility_icon = cstat.Icon.ICON_EYE_ENABLED if self._node.get_visible() else cstat.Icon.ICON_EYE_DISABLED
                visibility_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, visibility_icon, (16, 16))
                if imgui.image_button(f"##visibility_{self._node.get_data_object()}", visibility_icon_id, image_size=(16, 16), tint_col=(0,0,0,1)):
                    self._node.set_visibility(not self._node.get_visible())
                imgui.pop_style_color(3)
                imgui.pop_style_var(1)

    def _draw(self):
        """
        Draw the outliner entry.
        """
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (0, 0))  
        self._scroll = imgui.ImVec2(imgui.get_scroll_x(), imgui.get_scroll_y())
        self._draw_background()
        self._draw_visibility()
        self._draw_navigation()
        self._draw_node()
        imgui.pop_style_var(1)
        imgui.new_line()

    def set_index(self, index: int) -> None:
        """
        Set the index of the node.
        """
        self._index = index

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



