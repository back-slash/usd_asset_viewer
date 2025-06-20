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
import time


# PROJECT
import core.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
import tool.panel.outliner_panel as tpo
import tool.panel.detail_panel as tpd
import tool.panel.trackbar_panel as tpt
import tool.panel.viewport_panel as tvp
#####################################################################################################################################

#####################################################################################################################################
class USDAssetViewer(cbase.Frame):
    """
    USD Asset Viewer class for displaying USD assets.
    """
    _sm = None
    def __init__(self):
        self._cache_time = time.time()
        self._frame_count = 0
        self._fps = 0
        super().__init__()
        self._usd_path = None
        self._cfg = cutils.get_core_config()
        self._init_rendering()

    def _init_pre_rendering(self):
        pass     

    def _init_panels(self):
        self._outliner_panel = tpo.OutlinerPanel(self)
        self._details_panel = tpd.DetailPanel(self)
        self._trackbar_panel = tpt.TrackbarPanel(self)
        self._viewport = tvp.ViewportPanel(self)
        self._panel_list = [
            self._outliner_panel,
            self._details_panel,
            self._trackbar_panel,
            self._viewport
        ]

    def _init_usd_stage(self, usd_path=None):
        """
        Initialize the USD stage and scene manager.
        """
        if self._usd_path and usd_path == self._usd_path:
            self._sm.set_animation(False)
            self._trackbar_panel.set_enable_animation(False)
            self._sm.reload_scene()
            return
        if usd_path:
            self._sm = cbase.SceneManager(usd_path)
        else:
            self._sm = cbase.SceneManager(default=True)
        self._viewport.update_usd()
        self._outliner_panel.update_usd()
        self._details_panel.update_usd()
        self._trackbar_panel.update_usd()
        self._usd_path = usd_path

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
                for file in os.listdir(cutils.get_usd_default_path()):
                    if file.endswith(".usda") or file.endswith(".usdc"):
                        if imgui.menu_item_simple(file, "", False, True):
                            usd_path = os.path.join(cutils.get_usd_default_path(), file)
                            self._init_usd_stage(usd_path)
                            self._viewport.calc_frame_scene()
                imgui.end_menu()
            if imgui.menu_item_simple("Close USD", "", False, True):
                self._init_usd_stage()
                self._viewport.calc_frame_scene()          
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

    def _draw_stats_overlay(self, viewport_position: imgui.ImVec2Like, viewport_size: imgui.ImVec2Like):
        """
        Draw the FPS overlay.
        """
        self._frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self._cache_time
        if elapsed_time > 1.0:
            self._fps = self._frame_count / elapsed_time
            self._frame_count = 0
            self._cache_time = current_time
        if self._fps == 0:
            return
        stats_color = imgui.get_color_u32((0.8, 0.5, 0.0, 1.0))
        fps_text = f"FPS: {self._fps:.1f}"
        ms_text = f"MS: {1000 / self._fps:.1f}"
        draw_list = imgui.get_foreground_draw_list()
        fps_position = imgui.ImVec2(viewport_position[0] + viewport_size[0] - 55, viewport_position[1] + viewport_size[1] - 30)
        draw_list.add_text(fps_position, stats_color, fps_text)
        ms_position = fps_position + imgui.ImVec2(0, 15)
        draw_list.add_text(ms_position, stats_color, ms_text)

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
        if self._viewport.get_user_cfg()["show"]['FPS']:
            stats_overlay_position = imgui.ImVec2(viewport_rect[0], viewport_rect[1])
            stats_overlay_size = imgui.ImVec2(viewport_rect[2] - viewport_rect[0], viewport_rect[3] - viewport_rect[1])
            self._draw_stats_overlay(stats_overlay_position, stats_overlay_size)

    def _shutdown(self, *args):
        for panel in self._panel_list:
            panel.shutdown()
        super()._shutdown(*args)