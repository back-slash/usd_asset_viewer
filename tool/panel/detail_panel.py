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
import pxr.Usd as pusd
import pxr.UsdGeom as pgeo
import pxr.UsdLux as plux
import pxr.Gf as pgf

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

    def _draw_detail_tab(self) -> None:
        """
        Draw the detail tab.
        """
        if self._stage:
            pass

    def _draw_scene_tab(self) -> None:
        """
        Draw the scene tab.
        """
        imgui.set_cursor_pos_x(10)
        width = imgui.get_content_region_avail()[0] - 10
        cutils.draw_generic_sub_window("Light Settings:", (width, 0), self._draw_scene_settings)

    def _draw_scene_settings(self) -> None:
        """
        Draw the scene settings.
        """
        for light_name in self._sm.create_light_dict():
            light: cbase.Light = self._sm.create_light_dict()[light_name]["node"]
            if not hasattr(light, "light_adjustment_pencil"):
                light.light_adjustment_pencil = LightAdjustmentPencil(light)
            light.light_adjustment_pencil.update_draw()
         
    def draw(self) -> None:
        """
        Draw the outliner panel.
        """ 
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        detail_tab_dict = {
            "detail": self._draw_detail_tab,
            "scene": self._draw_scene_tab,
        }
        cutils.draw_tab_bar("detail", detail_tab_dict)
        self._draw_vertical_separator()

    def update_usd(self):
        super().update_usd()


class LightAdjustmentPencil(cbase.NodePencil):
    """
    Pencil class for creating a light adjustment widget.
    """
    def __init__(self, node: cbase.Light):
        super().__init__(node)
        self._node: cbase.Light
        self._api_object = plux.LightAPI(node.get_prim())

    def _internal_draw(self):
        if not self._node.get_prim().IsValid():
            return
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (5, 5))
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 1.0)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 2.0)
        
        imgui.push_style_color(imgui.Col_.frame_bg, (0.175, 0.175, 0.175, 1))
        imgui.push_style_color(imgui.Col_.frame_bg_active, (0.175, 0.175, 0.175, 1))
        imgui.push_style_color(imgui.Col_.frame_bg_hovered, (0.175, 0.175, 0.175, 1))
        imgui.push_style_color(imgui.Col_.slider_grab, (0.1, 0.1, 0.1, 1))

        start_cursor_pos = imgui.get_cursor_pos()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 10)
        imgui.text(self._node.get_name())
        imgui.same_line()
        imgui.set_cursor_pos_x(start_cursor_pos[0] + 75)
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - (imgui.get_text_line_height()  * 0.5))
        color_edit_flags = imgui.ColorEditFlags_.no_alpha | imgui.ColorEditFlags_.no_label | imgui.ColorEditFlags_.picker_hue_bar | imgui.ColorEditFlags_.no_inputs
        changed, return_color = imgui.color_edit3(f"##light_{self._node.get_name()}", self._api_object.GetColorAttr().Get(), flags=color_edit_flags)
        if changed:
            self._api_object.GetColorAttr().Set(pgf.Vec3d(return_color[0], return_color[1], return_color[2]))
        imgui.same_line()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - (imgui.get_text_line_height()  * 0.5))
        slider_width = imgui.get_content_region_avail()[0] - 50
        imgui.push_item_width(slider_width)
        slider_flags = 0
        changed, return_intensity = imgui.slider_float(f"##light_intensity_{self._node.get_name()}", self._api_object.GetIntensityAttr().Get(), 0.0, 50.0)
        if changed:
            self._api_object.GetIntensityAttr().Set(return_intensity)
        imgui.pop_item_width()

        imgui.push_style_var(imgui.StyleVar_.frame_padding, (3, 3))
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 1.0)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 2.0)
    
        icon_visibility_enabled_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_EYE_ENABLED, (14, 14))
        icon_visibility_disabled_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_EYE_DISABLED, (14, 14))
        if self._node.get_prim().GetAttribute("visibility").Get() == pgeo.Tokens.invisible:
            icon_visibility_id = icon_visibility_disabled_id
            button_color = (0.15, 0.15, 0.15, 1)
        else:
            icon_visibility_id = icon_visibility_enabled_id
            button_color = (0.3, 0.3, 0.3, 1)
        
        imgui.push_style_color(imgui.Col_.button, button_color)
        imgui.push_style_color(imgui.Col_.button_active, (0.1, 0.1, 0.1, 1))
        imgui.push_style_color(imgui.Col_.button_hovered, (0.4, 0.4, 0.4, 1))
        
        imgui.same_line()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - (imgui.get_text_line_height()  * 0.5))
        if imgui.image_button(f"##visibility_{self._node.get_name()}", icon_visibility_id, (14,14), tint_col=(0, 0, 0, 1)):
            current_visibility = self._node.get_prim().GetAttribute("visibility").Get()
            if current_visibility == pgeo.Tokens.invisible:
                self._node.get_prim().GetAttribute("visibility").Set(pgeo.Tokens.inherited)
            else:
                self._node.get_prim().GetAttribute("visibility").Set(pgeo.Tokens.invisible)

        imgui.push_style_var(imgui.StyleVar_.frame_padding, (2, 2))

        imgui.push_style_color(imgui.Col_.button, (0.3, 0.3, 0.3, 1))
        imgui.push_style_color(imgui.Col_.button_active, (0.1, 0.1, 0.1, 1))
        imgui.push_style_color(imgui.Col_.button_hovered, (0.4, 0.4, 0.4, 1))        
        icon_refresh_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_REFRESH, (16, 16))        
        imgui.same_line()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - (imgui.get_text_line_height()  * 0.5))
        if imgui.image_button(f"##refresh_{self._node.get_name()}", icon_refresh_id, (16,16), tint_col=(0, 0, 0, 1)):
            self._node.get_prim().GetAttribute("visibility").Set(self._node.light_visibility)
            self._api_object.GetColorAttr().Set(self._node.light_color)
            self._api_object.GetIntensityAttr().Set(self._node.light_intensity)
        imgui.pop_style_var(7)
        imgui.pop_style_color(10)        
    