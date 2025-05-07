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
    _scene_manager = None
    def __init__(self):
        self._cfg = cutils.get_core_config() 
        super().__init__()    

    def _init_pre_rendering(self):
        pass     

    def _init_panels(self):
        self._outliner_panel = tpo.OutlinerPanel(self)
        self._details_panel = tpd.DetailPanel(self)
        self._trackbar_panel = tpt.TrackbarPanel(self)

    def _init_usd_stage(self, usd_path=None):
        """
        Initialize the USD stage and scene manager.
        """
        if usd_path is None:
            usd_path = os.path.join(cutils.get_usd_default_path(), self._cfg['settings']['default_usd'])
        if not self._scene_manager:
            self._scene_manager = cbase.SceneManager(usd_path)
            self._stage = self._scene_manager.get_stage()
        else:
            self._scene_manager.set_usd_file(usd_path)
        self._render_context_manager.set_usd_stage(self._scene_manager.get_stage())

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
            if imgui.begin_menu("Open USD", True):
                usd_file_list = [file for file in os.listdir(cutils.get_usd_default_path())]
                for usd_file in usd_file_list:
                    if imgui.menu_item_simple(usd_file, "", False, True):
                        usd_path = os.path.join(cutils.get_usd_default_path(), usd_file)
                        self._init_usd_stage(usd_path)
                imgui.end_menu()
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

