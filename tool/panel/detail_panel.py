#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Detail
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
#####################################################################################################################################
      
class DetailPanel(cbase.Panel):
    """
    Detail panel class for display selection details.
    """