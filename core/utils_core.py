#####################################################################################################################################
# USD Asset Viewer | Core | Utility
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
    def read(cls, file_path: str, file_type: cstat.Filetype) -> Any:
        """
        Read data from a file based on its type.
        """
        process_file_type_dict = {
            cstat.Filetype.USD: lambda x: cls._read_usd(x),
            cstat.Filetype.TOML: lambda x: cls._read_toml(x),
            cstat.Filetype.IMG: lambda x: cls._read_img(x),
            cstat.Filetype.ICON: lambda x: cls._read_icon(x),

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
        return 0
    
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


