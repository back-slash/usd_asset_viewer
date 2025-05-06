#####################################################################################################################################
# USD Asset Viewer | Core | Static
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON
from enum import Enum


#####################################################################################################################################

DEFAULT_USD_PATH = "core\\assets\\usd\\example.usdc"


class FontType(Enum):
    """
    Enum for font types used in the prototype.
    """
    DEFAULT = 0
    VERDANA = 1
    ARIAL = 2
    TIMES = 3
    SEGOEUI = 4
    CONSOLAS = 5


class FontSetSizes(Enum):
    """
    Enum for font sizes used in the prototype.
    """
    TINY = 8
    SMALL = 12
    MEDIUM = 16
    LARGE = 24


class Filetype(Enum):
    """
    Enum for file types used in the prototype.
    """
    USD = 1
    TOML = 2
    IMG = 3
    ICON = 4


class NodeIcon(Enum):
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


class PanelTypes(Enum):
    """
    Enum for panel modes.
    """
    NONE = 0
    OUTLINER = 1
    DETAIL = 2
    NODE_EDITOR = 3



#####################################################################################################################################

LINE_HEIGHT = 20
LINE_ROUNDING = 2.0
LINE_SPACING = 0.0
LINE_COLOR = (0.2, 0.2, 0.2, 1.0)
LINE_COLOR_ALTERNATE = (0.3, 0.3, 0.3, 1.0)



