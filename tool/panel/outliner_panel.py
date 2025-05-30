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
        if node.get_detailed():
            node_details = node.get_detail_nodes()
            for node_detail in node_details:
                if not hasattr(node_detail, "outliner_detail_pencil"):
                    node_detail.outliner_detail_pencil = OutlinerPropertyPencil(node_detail, self._node_index, indent + 1)
                node_detail.outliner_detail_pencil.update_draw()
        if node.get_expanded():
            node_children = node.get_child_nodes()
            if node_children:
                for child in node_children:
                    self._recursive_node_draw(child, indent + 1)
        if node.get_detailed():
            pass
            
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
        bg_max_y = self._draw_y_pos + 22
        if self._node.get_detailed():
            bg_max_y = self._draw_y_pos + 22 + (22 * len(self._node.get_detail_nodes()))
        bg_rect_min = imgui.ImVec2(imgui.get_cursor_pos_x(), self._draw_y_pos) - imgui.ImVec2(0, self._scroll[1])
        bg_rect_max = imgui.ImVec2(bg_max_x, bg_max_y) - imgui.ImVec2(0, self._scroll[1])
        bg_color = (0.1, 0.1, 0.1, 1) if odd_index else (0.12, 0.12, 0.12, 1)
        self._draw_list.add_rect_filled(bg_rect_min, bg_rect_max, imgui.get_color_u32(bg_color), rounding=2.0)

    def _has_lower_sibling(self, node: cbase.Primative) -> bool:
        """
        Check if the node has a lower sibling.
        """
        parent_node = node.get_parent_node()
        if not parent_node:
            return False
        sibling_list = parent_node.get_child_nodes()
        if sibling_list[-1] != node:
            return True
        return False

    def _get_index_parent_node(self, node: cbase.Node, index):
        for parent_index in range(0, index):
            parent = node.get_parent_node()
            node = parent
        return node


    def _calc_navigation(self):
        """
        Draw the navigation of the node.
        """
        self._nav_list = []
        index_node: cbase.Pathed = self._node
        for index, segment in enumerate(range(self._indent - 1, -1, -1)):
            parent_node = index_node.get_parent_node() if index_node else None
            if (segment == self._indent - 1):
                if not self._node.get_child_nodes():
                    nav_icon = cstat.Icon.ICON_NAV_END
                elif self._node.get_expanded() and self._node.get_parent_node():
                    nav_icon = cstat.Icon.ICON_NAV_OPEN
                elif self._node.get_expanded() and not self._node.get_parent_node():
                    nav_icon = cstat.Icon.ICON_NAV_OPEN_NOP
                elif not self._node.get_expanded() and self._node.get_parent_node():
                    nav_icon = cstat.Icon.ICON_NAV_CLOSED_NOS
                else:
                    nav_icon = cstat.Icon.ICON_NAV_CLOSED_NOP_NOS
            else:
                if not parent_node and self._node not in index_node.get_child_nodes():
                    nav_icon = cstat.Icon.ICON_NAV_SPACER               
                elif self._get_index_parent_node(self._node, index - 1).get_has_lower_sibling():
                    if self._node.get_has_lower_sibling() and index < 2:
                        nav_icon = cstat.Icon.ICON_NAV_LINE_T
                    else:
                        nav_icon = cstat.Icon.ICON_NAV_LINE_VERTICAL
                elif self._node in index_node.get_child_nodes():
                    if self._node.get_has_lower_sibling():
                        nav_icon = cstat.Icon.ICON_NAV_LINE_T
                    elif not self._node.get_has_lower_sibling():
                        nav_icon = cstat.Icon.ICON_NAV_LINE_L
                else:
                    nav_icon = cstat.Icon.ICON_NAV_SPACER            
            index_node = index_node.get_parent_node()
            self._nav_list.append(nav_icon)
        self._nav_list.reverse()

    def _recursive_collapse(self, node: cbase.Node):
        node.set_expanded(False)
        node_children = node.get_child_nodes()
        for node_child in node_children:
            node_child.set_expanded(False)
            self._recursive_collapse(node_child)

    def _recursive_expand(self, node: cbase.Node):
        node.set_expanded(True)
        node_children = node.get_child_nodes()
        for node_child in node_children:
            node_child.set_expanded(True)
            self._recursive_expand(node_child)


    def _draw_navigation(self):
        """
        Draw the navigation of the node.
        """
        nav_color = (0.33, 0.33, 0.33, 1)
        for index, nav_segment in enumerate(self._nav_list):
            nav_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, nav_segment, (22, 22))
            imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
            imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
            imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
            imgui.push_style_var(imgui.StyleVar_.frame_padding, (0, 0))
            imgui.same_line()
            imgui.set_cursor_pos_x(self._indent_size_x * index)
            if nav_segment == self._nav_list[-1]:
                if imgui.image_button(f"##nav_{self._node.get_data_object()}", nav_icon_id, image_size=(22, 22), bg_col=(0.0, 0.0, 0.0, 0.0), tint_col=nav_color):
                    key_shift = imgui.get_io().key_shift
                    if self._node.get_expanded():
                        if key_shift:
                            self._recursive_collapse(self._node)                            
                        else:
                            self._node.set_expanded(False)
                    else:
                        if key_shift:
                            self._recursive_expand(self._node)  
                        else:
                            self._node.set_expanded(True)
            else:
                imgui.image_with_bg(nav_icon_id, (22, 22), bg_col=(0.0, 0.0, 0.0, 0.0), tint_col=nav_color)
            imgui.pop_style_color(3)
            imgui.pop_style_var(1)

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
        node_base_color = imgui.ImVec4(0.4, 0.4, 0.4, 1.0) if self._node.get_selected() else imgui.ImVec4(0.25, 0.25, 0.25, 1.0)
        if self._node.get_detailed():
            detail_count = len(self._node.get_detail_nodes())
            detail_rect_max = (node_rect_max[0], node_rect_max[1] + (22 * detail_count) - 1)
            self._draw_list.add_rect_filled(node_rect_min, detail_rect_max, imgui.get_color_u32(node_base_color * 0.75), rounding=2.0)
            self._draw_list.add_rect(node_rect_min, detail_rect_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0)
        self._draw_list.add_rect_filled(node_rect_min, node_rect_max, imgui.get_color_u32(node_base_color), rounding=2.0)
        self._draw_list.add_rect(node_rect_min, node_rect_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0)
        hovered = imgui.is_mouse_hovering_rect(node_rect_min, node_rect_max)
        if hovered:
            if imgui.is_mouse_clicked(imgui.MouseButton_.left):
                if imgui.get_io().key_shift or imgui.get_io().key_ctrl:
                    self._node.set_selected(not self._node.get_selected())
                else:
                    self._node.get_sm().deselect_all()
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
        if self._node.get_detail_nodes():
            self._node: cbase.Primative
            imgui.same_line()
            imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + 10)
            imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
            imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
            imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
            imgui.push_style_var(imgui.StyleVar_.frame_padding, (5, 5))
            icon_arrow = cstat.Icon.ICON_ARROW_DOWN if self._node.get_detailed() else cstat.Icon.ICON_ARROW_LEFT
            icon_arrow_id = cutils.FileHelper.read(cstat.Filetype.ICON, icon_arrow, (12, 12))
            if imgui.image_button(f"##{self._node.get_data_object()}", icon_arrow_id, (12, 12), tint_col=(0, 0, 0, 1)):
                self._node.set_detailed(not self._node.get_detailed())
            imgui.pop_style_color(3)
            imgui.pop_style_var(1)        

        if issubclass(self._node.__class__, cbase.Primative):
            if self._node.get_has_visibility():
                imgui.same_line()
                imgui.set_cursor_pos_x(node_rect_max[0] - 28)
                imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
                imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
                imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
                imgui.push_style_var(imgui.StyleVar_.frame_padding, (3, 3))
                visibility_icon = cstat.Icon.ICON_EYE_ENABLED if self._node.get_visible() else cstat.Icon.ICON_EYE_DISABLED
                visibility_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, visibility_icon, (16, 16))
                if imgui.image_button(f"##visibility_{self._node.get_data_object()}", visibility_icon_id, (16, 16), tint_col=(0,0,0,1)):
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
        self._calc_navigation()
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
        self._indent_size_x = 20

    def _draw_node(self):
        """
        Draw the node icon and name.
        """
        imgui.same_line()
        indent_cursor_pos_x = self._indent * self._indent_size_x
        self._draw_y_pos = imgui.get_cursor_pos_y() + imgui.get_text_line_height_with_spacing() + 3 + 22
        imgui.set_cursor_pos_x(indent_cursor_pos_x + 20)
        remaining_x = imgui.get_content_region_avail()[0] + 15
        text_width = imgui.calc_text_size(self._node.get_name())[0]
        node_width = 180
        if remaining_x < node_width:
            node_width = remaining_x
            if node_width < text_width + 100:
                node_width = text_width + 100
        node_rect_min = imgui.ImVec2(indent_cursor_pos_x + 2, self._draw_y_pos + 2) - self._scroll
        node_rect_max = (node_rect_min[0] + node_width, node_rect_min[1] + 18)
        self._draw_list.add_rect_filled(node_rect_min, node_rect_max, imgui.get_color_u32(self._node_color), rounding=2.0)
        self._draw_list.add_rect(node_rect_min, node_rect_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0)
        internal_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_ROOT, (22, 22))  
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (0, 0))     
        imgui.set_cursor_pos_x(indent_cursor_pos_x)
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        imgui.image_with_bg(internal_icon_id, (22, 22), tint_col=(0, 0, 0, 1))
        imgui.pop_style_var(1)
        imgui.same_line()
        imgui.set_cursor_pos_x(indent_cursor_pos_x + 25)
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 3) 
        imgui.push_style_color(imgui.Col_.text, (0.1, 0.1, 0.1, 1))       
        imgui.text(self._node.get_name())
        imgui.pop_style_color(1)

    def _draw(self):
        """
        Draw the outliner entry.
        """
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (0, 0))  
        self._scroll = imgui.ImVec2(imgui.get_scroll_x(), imgui.get_scroll_y())
        self._draw_node()
        imgui.pop_style_var(1)
        imgui.new_line()

    def set_index(self, index: int) -> None:
        """
        Set the index of the node.
        """
        self._index = index

#####################################################################################################################################



