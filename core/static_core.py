#####################################################################################################################################
# USD Asset Viewer | Core | Static
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON
from enum import Enum

# ADDONS
from pxr import UsdImagingGL as pimg


#####################################################################################################################################


class Filetype(Enum):
    """
    Enum for file types used in the prototype.
    """
    USD = 1
    TOML = 2
    IMG = 3
    ICON = 4


class Icon(Enum):
    """
    Enum for node types.
    """
    ICON_ROOT = "icon_root"
    ICON_MESH = "icon_mesh"
    ICON_LIGHT = "icon_light"
    ICON_CAMERA = "icon_camera"
    ICON_MATERIAL = "icon_material"
    ICON_TEXTURE = "icon_texture"
    ICON_NULL = "icon_null"
    ICON_CURVE = "icon_curve"
    ICON_BONE = "icon_bone"
    ICON_LOCATOR = "icon_locator"
    ICON_SKELETON = "icon_skeleton"
    ICON_SKELETON_ROOT = "icon_skeleton"
    ICON_ANIMATION = "icon_animation"
    ICON_UNKNOWN = "icon_unknown"
    ICON_VIEWPORT_WIREFRAME = "icon_viewport_wireframe"
    ICON_VIEWPORT_FLAT = "icon_viewport_flat"
    ICON_VIEWPORT_FULL = "icon_viewport_full"
    ICON_VIEWPORT_AXIS_Z = "icon_viewport_axis_z"
    ICON_VIEWPORT_AXIS_Y = "icon_viewport_axis_y"
    ICON_VIEWPORT_LIGHT = "icon_viewport_light"
    ICON_VIEWPORT_CAMERA = "icon_viewport_camera"
    ICON_VIEWPORT_SETTINGS = "icon_viewport_settings"
    ICON_TRACKBAR_PLAY = "icon_trackbar_play"
    ICON_TRACKBAR_STOP = "icon_trackbar_stop"
    ICON_TRACKBAR_PAUSE = "icon_trackbar_pause"
    ICON_TRACKBAR_START = "icon_trackbar_start"
    ICON_TRACKBAR_END = "icon_trackbar_end"
    ICON_TRACKBAR_SETTINGS = "icon_trackbar_settings"



class PanelTypes(Enum):
    """
    Enum for panel modes.
    """
    OUTLINER = 0
    DETAIL = 1
    NODE_NETWORK = 2
    TRACKBAR = 3
    VIEWPORT = 4


#####################################################################################################################################

