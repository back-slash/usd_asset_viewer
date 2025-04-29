#####################################################################################################################################
# USD Outliner | Utility Core
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON
from enum import Enum
import os
import json
import toml
from typing import Any, Dict, List, Tuple


#IMPORTS
import imgui


import core.static.static_core as cstat

#####################################################################################################################################



#####################################################################################################################################



def write_to_file(file_path: str, data: Any, file_type: cstat.PrototypeFiletype) -> None:
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


def load_image(file_path: str) -> int:
    """
    Load an image from a file and return its ID.
    """
    # Placeholder for image loading logic
    return 0


