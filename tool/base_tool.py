#####################################################################################################################################
# USD Asset Viewer | Tool | Base
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON
from typing import Any
import os

# ADDONS
from imgui_bundle import imgui

# PROJECT
import core.static.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
import core.render_core as crend
import tool.panel.outliner_panel as tpo
import tool.panel.detail_panel as tpd
import tool.panel.trackbar_panel as tpt
#####################################################################################################################################
      

class USDAssetViewer(cbase.Frame):
    """
    USD Asset Viewer class for displaying USD assets.
    """
    def __init__(self):
        super().__init__()        

    def _init_pre_rendering(self):
        self._init_usd_stage()       

    def _init_panels(self):
        self._outliner_panel = tpo.OutlinerPanel(self)
        self._details_panel = tpd.DetailPanel(self)
        self._trackbar_panel = tpt.TrackbarPanel(self)

    def _init_usd_stage(self):
        usd_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), cstat.DEFAULT_USD_PATH)
        self._scene_manager = cbase.SceneManager(usd_path)
        self._stage = self._scene_manager.get_stage()   

    def _set_window_flags(self):
        super()._set_window_flags()
        self._window_flags |= imgui.WindowFlags_.menu_bar
        self._window_flags |= imgui.WindowFlags_.no_bring_to_front_on_focus
        self._window_flags |= imgui.WindowFlags_.no_background

    def _draw_menu_bar(self):
        imgui.set_next_window_pos((0, 0))
        display_size = imgui.get_io().display_size
        imgui.set_next_window_size(display_size)
        imgui.begin("##menu_bar", True, self._window_flags)
        imgui.begin_menu_bar()
        if imgui.begin_menu("File", True):
            if imgui.menu_item_simple("Open USD", "", False, True):
                print("Open USD")
            if imgui.menu_item_simple("Exit", "", False, True):
                print("Open USD")
            imgui.end_menu()
        imgui.end_menu_bar()    
        imgui.end()

    def draw(self):
        """
        Draw the USD Asset Viewer.
        """
        self._draw_menu_bar()

