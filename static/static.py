#####################################################################################################################################
# File: prototypeStatics.py
# This module contains static variables and constants used in the prototype.
#####################################################################################################################################

#PYTHON
from enum import Enum


#####################################################################################################################################

class PrototypeFont(Enum):
    """
    Enum for font types used in the prototype.
    """
    DEFAULT = 0
    VERDANA = 1
    ARIAL = 2
    TIMES = 3
    SEGOEUI = 4
    CONSOLAS = 5

class PrototypeFiletype(Enum):
    """
    Enum for file types used in the prototype.
    """
    TEXT = 0
    USD = 1
    JSON = 2
    TOML = 3


class PrototypePanelType(Enum):
    """
    Enum for panel types used in the prototype.
    """
    ASSET_BROWSER = 0
    OUTLINER = 1
    NODE_EDITOR = 2
    CONTROL = 3
    TOOLBAR = 4
    PROPERTIES = 5
    LOG = 6
    GENERIC = 7


class PrototypeDockLocation(Enum):
    """
    Enum for dock locations used in the prototype.
    """
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
    FLOATING = 4

#####################################################################################################################################
USD_FILE_PATH = "P:\\DATA\\GAMEDEV\\CODE\\ntoolkit\\code\\.prototype\\usd_files\\ARM.usdc"
USD_DIRECTORY = "P:\\DATA\\GAMEDEV\\CODE\\ntoolkit\\code\\.prototype\\usd_files"
#####################################################################################################################################

DEFAULT_OUTLINER_WIDTH = 1280
DEFAULT_OUTLINER_HEIGHT = 720

#####################################################################################################################################


OUTLINER_WINDOW_PADDING = (6, 6)
OUTLINER_WINDOW_ROUNDING = 0.0
OUTLINER_LINE_HEIGHT = 24
OUTLINER_SCALE = 1.0
OUTLINER_ITEM_SPACING = (8, 12)


OUTLINER_TITLE_BG_COLOUR = (0.2, 0.2, 0.2, 1.0)
OUTLINER_TITLE_ACTIVE_BG_COLOUR = (0.3, 0.3, 0.3, 1.0)



OUTLINER_BG_COLOUR = (0.05, 0.05, 0.05, 1.0)
OUTLINER_LINE_COLOUR_LIGHT = (0.1, 0.1, 0.1, 1.0)
OUTLINER_LINE_COLOUR_DARK = (0.075, 0.075, 0.075, 1.0)



