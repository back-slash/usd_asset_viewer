#####################################################################################################################################
# PrototypeUtils.py
# This module contains utility functions and classes for the prototype.
#####################################################################################################################################

#PYTHON
from enum import Enum
import os
import json
import toml
from typing import Any, Dict, List, Tuple
import platform


#IMPORTS
import imgui


import statics.statics

#####################################################################################################################################



#####################################################################################################################################

def init_font(font_name: ps.PrototypeFont, font_size: float, renderer: GlfwRenderer):
    io = imgui.get_io()
    font_dict = {
        ps.PrototypeFont.DEFAULT: None,
        ps.PrototypeFont.VERDANA: "verdana.ttf",
        ps.PrototypeFont.ARIAL: "arial.ttf",
        ps.PrototypeFont.TIMES: "times.ttf",
        ps.PrototypeFont.SEGOEUI: "segoeui.ttf",
        ps.PrototypeFont.CONSOLAS: "consola.ttf"
    }
    font_path = os.path.join(get_font_directory(), font_dict[font_name])
    if os.path.exists(font_path):
        font = io.fonts.add_font_from_file_ttf(font_path, font_size)
        renderer.refresh_font_texture()
    return font


def get_font_directory():
    system = platform.system()
    if system == 'Windows':
        return 'C:\\Windows\\Fonts'
    elif system == 'Darwin':
        return '/System/Library/Fonts'
    elif system == 'Linux':
        return '/usr/share/fonts'
    else:
        return None
    

def write_to_file(file_path: str, data: Any, file_type: ps.PrototypeFiletype) -> None:
    """
    Write data to a file.
    """
    with open(file_path, 'w') as file:
        process_file_type_dict = {
            ps.PrototypeFiletype.TEXT: lambda x: file.write(x),
            ps.PrototypeFiletype.USD: lambda x: file.write(x),
            ps.PrototypeFiletype.JSON: lambda x: json.dump(x, file, indent=4),
            ps.PrototypeFiletype.TOML: lambda x: toml.dumps(x)
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