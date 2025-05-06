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
import tool.panel.outliner_panel as tbo
import tool.panel.detail_panel as tbd
#####################################################################################################################################
      

class USDAssetViewer(cbase.Frame):
    """
    USD Asset Viewer class for displaying USD assets.
    """
    def __init__(self):
        super().__init__()
        usd_path = os.path.join(cstat.DEFAULT_USD_PATH)
        self._scene_manger = cbase.SceneManager(usd_path)
        self._stage = self._scene_manger.get_stage()

    def _init_panels(self):
        super()._init_panels()
        self._outliner_panel = tbo.OutlinerPanel(self._stage, self._scene_manger)
        self._details_panel = tbd

