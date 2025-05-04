#####################################################################################################################################
# USD Outliner | Utility Core
# TODO:
# -
#####################################################################################################################################

# PYTHON
from enum import Enum
import os
import json
import toml
from typing import Any, Dict, List, Tuple


#IMPORTS
from imgui_bundle import imgui
import pxr.Usd as pusd


import core.static.static_core as cstat

#####################################################################################################################################



#####################################################################################################################################


class FileHelper:
    """
    Class for file input/output operations.
    """
    @classmethod
    def read(cls, file_path: str, file_type: cstat.IOFiletype) -> Any:
        """
        Read data from a file based on its type.
        """
        process_file_type_dict = {
            cstat.IOFiletype.USD: lambda x: cls._read_usd(x),
            cstat.IOFiletype.TOML: lambda x: cls._read_toml(x)
        }
        return process_file_type_dict[file_type](file_path)
    
    def _read_toml(self, file_path) -> Dict[str, Any]:
        """
        Read data from a TOML file.
        """
        with open(file_path, 'r') as file:
            return toml.load(file)
        
    def _read_usd(self, file_path) -> pusd.Stage:
        """
        Read data from a USD file.
        """
        stage = pusd.Stage.Open(file_path)
        return stage


def convert_dict_string(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Convert all keys and values in a dictionary to strings.
    """
    return {str(key): str(value) for key, value in data.items()}

def get_image_id(file_path: str, context: imgui.internal.Context) -> int:
    """
    Load an image from a file and return its ID.
    """
    imgui.set_current_context(context)
    return 0

def get_icon_id(icon_enum: cstat.NodeIcon, context: imgui.internal.Context) -> int:
    """
    Get the ID of an icon based on its name.
    """
    current_dir = os.path.dirname(__file__)
    icon_path = os.path.join(current_dir, 'assets', 'icons', icon_enum.value + ".png")
    return get_image_id(icon_path, context)

def get_usd_default_path() -> str:
    """
    Get the default path for USD files.
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'assets', 'usd')


