#####################################################################################################################################
# USD Asset Viewer | Tool | Base
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON
import sys
from typing import Any
import os

# ADDONS
from imgui_bundle import imgui
import glfw

# PROJECT
import core.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
import tool.panel.outliner_panel as tpo
import tool.panel.detail_panel as tpd
import tool.panel.trackbar_panel as tpt
import tool.panel.viewport_panel as tvp
#####################################################################################################################################
      

class USDAssetViewer(cbase.Frame):
    """
    USD Asset Viewer class for displaying USD assets.
    """
    _scene_manager = None
    def __init__(self):
        super().__init__()
        self._cfg = cutils.get_core_config()
        self._init_rendering()

    def _init_pre_rendering(self):
        pass     

    def _init_panels(self):
        self._outliner_panel = tpo.OutlinerPanel(self)
        self._details_panel = tpd.DetailPanel(self)
        self._trackbar_panel = tpt.TrackbarPanel(self)
        self._viewport = tvp.ViewportPanel(self)

    def _init_usd_stage(self, usd_path=None):
        """
        Initialize the USD stage and scene manager.
        """
        if usd_path is None:
            usd_path = os.path.join(cutils.get_usd_default_path(), self._cfg['settings']['default_usd'])
        self._scene_manager = cbase.SceneManager(usd_path)
        self._viewport.update_usd()
        self._outliner_panel.update_usd()
        self._details_panel.update_usd()
        self._trackbar_panel.update_usd()

    def _set_window_flags(self):
        super()._set_window_flags()
        self._window_flags |= imgui.WindowFlags_.menu_bar

    def _draw_menu_bar(self):
        imgui.set_next_window_pos((0, 0))
        display_size = imgui.get_io().display_size
        imgui.set_next_window_size(display_size)
        imgui.begin("##menu_bar", True, self._window_flags)
        imgui.begin_menu_bar()
        if imgui.begin_menu("File", True):
            if imgui.begin_menu("Open USD", True):
                usd_file_list = [file for file in os.listdir(cutils.get_usd_default_path())]
                for usd_file in usd_file_list:
                    if imgui.menu_item_simple(usd_file, "", False, True):
                        usd_path = os.path.join(cutils.get_usd_default_path(), usd_file)
                        self._init_usd_stage(usd_path)
                imgui.end_menu()
            if imgui.menu_item_simple("Exit", "", False, True):
                self._shutdown()
            imgui.end_menu()
        imgui.end_menu_bar()
        menu_bar_size = imgui.get_item_rect_size()   
        item_rect_max = imgui.get_item_rect_max()        
        draw_list = imgui.get_window_draw_list()
        window_pos = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        menu_line_min = imgui.ImVec2(window_pos[0], window_pos[1] + item_rect_max.y)
        menu_line_max = imgui.ImVec2(menu_line_min[0] + window_size[0], menu_line_min[1] + 1)
        draw_list.add_rect_filled(menu_line_min, menu_line_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=0.0, flags=0)
        imgui.end()
        return menu_bar_size

    def draw(self):
        """
        Draw the USD Asset Viewer.
        """
        self._menu_bar_size = self._draw_menu_bar()
        min_y = self._menu_bar_size.y + 2
        trackbar_min_y = self._display_size[1] - self._cfg['trackbar']['height']
        trackbar_size_x = self._display_size[0]
        trackbar_size_y = self._cfg['trackbar']['height']
        trackbar_rect = self._trackbar_panel.update_draw((0, trackbar_min_y), (trackbar_size_x, trackbar_size_y))

        outliner_size_x = self._cfg['outliner']['width']
        panel_size_y = self._display_size[1] - trackbar_size_y - min_y
        outliner_rect = self._outliner_panel.update_draw((0, min_y), (outliner_size_x, panel_size_y))
        
        details_min_x = self._display_size[0] - self._cfg['detail']['width']
        details_size_x = self._cfg['detail']['width']
        details_rect = self._details_panel.update_draw((details_min_x, min_y), (details_size_x, panel_size_y))

        viewport_size_x = self._display_size[0] - (outliner_rect[2] - outliner_rect[0]) - (details_rect[2] - details_rect[0])
        viewport_rect = self._viewport.update_draw((outliner_rect[2], min_y), (viewport_size_x, panel_size_y))

