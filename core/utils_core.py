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


import core.static.static_core as cstat

#####################################################################################################################################



#####################################################################################################################################



def write_to_file(file_path: str, data: Any, file_type: cstat.Filetype) -> None:
    """
    Write data to a file.
    """
    with open(file_path, 'w') as file:
        process_file_type_dict = {
            cstat.Filetype.TEXT: lambda x: file.write(x),
            cstat.Filetype.USD: lambda x: file.write(x),
            cstat.Filetype.JSON: lambda x: json.dump(x, file, indent=4),
            cstat.Filetype.TOML: lambda x: toml.dumps(x)
        }
        process_file_type_dict[file_type](data)

def read_from_file(file_path: str, file_type) -> str:
    """
    Read data from a file.
    """
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def convert_dict_string(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Convert all keys and values in a dictionary to strings.
    """
    return {str(key): str(value) for key, value in data.items()}

def load_image(file_path: str, context: imgui.internal.Context) -> int:
    """
    Load an image from a file and return its ID.
    """
    imgui.set_current_context(context)
    return 0

def _get_icon_path(icon_enum: cstat.Icons) -> str:
    """
    Get the path of an icon based on its name.
    """
    current_dir = os.path.dirname(__file__)
    icon_path = os.path.join(current_dir, 'assets', 'icons', icon_enum.value + ".png")
    return icon_path

def get_icon(icon_enum: cstat.Icons, context: imgui.internal.Context) -> int:
    """
    Get the ID of an icon based on its name.
    """
    icon_path = _get_icon_path(icon_enum)
    return load_image(icon_path, context)

def get_usd_default_path() -> str:
    """
    Get the default path for USD files.
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'assets', 'usd')


