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
    def __init__(self, title: str = "USD Asset Viewer", width: int = 1280, height: int = 720):
        super().__init__(title, width, height)
        usd_path = os.path.join(cstat.DEFAULT_USD_PATH)
        self._scene_manger = cbase.SceneManager(usd_path)
        self._stage = self._scene_manger.get_stage()

    def _init_panels(self):
        super()._init_panels()
        self._outliner_panel = tpo.OutlinerPanel()
        self._details_panel = tpd.DetailPanel()
        self._trackbar_panel = tpt.TrackbarPanel()

    def draw(self):
        """
        Draw the USD Asset Viewer.
        """
        self._update_size()
        self._outliner_panel.draw()
        self._details_panel.draw()
        self._trackbar_panel.draw()

