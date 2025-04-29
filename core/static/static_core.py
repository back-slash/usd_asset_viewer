#####################################################################################################################################
# USD Outliner | Static Core
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON
from enum import Enum

#####################################################################################################################################

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


class Filetype(Enum):
    """
    Enum for file types used in the prototype.
    """
    TEXT = 0
    USD = 1
    JSON = 2
    TOML = 3



class Icons(Enum):
    """
    Enum for icons used in the prototype.
    """
    MESH_ICON = "icon_mesh"
    LIGHT_ICON = "icon_light"
    CAMERA_ICON = "icon_camera"
    MATERIAL_ICON = "icon_material"
    TEXTURE_ICON = "icon_texture"
    NULL_ICON = "icon_null"
    CURVE_ICON = "icon_curve"


#####################################################################################################################################




