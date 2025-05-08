#####################################################################################################################################
# USD Asset Viewer | Core | Utility
# TODO:
# -
#####################################################################################################################################

# PYTHON
import os
import toml
from typing import Any, Dict, List, Tuple


# ADDONS
from imgui_bundle import imgui
import OpenGL.GL as gl
import pxr.Usd as pusd
from PIL import Image

# PROJECT
import core.static_core as cstat

#####################################################################################################################################



#####################################################################################################################################


class FileHelper:
    """
    Class for file input/output operations.
    """
    @classmethod
    def read(cls, file_path: str, file_type: cstat.Filetype) -> Any:
        """
        Read data from a file based on its type.
        """
        process_file_type_dict = {
            cstat.Filetype.USD: lambda input: cls._read_usd(input),
            cstat.Filetype.TOML: lambda input: cls._read_toml(input),
            cstat.Filetype.IMG: lambda input: cls._read_img(input),
            cstat.Filetype.ICON: lambda input: cls._read_icon(input),
        }
        return process_file_type_dict[file_type](file_path)
    
    @classmethod
    def _read_toml(cls, file_path) -> Dict[str, Any]:
        """
        Read data from a TOML file.
        """
        with open(file_path, 'r') as file:
            return toml.load(file)

    @classmethod    
    def _read_usd(cls, file_path) -> pusd.Stage:
        """
        Read data from a USD file.
        """
        usd_stage = pusd.Stage.Open(file_path)
        return usd_stage

    @classmethod
    def _read_img(self, file_path) -> int:
        """
        Read data from an image file.
        """
        if os.path.exists(file_path):
            image = Image.open(file_path).convert("RGBA")
            image_data = image.tobytes("raw", "RGBA", 0, -1)
            width, height = image.size
            gl.glEnable(gl.GL_TEXTURE_2D)
            texture_id = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image_data)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
            image.close()
            return texture_id

    @classmethod
    def _read_icon(self, icon: cstat.NodeIcon) -> int:
        """
        Read data from an icon file.
        """
        current_dir = os.path.dirname(__file__)
        icon_path = os.path.join(current_dir, 'asset', 'icons', icon.value + ".png")
        return self._read_img(icon_path)


def convert_dict_string(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Convert all keys and values in a dictionary to strings.
    """
    return {str(key): str(value) for key, value in data.items()}


def get_usd_default_path() -> str:
    """
    Get the default path for USD files.
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'asset', 'usd')


def get_font_path() -> str:
    """
    Get the default font path.
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'asset', 'font')


def get_core_config() -> Dict[str, Any]:
    """
    Get the core configuration from the TOML file.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.toml")
    if os.path.exists(config_path):
        config: dict = FileHelper.read(config_path, cstat.Filetype.TOML)
        return config
    else:
        raise FileNotFoundError(f"Config not found: {config_path}")
    

def set_window_flag(window_flags: int, config_section: dict, config_identifier: str) -> int:
    """
    Set or unset a specific window flag for the frame based on the configuration.
    """
    if hasattr(imgui.WindowFlags_, config_identifier):
        imgui_identifier = getattr(imgui.WindowFlags_, config_identifier)
    else:
        raise AttributeError(f"{config_identifier} is not a valid attribute of imgui.WindowFlags_")
    if config_section.get(config_identifier, False):
        window_flags |= imgui_identifier
    else:
        window_flags &= ~imgui_identifier
    return window_flags



def set_flag(flag: int, value: bool):
    """
    Set a specific flag for the frame.
    """
    if value:
        imgui.get_io().config_flags |= flag
    else:
        imgui.get_io().config_flags &= ~flag


def push_style_var(config_section, config_identifier: str):
    """
    Push a style color to the frame.
    """
    value = config_section[config_identifier]
    if hasattr(imgui.StyleVar_, config_identifier):
        imgui_identifier = getattr(imgui.StyleVar_, config_identifier)
        imgui.push_style_var(imgui_identifier, value)


def push_style_color(config_section, config_identifier: str):
    """
    Push a style color to the frame.
    """
    color = config_section[config_identifier]
    if hasattr(imgui.Col_, config_identifier):
        imgui_identifier = getattr(imgui.Col_, config_identifier)
        imgui.push_style_color(imgui_identifier, color)