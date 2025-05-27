#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Viewport
# TODO:
#
#####################################################################################################################################
import build
# PYTHON
from typing import Any
import math
import sys
import pprint as pp
import threading

# ADDONS
from imgui_bundle import imgui
import glfw
import OpenGL.GL as gl
import pxr.Usd as pusd
import pxr.UsdGeom as pgeo
import pxr.UsdImagingGL as pimg
import pxr.Gf as pgf
import pxr.Sdf as psdf
import pxr.UsdLux as plux
import pxr.UsdShade as pshd
import numpy as np

# C++
import core.c_base as cdraw

# PROJECT
import core.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
#####################################################################################################################################






#####################################################################################################################################      
class ViewportPanel(cbase.Panel):
    """
    Viewport for USD Scene.
    """
    def __init__(self, frame: cbase.Frame):
        self._key_scroll_up = False
        self._key_scroll_down = False
        self._current_draw_style = None
        self._default_light = True
        self._scene_light = False
        self._hydra = None    
        super().__init__("viewport", frame)
        self._window = frame.get_window()
        self._init_hydra()
        self._init_viewport_draw_styles()
        self._update_hydra_render_params()

    def _init_config(self):
        super()._init_config()
        self._user_cfg = {}
        self._user_cfg["show"] = {}
        self._user_cfg["show"]["mesh"] = True
        self._user_cfg["show"]["grid"] = True
        self._user_cfg["show"]["gizmo"] = True
        self._user_cfg["show"]["lights"] = True
        self._user_cfg["show"]["camera"] = True
        self._user_cfg["show"]["bones"] = True
        self._user_cfg["show"]["xray"] = False
        self._user_cfg["show"]["FPS"] = True

    def _init_viewport_draw_styles(self):
        """
        Initialize viewport draw styles.
        """
        self._draw_style_dict = self._cfg["viewport"]["draw_style"]
        self._current_draw_style = self._cfg["viewport"]["default_draw_style"]

    def _init_hydra(self):
        """
        Initialize Hydra renderer.
        """
        self._hydra = pimg.Engine()
        render_plugins = self._hydra.GetRendererPlugins()
        if render_plugins:
            self._hydra.SetRendererPlugin(render_plugins[0])
            self._scene_bbox_center, self._scene_bbox_size = self._sm.create_scene_bounding_box()
            self._hydra.SetCameraPath(self._sm.get_camera().GetPath())
            cdraw.c_init_glad()
            self._sm.calc_light_xform_default()
            self.calc_frame_scene()
        else:
            raise RuntimeError("No renderer plugins available")

    def _update_hydra_render_params(self):
        """
        Update Hydra render parameters.
        """
        draw_style_dict = self._cfg["viewport"]["draw_style"]
        selected_draw_style_dict = draw_style_dict[self._current_draw_style]
        self._hydra_rend_params = pimg.RenderParams()
        self._hydra_rend_params.cullStyle = pimg.CullStyle.CULL_STYLE_BACK
        self._hydra_rend_params.drawMode = getattr(pimg.DrawMode, selected_draw_style_dict["draw_mode"])
        self._hydra_rend_params.enableLighting = selected_draw_style_dict["enable_lighting"]
        self._hydra_rend_params.enableSampleAlphaToCoverage = True
        self._hydra_rend_params.showProxy = True
        self._hydra_rend_params.highlight = True

    def _update_hydra_time(self):
        """
        Update the time for the Hydra renderer.
        """
        self._hydra_rend_params.frame = self._sm.get_current_time()

    def _calc_smooth_delta(self, mouse_position: tuple) -> tuple:
        """
        Interpolate the mouse position to smooth the delta.
        """
        if not hasattr(self, "_prev_cursor_position"):
            self._prev_cursor_position = mouse_position
        delta_x = mouse_position[0] - self._prev_cursor_position[0]
        delta_y = mouse_position[1] - self._prev_cursor_position[1]
        if not hasattr(self, "_smoothed_delta"):
            self._smoothed_delta = (0.0, 0.0)
        alpha = 0.333
        raw_delta = (delta_x, delta_y)
        smoothed_x = (1 - alpha) * self._smoothed_delta[0] + alpha * raw_delta[0]
        smoothed_y = (1 - alpha) * self._smoothed_delta[1] + alpha * raw_delta[1]
        self._smoothed_delta = (smoothed_x, smoothed_y)
        return (smoothed_x, smoothed_y)
    
    def _process_imgui_input_events(self):
        """
        Process ImGui input events.
        """
        self._orbit = False
        self._zoom = False
        self._pan = False
        self._light_rotate = False
        self._incremental_zoom_in = False
        self._incremental_zoom_out = False
        self._frame_scene = False

        io = imgui.get_io()
        self._key_f = imgui.is_key_pressed(imgui.Key.f)
        self._key_esc = imgui.is_key_pressed(imgui.Key.escape)
        self._key_alt = imgui.is_key_pressed(imgui.Key.left_alt) or imgui.is_key_pressed(imgui.Key.right_alt)
        self._key_shift = imgui.is_key_pressed(imgui.Key.left_shift) or imgui.is_key_pressed(imgui.Key.right_shift)
        self._key_ctrl = imgui.is_key_pressed(imgui.Key.left_ctrl) or imgui.is_key_pressed(imgui.Key.right_ctrl)
        
        self._key_mouse_position = glfw.get_cursor_pos(self._window)
        self._key_mouse_position_delta = self._calc_smooth_delta(self._key_mouse_position)
        self._key_mouse_left = io.mouse_down[0]
        self._key_mouse_right = io.mouse_down[1]
        self._key_mouse_middle = io.mouse_down[2]

        scene_hover = imgui.is_mouse_hovering_rect(self._panel_position, (self._panel_position[0] + self._panel_width, self._panel_position[1] + self._panel_height), clip=False)
        mouse_wheel = io.mouse_wheel

        if scene_hover:
            if mouse_wheel > 0 :
                self._key_scroll_up = True
            elif mouse_wheel < 0:
                self._key_scroll_down = True
            else:
                self._key_scroll_up = False
                self._key_scroll_down = False
        else:
            self._key_scroll_up = False
            self._key_scroll_down = False

        if self._key_alt and self._key_mouse_left:
            self._orbit = True
        elif self._key_alt and self._key_mouse_right:
            self._zoom = True
        elif self._key_alt and self._key_mouse_middle:
            self._pan = True
        elif self._key_shift and self._key_mouse_right:
            self._light_rotate = True
        elif self._key_scroll_up:
            self._incremental_zoom_in = True
        elif self._key_scroll_down:
            self._incremental_zoom_out = True
        elif self._key_f:
            self._frame_scene = True

    def _calc_viewport_selection(self):
        """
        Calculate the selection in the viewport.
        """
        scene_hover = imgui.is_mouse_hovering_rect(
            self._panel_position, (self._panel_position[0] + self._panel_width, self._panel_position[1] + self._panel_height), clip=False)    
        if scene_hover and self._key_mouse_left:
            camera_matrix: pgf.Matrix4d = self._sm.get_camera().GetAttribute("xformOp:transform").Get()
            camera_frustum = pgf.Frustum()
            camera_frustum.SetPositionAndRotationFromMatrix(camera_matrix)
            camera_frustum.SetProjectionType(pgf.Frustum.Perspective)
            
            aspect_ratio = self._panel_width / self._panel_height
            near_z = self._cfg["viewport"]["clipping_range"][0]
            far_z = self._cfg["viewport"]["clipping_range"][1]
            camera_frustum.SetPerspective(self._calc_fov(), aspect_ratio, near_z, far_z)
            
            local_x = self._key_mouse_position[0] - self._panel_position[0]
            local_y = self._key_mouse_position[1] - self._panel_position[1]
            
            mouse_ndc = pgf.Vec2d(
                (2.0 * local_x / self._panel_width) - 1.0, 
                1.0 - (2.0 * local_y / self._panel_height))
            pixel_size = pgf.Vec2d(1.0 / self._panel_width, 1.0 / self._panel_height)
            pixel_frustum = camera_frustum.ComputeNarrowedFrustum(mouse_ndc, pixel_size)
            try:
                intersection = self._hydra.TestIntersection(
                    pixel_frustum.ComputeViewMatrix(),
                    pixel_frustum.ComputeProjectionMatrix(),
                    self._sm.get_root(),
                    self._hydra_rend_params
                )
                intersection_path = intersection[2]
                intersection_prim = self._sm.get_stage().GetPrimAtPath(intersection_path)
            except:
                pass
            if intersection_prim:
                node = self._sm.init_path_node(intersection_prim)
                if node:
                    if not self._key_shift or self._key_ctrl:
                        self._sm.deselect_all()
                    node.set_selected(True)
            else:
                self._sm.deselect_all()

    def _update_viewport_input(self):
        """
        Update the viewport input.
        """
        if self._orbit or self._zoom or self._pan or self._light_rotate:
            delta_x, delta_y = self._key_mouse_position_delta
            if self._orbit:
                self._calc_viewport_orbit(delta_x, delta_y)
            elif self._zoom:
                self._calc_viewport_zoom(delta_x, delta_y)
            elif self._pan:
                self._calc_viewport_pan(delta_x, delta_y)
            elif self._light_rotate:
                self._calc_lighting_rotate(delta_x, delta_y)
        else:
            del(self._smoothed_delta)
        if self._incremental_zoom_in:
            self._calc_incremental_zoom(out=False)
        if self._incremental_zoom_out:
            self._calc_incremental_zoom(out=True)
        if self._frame_scene:
            self.calc_frame_scene() 
        self._calc_viewport_selection()     

    def _calc_fov(self):
        """
        Calculate the field of view for the camera.
        """
        camera = pgeo.Camera(self._sm.get_camera())
        fov = 2 * math.atan(camera.GetVerticalApertureAttr().Get() / (2 * camera.GetFocalLengthAttr().Get()))
        return math.degrees(fov)

    def _calc_lighting_rotate(self, delta_x:float, delta_y:float) -> None:
        """
        Calculate the user rotation of the lights.
        """
        rot_axis = self._sm.get_up_vector()
        rot_y_matrix = pgf.Matrix4d().SetRotate(pgf.Rotation(rot_axis, -delta_x))
        light_transform = self._sm.get_light_xform().GetAttribute("xformOp:transform").Get()
        light_transform = light_transform * rot_y_matrix
        self._sm.get_light_xform().GetAttribute("xformOp:transform").Set(light_transform)

    def _calc_viewport_orbit(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the orbit transformation for the viewport.
        """
        pivot_point = self._sm.create_scene_bounding_box()[0]
        camera_xform: pgf.Matrix4d = self._sm.get_camera().GetAttribute("xformOp:transform").Get()        
        camera_position = camera_xform.ExtractTranslation()
        x_rotation_axis = camera_xform.TransformDir(pgf.Vec3d(1, 0, 0))
        rot_axis = self._sm.get_up_vector()
        rot_matrix_y = pgf.Matrix4d().SetRotate(pgf.Rotation(rot_axis, -delta_x))
        rot_matrix_x = pgf.Matrix4d().SetRotate(pgf.Rotation(x_rotation_axis, -delta_y))
        world_rotation: pgf.Matrix4d = (rot_matrix_x * rot_matrix_y)
        relative_pos: pgf.Vec3d = camera_position - pivot_point
        new_position = world_rotation.Transform(relative_pos) + pivot_point
        new_transform: pgf.Matrix4d =  camera_xform * world_rotation
        new_transform.SetTranslateOnly(new_position)
        self._sm.get_camera().GetAttribute("xformOp:transform").Set(new_transform)

    def _calc_viewport_zoom(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the zoom transformation for the viewport.
        """
        transform_factor = self._scene_bbox_size.GetLength() / 100
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, -delta_x * transform_factor))
        camera_xform = self._sm.get_camera().GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._sm.get_camera().GetAttribute("xformOp:transform").Set(transform)

    def _calc_incremental_zoom(self, out=True) -> None:
        """
        Calculate the incremental zoom transformation for the viewport.
        """
        factor = self._scene_bbox_size.GetLength() / 5
        zoom_factor = factor if out else -factor
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, zoom_factor))
        camera_xform = self._sm.get_camera().GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._sm.get_camera().GetAttribute("xformOp:transform").Set(transform)

    def _calc_viewport_pan(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the pan transformation for the viewport.
        """
        transform_factor = self._scene_bbox_size.GetLength() / 150
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(-delta_x * transform_factor, delta_y * transform_factor, 0))
        camera_xform = self._sm.get_camera().GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._sm.get_camera().GetAttribute("xformOp:transform").Set(transform)

    def _create_c_render_dict(self) -> dict:
        """
        Create a dictionary for Hydra.
        """
        render_dict = {}
        render_dict["draw_dict"] = self._create_c_opengl_draw_dict()
        display_size = (int(imgui.get_io().display_size[0]), int(imgui.get_io().display_size[1]))
        render_dict["display_size"] = pgf.Vec2i(display_size)
        render_dict["viewport_position"] = pgf.Vec2i(self._panel_position[0], self._panel_position[1])
        render_dict["viewport_size"] = pgf.Vec2i(self._panel_width, self._panel_height)
        render_dict["bone_list"] = self._sm.get_data_node_list_by_type(cbase.Bone)
        render_dict["light_dict"] = self._sm.create_light_dict()
        render_dict["camera_dict"] = self._sm.create_camera_dict()
        render_dict["root"] = self._sm.get_stage().GetPseudoRoot()
        return render_dict 

    def _create_c_opengl_draw_dict(self) -> dict:
        """
        Create a dictionary for OpenGL drawing.
        """
        camera_matrix = self._sm.get_camera().GetAttribute("xformOp:transform").Get()
        draw_dict = {}
        draw_dict["camera_matrix"] = camera_matrix
        draw_dict["up_matrix"] = self._sm.get_up_axis_matrix()
        draw_dict["panel_width"] = self._panel_width
        draw_dict["panel_height"] = self._panel_height
        draw_dict["hydra_x_min"] = self._hydra_x_min
        draw_dict["hydra_y_min"] = self._hydra_y_min
        draw_dict["fov"] = self._calc_fov()
        draw_dict["near_z"] = self._cfg["viewport"]["clipping_range"][0]
        draw_dict["far_z"] = self._cfg["viewport"]["clipping_range"][1]
        draw_dict["scene_bbox_size"] = self._scene_bbox_size
        draw_dict["grid_density"] = self._cfg["viewport"]["grid_density"]
        draw_dict["grid_color"] = self._cfg["viewport"]["grid_color"]
        draw_dict["up_axis"] = self._sm.get_up_axis()
        return draw_dict 

    def _update_selected_list(self) -> None:
        """
        Update the selected list for the viewport.
        """
        selected_list: list[pusd.Prim] = []
        path_node_list = self._sm.get_path_node_list()
        for path_node in path_node_list:
            if path_node.get_selected():
                selected_list.append(path_node.get_path())
        self._hydra.SetSelected(selected_list)

    def _hydra_render_loop(self) -> None:
        """
        Render loop for the Hydra renderer.
        """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        display_size = glfw.get_window_size(self._window)
        self._hydra_x_min = int(self._panel_position[0])
        self._hydra_y_min = int(display_size[1] - self._panel_position[1] - self._panel_height)
        self._hydra.SetRenderViewport((self._hydra_x_min, self._hydra_y_min, self._panel_width, self._panel_height))
        self._hydra.SetRenderBufferSize(pgf.Vec2i(int(self._panel_width), int(self._panel_height))) 
        self._update_hydra_time()
        self._update_viewport_input()
        self._update_selected_list()
        if self._user_cfg["show"]["mesh"]:
            self._hydra.Render(self._sm.get_root(), self._hydra_rend_params)
        if self._user_cfg["show"]["grid"]:
            cdraw.c_draw_opengl_grid(self._create_c_opengl_draw_dict())
        if self._user_cfg["show"]["gizmo"]:
            cdraw.c_draw_opengl_gizmo(self._create_c_opengl_draw_dict())    
        if self._user_cfg["show"]["lights"]:
            cdraw.c_draw_opengl_light(self._create_c_opengl_draw_dict(), self._sm.create_light_dict())  
        if self._user_cfg["show"]["camera"]:
            cdraw.c_draw_opengl_camera(self._create_c_opengl_draw_dict(), self._sm.create_camera_dict())                      
        if self._user_cfg["show"]["bones"]:
            cdraw.c_draw_opengl_bone(self._sm.get_data_node_list_by_type(cbase.Bone), self._create_c_opengl_draw_dict())
        if self._user_cfg["show"]["xray"]:
            cdraw.c_draw_opengl_bone_xray(self._sm.get_data_node_list_by_type(cbase.Bone), self._create_c_opengl_draw_dict())

    def _options_backdrop(self) -> None:
        """
        Draw the options backdrop.
        """
        options_min = (self._panel_position[0] + self._panel_width - 60, self._panel_position[1] + 2)
        options_max = (options_min[0] + 55, options_min[1] + 148)
        draw_list = imgui.get_window_draw_list()
        draw_list.add_rect_filled(options_min, options_max, imgui.get_color_u32((0.125, 0.125, 0.125, 0.75)), 2)
        draw_list.add_rect(options_min, options_max, imgui.get_color_u32((0, 0, 0, 0.75)), 2)

        setting_min = (self._panel_position[0] + 5, self._panel_position[1] + 5)
        setting_max = (setting_min[0] + 40, setting_min[1] + 28)
        draw_list.add_rect_filled(setting_min, setting_max, imgui.get_color_u32((0.125, 0.125, 0.125, 0.75)), 2)
        draw_list.add_rect(setting_min, setting_max, imgui.get_color_u32((0, 0, 0, 0.75)), 2)
        
    def _draw_up_axis_dropdown(self):
        """
        Draw the up axis dropdown.
        """
        imgui.set_cursor_pos_x(self._panel_width - 60)
        imgui.push_font(self._frame._font_small)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 3)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 0)
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (5, 5))
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (0, 0))

        imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg_active, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg_hovered, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.check_mark, (0.5, 0.5, 0.5, 1.0))

        imgui.push_item_width(30)

        if imgui.begin_combo("##up_axis", "", imgui.ComboFlags_.height_largest):    
            if self._stage:      
                for axis in ["Y", "Z"]:
                    selected, clicked = imgui.checkbox(f"  {axis}  ", self._sm.get_up_axis() == axis)
                    if selected:
                        self._sm.set_up_axis(axis)
                        self.calc_frame_scene(reset=True)
                        self._sm.calc_light_xform_default()
            imgui.end_combo()
        imgui.same_line()
        icon = cstat.Icon.ICON_VIEWPORT_AXIS_Y if self._sm.get_up_axis() == "Y" else cstat.Icon.ICON_VIEWPORT_AXIS_Z
        axis_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, icon, (15, 15))
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 2)
        imgui.image(axis_icon_id, (15, 15))
        imgui.pop_style_var(4)
        imgui.pop_style_color(7)
        imgui.pop_font()

    def _draw_light_dropdown(self):
        """
        Draw the light selection dropdown.
        """
        imgui.set_cursor_pos_x(self._panel_width - 60)
        imgui.push_font(self._frame._font_small)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 3)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 0)
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (10, 5))
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (0, 0))

        imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg_active, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg_hovered, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.check_mark, (0.5, 0.5, 0.5, 1.0))

        imgui.push_item_width(30)

        if imgui.begin_combo("##light", "", imgui.ComboFlags_.height_largest):
            if self._stage:       
                selected, clicked = imgui.checkbox("Default", self._default_light)
                if selected:
                    self._default_light = self._sm.enable_default_lights()
                    self._scene_light = self._sm.disable_scene_lights()
                selected, clicked = imgui.checkbox("Scene", self._scene_light)
                if selected:
                    self._scene_light = self._sm.enable_scene_lights()
                    self._default_light = self._sm.disable_default_lights()
            imgui.end_combo()
        imgui.same_line()
        icon = cstat.Icon.ICON_VIEWPORT_LIGHT
        light_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, icon, (15, 15))
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 2)
        imgui.image(light_icon_id, (15, 15))
        imgui.pop_style_var(4)
        imgui.pop_style_color(7)
        imgui.pop_font()

    def _draw_camera_dropdown(self):
        """
        Draw the camera selection dropdown.
        """
        imgui.set_cursor_pos_x(self._panel_width - 60)
        imgui.push_font(self._frame._font_small)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 3)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 0)
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (10, 5))
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (0, 0))

        imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg_active, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg_hovered, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.check_mark, (0.5, 0.5, 0.5, 1.0))

        imgui.push_item_width(30)

        if imgui.begin_combo("##camera", "", imgui.ComboFlags_.height_largest):
            if self._stage:       
                selected, clicked = imgui.checkbox("Default", self._default_light)
                if selected:
                    pass
            imgui.end_combo()
        imgui.same_line()
        icon = cstat.Icon.ICON_VIEWPORT_CAMERA
        camera_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, icon, (15, 15))
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 2)
        imgui.image(camera_icon_id, (15, 15))
        imgui.pop_style_var(4)
        imgui.pop_style_color(7)
        imgui.pop_font()

    def _draw_user_settings_dropdown(self):
        """
        Draw the camera selection dropdown.
        """
        imgui.set_cursor_pos_x(10)
        imgui.set_cursor_pos_y(10)
        imgui.push_font(self._frame._font_small)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 3)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 0)
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (10, 5))
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (0, 0))

        imgui.push_style_color(imgui.Col_.button, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.button_active, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.button_hovered, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg_active, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.frame_bg_hovered, (0, 0, 0, 0))
        imgui.push_style_color(imgui.Col_.check_mark, (0.5, 0.5, 0.5, 1.0))


        icon = cstat.Icon.ICON_VIEWPORT_SETTINGS
        settings_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, icon, (15, 15))
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 2)
        imgui.image(settings_icon_id, (15, 15))
        
        imgui.same_line()
        imgui.push_item_width(30)
        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() - 8)
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        if imgui.begin_combo("##user_settings", "", imgui.ComboFlags_.height_largest):
            for vis_setting in self._user_cfg["show"]:
                vis_setting: str
                selected, clicked = imgui.checkbox(f" {vis_setting.title()}", self._user_cfg["show"][vis_setting])
                if selected:
                    if vis_setting == "bones":
                        self._user_cfg["show"]["bones"] = not self._user_cfg["show"]["bones"]
                        if self._user_cfg["show"]["bones"]:
                            self._user_cfg["show"]["xray"] = False
                    elif vis_setting == "xray":
                        self._user_cfg["show"]["xray"] = not self._user_cfg["show"]["xray"]
                        if self._user_cfg["show"]["bones"]:
                            self._user_cfg["show"]["bones"] = False
                    else:
                        self._user_cfg["show"][vis_setting] = not self._user_cfg["show"][vis_setting]     
            imgui.end_combo()

        imgui.pop_style_var(4)
        imgui.pop_style_color(7)
        imgui.pop_font()

    def _draw_draw_style_radio(self):
        """
        Draw the render modes for the viewport.
        """
        imgui.set_cursor_pos_x(self._panel_width - 50)
        imgui.push_font(self._frame._font_tiny)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 3)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 1.0)
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (3, 3))
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (5, 0))

        imgui.push_style_color(imgui.Col_.frame_bg, (0.2, 0.2, 0.2, 0.5))
        imgui.push_style_color(imgui.Col_.frame_bg_active, (0.2, 0.2, 0.2, 0.75))
        imgui.push_style_color(imgui.Col_.frame_bg_hovered, (0.2, 0.2, 0.2, 1))
        imgui.push_style_color(imgui.Col_.check_mark, (0.65, 0.65, 0.65, 1.0))

        imgui.set_cursor_pos((self._panel_width - 50, 10))
        for index, style_key in enumerate(self._draw_style_dict):
            imgui.set_cursor_pos_x(self._panel_width - 50)
            style_dict = self._draw_style_dict[style_key]
            icon = style_dict["icon"]
            current = self._current_draw_style == style_key
            imgui.push_id(index)
            if imgui.radio_button("", current):
                self._current_draw_style = style_key
                self._update_hydra_render_params()
            imgui.pop_id()
            imgui.same_line()
            icon_size = (16, 16)
            icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, getattr(cstat.Icon, icon), icon_size)
            imgui.image(icon_id, icon_size)
            imgui.new_line()
        imgui.pop_style_var(4)
        imgui.pop_style_color(4)
        imgui.pop_font()

    def calc_frame_scene(self, reset=False) -> None:
        """
        Frame the scene in the viewport.
        """
        if reset:
            self._sm.get_camera().GetAttribute("xformOp:transform").Set(pgf.Matrix4d())
        bbox_center, bbox_size = self._sm.create_scene_bounding_box()
        bbox_size_factor = bbox_size.GetLength()
        if bbox_size_factor <= 0:
            bbox_size_factor = 1.0
        distance_factor = 2.0
        distance = bbox_size_factor * distance_factor
        world_up = self._sm.get_up_vector()
        camera_position = self._sm.get_camera().GetAttribute("xformOp:transform").Get().ExtractTranslation()
        if camera_position == pgf.Vec3d(0, 0, 0):
            camera_position = pgf.Vec3d(1000, 1000, 1000)
        current_distance = (bbox_center - camera_position).GetLength()
        target_distance = distance / current_distance
        transform = cutils.calc_look_at_neg_z(camera_position * target_distance, bbox_center, world_up, flip_forward=True)
        self._sm.get_camera().GetAttribute("xformOp:transform").Set(transform)

    def draw(self) -> None:
        """
        Draw the outliner panel.
        """
        self._process_imgui_input_events()
        self._prev_cursor_position = self._key_mouse_position  
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        if self._stage:
            self._hydra_render_loop()
        self._options_backdrop()
        self._draw_user_settings_dropdown()
        self._draw_draw_style_radio()
        self._draw_up_axis_dropdown()
        self._draw_light_dropdown()
        self._draw_camera_dropdown()

    def get_user_cfg(self) -> dict:
        """
        Get the user configuration for the viewport.
        """
        return self._user_cfg

    def update_usd(self):
        super().update_usd()
        self._init_hydra()

