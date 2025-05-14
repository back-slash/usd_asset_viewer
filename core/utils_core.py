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
import pxr.Gf as pgf

# PROJECT
import core.static_core as cstat

#####################################################################################################################################



#####################################################################################################################################


class FileHelper:
    """
    Class for file input/output operations.
    """
    @classmethod
    def read(cls, file_type: cstat.Filetype, *args) -> Any:
        """
        Read data from a file based on its type.
        """
        process_file_type_dict = {
            cstat.Filetype.USD: lambda *args: cls._read_usd(*args),
            cstat.Filetype.TOML: lambda *args: cls._read_toml(*args),
            cstat.Filetype.IMG: lambda *args: cls._read_img(*args),
            cstat.Filetype.ICON: lambda *args: cls._read_icon(*args),
        }
        return process_file_type_dict[file_type](*args)
    
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
    def _read_img(cls, file_path, size: tuple[int, int]) -> int:
        """
        Read data from an image file.
        """
        if os.path.exists(file_path):
            image = Image.open(file_path).convert("RGBA")
            image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            image = image.resize(size, Image.Resampling.LANCZOS)
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
    def _read_icon(cls, icon: cstat.Icon, size: tuple[int, int]) -> int:
        """
        Read data from an icon file.
        """
        icon_base_path = get_icon_path()
        icon_path = os.path.join(icon_base_path, icon.value + ".png")
        return cls._read_img(icon_path, size)


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

def get_icon_path() -> str:
    """
    Get the default icon path.
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'asset', 'icon')

def get_core_config() -> Dict[str, Any]:
    """
    Get the core configuration from the TOML file.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.toml")
    if os.path.exists(config_path):
        config: dict = FileHelper.read(cstat.Filetype.TOML, config_path)
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

def calc_look_at(source_position: pgf.Vec3d, target_position: pgf.Vec3d, up: pgf.Vec3d, flip_forward:bool = False) -> pgf.Matrix4d:
    """
    Calculate the look-at matrix.
    """
    forward_vector: pgf.Vec3d = (target_position - source_position)
    forward_vector = forward_vector.GetNormalized()
    up = up.GetNormalized()
    if flip_forward:
        forward_vector = -forward_vector
    right_vector: pgf.Vec3d = up.GetCross(forward_vector).GetNormalized()
    up_vector: pgf.Vec3d = forward_vector.GetCross(right_vector).GetNormalized()
    look_at_matrix: pgf.Matrix4d = pgf.Matrix4d(
        right_vector[0], right_vector[1], right_vector[2], 0,
        up_vector[0], up_vector[1], up_vector[2], 0,
        forward_vector[0], forward_vector[1], forward_vector[2], 0,
        source_position[0], source_position[1], source_position[2], 1
    )
    return look_at_matrix