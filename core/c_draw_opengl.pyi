from typing import Any, Dict, List

def c_init_glad() -> None:
    """
    Initialize GLAD (OpenGL function loader).
    No input parameters.
    Returns:
        None
    """

def c_draw_opengl_bone(bone_list: List[Any], draw_dict: Dict[str, Any]) -> None:
    """
    Draw bones using OpenGL.

    Args:
        bone_list: List of bone objects (Python objects with get_data_object and get_child_nodes).
        draw_dict: Dictionary with drawing parameters. Expected keys:
            - "hydra_x_min": int — Minimum X coordinate of the viewport
            - "hydra_y_min": int — Minimum Y coordinate of the viewport
            - "panel_width": int — Width of the viewport/panel
            - "panel_height": int — Height of the viewport/panel
            - "fov": float — Field of view (in degrees)
            - "near_z": float — Near clipping plane distance
            - "far_z": float — Far clipping plane distance
            - "camera_matrix": Any — Camera transformation matrix (pxr.GfMatrix4d)
            - "grid_density": int — Number of grid lines in each direction
            - "scene_bbox_size": Any — Size of the scene bounding box (pxr.GfVec3d)
            - "grid_color": List[float] — RGBA color for the grid lines
            - "up_axis": str — Up axis direction, e.g., "Y" or "Z"
    """

def c_draw_opengl_bone_xray(bone_list: List[Any], draw_dict: Dict[str, Any]) -> None:
    """
    Draw bones with X-ray effect using OpenGL.

    Args:
        bone_list: List of bone objects (Python objects with get_data_object and get_child_nodes).
        draw_dict: Dictionary with drawing parameters. Expected keys:
            - "hydra_x_min": int — Minimum X coordinate of the viewport
            - "hydra_y_min": int — Minimum Y coordinate of the viewport
            - "panel_width": int — Width of the viewport/panel
            - "panel_height": int — Height of the viewport/panel
            - "fov": float — Field of view (in degrees)
            - "near_z": float — Near clipping plane distance
            - "far_z": float — Far clipping plane distance
            - "camera_matrix": Any — Camera transformation matrix (pxr.GfMatrix4d)
            - "grid_density": int — Number of grid lines in each direction
            - "scene_bbox_size": Any — Size of the scene bounding box (pxr.GfVec3d)
            - "grid_color": List[float] — RGBA color for the grid lines
            - "up_axis": str — Up axis direction, e.g., "Y" or "Z"
    """

def c_draw_opengl_grid(draw_dict: Dict[str, Any]) -> None:
    """
    Draw a grid using OpenGL.

    Args:
        draw_dict: Dictionary with drawing parameters. Expected keys:
            - "hydra_x_min": int — Minimum X coordinate of the viewport
            - "hydra_y_min": int — Minimum Y coordinate of the viewport
            - "panel_width": int — Width of the viewport/panel
            - "panel_height": int — Height of the viewport/panel
            - "fov": float — Field of view (in degrees)
            - "near_z": float — Near clipping plane distance
            - "far_z": float — Far clipping plane distance
            - "camera_matrix": Any — Camera transformation matrix (pxr.GfMatrix4d)
            - "grid_density": int — Number of grid lines in each direction
            - "scene_bbox_size": Any — Size of the scene bounding box (pxr.GfVec3d)
            - "grid_color": List[float] — RGBA color for the grid lines
            - "up_axis": str — Up axis direction, e.g., "Y" or "Z"
    """