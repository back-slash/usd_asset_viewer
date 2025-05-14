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
    MESH_ICON = "icon_mesh"
    LIGHT_ICON = "icon_light"
    CAMERA_ICON = "icon_camera"
    MATERIAL_ICON = "icon_material"
    TEXTURE_ICON = "icon_texture"
    NULL_ICON = "icon_null"
    CURVE_ICON = "icon_curve"
    BONE_ICON = "icon_bone"
    LOCATOR_ICON = "icon_locator"
    SKELETON_ICON = "icon_skeleton"
    UNKNOWN_ICON = "icon_unknown"
    WIREFRAME_ICON = "icon_wireframe"
    FLAT_ICON = "icon_flat"
    FULL_ICON = "icon_full"
    AXIS_Z_ICON = "icon_axis_z"
    AXIS_Y_ICON = "icon_axis_y"


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

