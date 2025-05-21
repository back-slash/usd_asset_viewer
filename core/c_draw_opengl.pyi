from typing import Any, Dict, List

def c_init_glad() -> None:
    """
    Initialize GLAD (OpenGL function loader).
    """

def c_draw_opengl_bone(bone_list: List[Any], draw_dict: Dict[str, Any]) -> None:
    """
    Draw bones using OpenGL.

    Args:
        bone_list: List of bone objects (Python objects with get_data_object()).
        draw_dict: Drawing parameters:
            - hydra_x_min: int
            - hydra_y_min: int
            - panel_width: int
            - panel_height: int
            - fov: float
            - near_z: float
            - far_z: float
            - camera_matrix: pxr.GfMatrix4d
            - up_matrix: pxr.GfMatrix4d
            - grid_density: int
            - scene_bbox_size: pxr.GfVec3d
            - grid_color: List[float]
            - up_axis: str
    """

def c_draw_opengl_bone_xray(bone_list: List[Any], draw_dict: Dict[str, Any]) -> None:
    """
    Draw bones with X-ray effect using OpenGL.

    Args:
        bone_list: List of bone objects (Python objects with get_data_object()).
        draw_dict: Drawing parameters:
            - hydra_x_min: int
            - hydra_y_min: int
            - panel_width: int
            - panel_height: int
            - fov: float
            - near_z: float
            - far_z: float
            - camera_matrix: pxr.GfMatrix4d
            - up_matrix: pxr.GfMatrix4d
            - grid_density: int
            - scene_bbox_size: pxr.GfVec3d
            - grid_color: List[float]
            - up_axis: str
    """

def c_draw_opengl_grid(draw_dict: Dict[str, Any]) -> None:
    """
    Draw a grid using OpenGL.

    Args:
        draw_dict: Drawing parameters:
            - hydra_x_min: int
            - hydra_y_min: int
            - panel_width: int
            - panel_height: int
            - fov: float
            - near_z: float
            - far_z: float
            - camera_matrix: pxr.GfMatrix4d
            - up_matrix: pxr.GfMatrix4d
            - grid_density: int
            - scene_bbox_size: pxr.GfVec3d
            - grid_color: List[float]
            - up_axis: str
    """

def c_draw_opengl_gizmo(draw_dict: Dict[str, Any]) -> None:
    """
    Draw a small orientation gizmo using OpenGL.

    Args:
        draw_dict: Drawing parameters:
            - hydra_x_min: int
            - hydra_y_min: int
            - panel_width: int
            - panel_height: int
            - fov: float
            - near_z: float
            - far_z: float
            - camera_matrix: pxr.GfMatrix4d
            - up_matrix: pxr.GfMatrix4d
            - grid_density: int
            - scene_bbox_size: pxr.GfVec3d
            - grid_color: List[float]
            - up_axis: str
    """

def c_draw_opengl_light(draw_dict: Dict[str, Any], light_dict: Dict[str, Any]) -> None:
    """
    Draw lights using OpenGL.

    Args:
        draw_dict: Drawing parameters:
            - hydra_x_min: int
            - hydra_y_min: int
            - panel_width: int
            - panel_height: int
            - fov: float
            - near_z: float
            - far_z: float
            - camera_matrix: pxr.GfMatrix4d
            - up_matrix: pxr.GfMatrix4d
            - grid_density: int
            - scene_bbox_size: pxr.GfVec3d
            - grid_color: List[float]
            - up_axis: str
        light_dict: Dictionary mapping light names to light parameter dicts.
            Each light parameter dict should contain:
                - visibility: bool
                - color: List[float] (RGB)
                - matrix: pxr.GfMatrix4d
    """

def c_draw_opengl_camera(draw_dict: Dict[str, Any], camera_dict: Dict[str, Any]) -> None:
    """
    Draw cameras using OpenGL.

    Args:
        draw_dict: Drawing parameters:
            - hydra_x_min: int
            - hydra_y_min: int
            - panel_width: int
            - panel_height: int
            - fov: float
            - near_z: float
            - far_z: float
            - camera_matrix: pxr.GfMatrix4d
            - up_matrix: pxr.GfMatrix4d
            - grid_density: int
            - scene_bbox_size: pxr.GfVec3d
            - grid_color: List[float]
            - up_axis: str
        camera_dict: Dictionary mapping camera names to camera parameter dicts.
            Each camera parameter dict should contain:
                - matrix: pxr.GfMatrix4d
                - prim: UsdPrim
                - visibility: bool
    """

