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
        super().__init__("viewport", frame)
        self._window = frame.get_window()
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

    def _init_viewport_draw_styles(self):
        """
        Initialize viewport draw styles.
        """
        self._draw_style_dict = self._cfg["viewport"]["draw_style"]
        self._current_draw_style = self._cfg["viewport"]["default_draw_style"]

    def _mouse_scroll_callback(self, window, x_offset, y_offset):
        """
        Mouse scroll callback for GLFW window.
        """
        if y_offset > 0:
            self._key_scroll_up = True
        elif y_offset < 0:
            self._key_scroll_down  = True

    def _init_hydra(self):
        """
        Initialize Hydra renderer.
        """
        self._hydra = self._scene_manager.get_hydra()
        self._scene_manager.set_viewport(self)
        render_plugins = self._hydra.GetRendererPlugins()
        if render_plugins:
            glfw.set_scroll_callback(self._window, self._mouse_scroll_callback)
            self._hydra.SetRendererPlugin(render_plugins[0])
            self._scene_bbox_center, self._scene_bbox_size = self._scene_manager.create_scene_bounding_box()
            cdraw.c_init_glad()
            self._scene_manager.set_default_light_xform()
            self._scene_manager.disable_scene_lights()
            self._scene_manager.enable_default_lights()
            self._scene_manager.calc_frame_scene()
        else:
            raise RuntimeError("No renderer plugins available")

    def _update_hydra_render_params(self):
        """
        Update Hydra render parameters.
        """
        draw_style_dict = self._cfg["viewport"]["draw_style"]
        selected_draw_style_dict = draw_style_dict[self._current_draw_style]
        self._hydra_rend_params = pimg.RenderParams()
        self._hydra_rend_params.drawMode = getattr(pimg.DrawMode, selected_draw_style_dict["draw_mode"])
        self._hydra_rend_params.enableLighting = selected_draw_style_dict["enable_lighting"]
        self._hydra_rend_params.enableSampleAlphaToCoverage = True

    def _update_hydra_time(self):
        self._hydra_rend_params.frame = self._scene_manager.get_current_time()


    #CONVERT TO IMGUI
    def _process_glfw_events(self):
        """
        Process GLFW events.
        """
        self._orbit = False
        self._zoom = False
        self._pan = False
        self._light_rotate = False
        self._incremental_zoom_in = False
        self._incremental_zoom_out = False
        self._frame_scene = False

        self._key_f = glfw.get_key(self._window, glfw.KEY_F)
        self._key_esc = glfw.get_key(self._window, glfw.KEY_ESCAPE)
        self._key_alt = glfw.get_key(self._window, glfw.KEY_LEFT_ALT) or glfw.get_key(self._window, glfw.KEY_RIGHT_ALT)
        self._key_shift = glfw.get_key(self._window, glfw.KEY_LEFT_SHIFT) or glfw.get_key(self._window, glfw.KEY_RIGHT_SHIFT)
        
        self._key_mouse_position = glfw.get_cursor_pos(self._window)
        self._key_mouse_left = glfw.get_mouse_button(self._window, glfw.MOUSE_BUTTON_LEFT)
        self._key_mouse_right = glfw.get_mouse_button(self._window, glfw.MOUSE_BUTTON_RIGHT)
        self._key_mouse_middle = glfw.get_mouse_button(self._window, glfw.MOUSE_BUTTON_MIDDLE)

        if self._key_alt == glfw.PRESS and self._key_mouse_left == glfw.PRESS:
            self._orbit = True
        elif self._key_alt == glfw.PRESS and self._key_mouse_right == glfw.PRESS:
            self._zoom = True
        elif self._key_alt == glfw.PRESS and self._key_mouse_middle == glfw.PRESS:
            self._pan = True
        elif self._key_shift == glfw.PRESS and self._key_mouse_right == glfw.PRESS:
            self._light_rotate = True
        elif self._key_scroll_up:
            self._incremental_zoom_in = True
        elif self._key_scroll_down:
            self._incremental_zoom_out = True
        elif self._key_f == glfw.PRESS:
            self._frame_scene = True
        self._key_scroll_up = False
        self._key_scroll_down = False

    def _create_camera_info_dict(self):
        """
        Create a list of lights in the scene.
        """
        if not self._stage:
            return []
        camera_dict: dict = {}
        prim_list = self._stage.Traverse()
        for prim in prim_list:
            if prim.IsA(pgeo.Camera):
                if prim.GetAttribute("visibility").Get() != pgeo.Tokens.invisible:
                    xformable = pgeo.Xformable(prim)
                    world_transform = xformable.ComputeLocalToWorldTransform(pusd.TimeCode.Default())
                    world_transform_orthonormalized = pgf.Matrix4d(world_transform).GetOrthonormalized()
                    world_rotation = world_transform_orthonormalized.ExtractRotation()
                    world_translate = world_transform.ExtractTranslation()
                    world_transform = pgf.Matrix4d().SetTranslateOnly(world_translate).SetRotateOnly(world_rotation)
                    camera_dict[str(prim.GetName())] = {
                        "prim": prim,
                        "matrix": world_transform,
                        "visibility": True if prim.GetAttribute("visibility").Get() == pgeo.Tokens.inherited else False,
                    }
        return camera_dict

    def _create_light_info_dict(self):
        """
        Create a list of lights in the scene.
        """
        if not self._stage:
            return {}
        light_dict: dict = {}
        prim_list = self._stage.Traverse()
        for prim in prim_list:
            if prim.HasAPI(plux.LightAPI):
                xformable = pgeo.Xformable(prim)
                world_transform = xformable.ComputeLocalToWorldTransform(pusd.TimeCode.Default())
                world_transform_orthonormalized = pgf.Matrix4d(world_transform).GetOrthonormalized()
                world_rotation = world_transform_orthonormalized.ExtractRotation()
                world_translate = world_transform.ExtractTranslation()
                world_transform = pgf.Matrix4d().SetTranslateOnly(world_translate).SetRotateOnly(world_rotation)
                light_dict[str(prim.GetName())] = {
                    "prim": prim,
                    "matrix": world_transform,
                    "color": prim.GetAttribute("inputs:color").Get(),
                    "visibility": True if prim.GetAttribute("visibility").Get() == pgeo.Tokens.inherited else False,
                }
        return light_dict

    def _update_viewport_input(self):
        """
        Update the viewport scene.
        """
        cursor_pos = glfw.get_cursor_pos(self._window)
        if self._orbit or self._zoom or self._pan or self._light_rotate:
            cursor_pos = glfw.get_cursor_pos(self._window)
            delta_x = cursor_pos[0] - self._prev_cursor_pos[0]
            delta_y = cursor_pos[1] - self._prev_cursor_pos[1]
            if self._orbit:
                self._calc_viewport_orbit(delta_x, delta_y)
            elif self._zoom:
                self._calc_viewport_zoom(delta_x, delta_y)
            elif self._pan:
                self._calc_viewport_pan(delta_x, delta_y)
            elif self._light_rotate:
                self._calc_lighting_rotate(delta_x, delta_y)
        if self._incremental_zoom_in:
            self._calc_incremental_zoom(out=False)
        if self._incremental_zoom_out:
            self._calc_incremental_zoom(out=True)
        if self._frame_scene:
            self._scene_manager.calc_frame_scene()
        self._prev_cursor_pos = cursor_pos

    def _calc_lighting_rotate(self, delta_x:float, delta_y:float) -> None:
        """
        Calculate the user rotation of the lights.
        """
        rot_axis = pgf.Vec3d(0, 1, 0) if self._scene_manager.get_up_axis() == "Y" else pgf.Vec3d(0, 0, 1)
        rot_y_matrix = pgf.Matrix4d().SetRotate(pgf.Rotation(rot_axis, -delta_x * 0.5))
        light_transform = self._scene_manager.get_light_xform().GetAttribute("xformOp:transform").Get()
        light_transform = light_transform * rot_y_matrix
        self._scene_manager.get_light_xform().GetAttribute("xformOp:transform").Set(light_transform)

    def _calc_fov(self):
        """
        Calculate the field of view for the camera.
        """
        camera = pgeo.Camera(self._scene_manager.get_camera())
        fov = 2 * math.atan(camera.GetVerticalApertureAttr().Get() / (2 * camera.GetFocalLengthAttr().Get()))
        return math.degrees(fov)

    def _calc_viewport_orbit(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the orbit transformation for the viewport.
        """
        pivot_point = self._scene_bbox_center
        camera_xform: pgf.Matrix4d = self._scene_manager.get_camera().GetAttribute("xformOp:transform").Get()        
        camera_position = camera_xform.ExtractTranslation()
        x_rotation_axis = camera_xform.TransformDir(pgf.Vec3d(1, 0, 0))
        rot_axis = pgf.Vec3d(0, 1, 0) if self._scene_manager.get_up_axis() == "Y" else pgf.Vec3d(0, 0, 1)
        rot_matrix_y = pgf.Matrix4d().SetRotate(pgf.Rotation(rot_axis, -delta_x * 0.1))
        rot_matrix_x = pgf.Matrix4d().SetRotate(pgf.Rotation(x_rotation_axis, -delta_y * 0.1))
        world_rotation: pgf.Matrix4d = (rot_matrix_x * rot_matrix_y)
        relative_pos: pgf.Vec3d = camera_position - pivot_point
        new_position = world_rotation.Transform(relative_pos) + pivot_point
        new_transform: pgf.Matrix4d =  camera_xform * world_rotation
        new_transform.SetTranslateOnly(new_position)
        self._scene_manager.get_camera().GetAttribute("xformOp:transform").Set(new_transform)

    def _calc_viewport_zoom(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the zoom transformation for the viewport.
        """
        transform_factor = self._scene_bbox_size.GetLength() / 1000.0
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, -delta_x * transform_factor))
        camera_xform = self._scene_manager.get_camera().GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._scene_manager.get_camera().GetAttribute("xformOp:transform").Set(transform)

    def _calc_incremental_zoom(self, out=True) -> None:
        """
        Calculate the incremental zoom transformation for the viewport.
        """
        factor = self._scene_bbox_size.GetLength() / 10.0
        zoom_factor = factor if out else -factor
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, zoom_factor))
        camera_xform = self._scene_manager.get_camera().GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._scene_manager.get_camera().GetAttribute("xformOp:transform").Set(transform)

    def _calc_viewport_pan(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the pan transformation for the viewport.
        """
        transform_factor = self._scene_bbox_size.GetLength() / 1000.0
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(-delta_x * transform_factor, delta_y * transform_factor, 0))
        camera_xform = self._scene_manager.get_camera().GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._scene_manager.get_camera().GetAttribute("xformOp:transform").Set(transform)

    def _create_c_opengl_draw_dict(self) -> dict:
        """
        Create a dictionary for OpenGL drawing.
        """
        camera_matrix = self._scene_manager.get_camera().GetAttribute("xformOp:transform").Get()
        draw_dict = {}
        draw_dict["camera_matrix"] = camera_matrix
        draw_dict["up_matrix"] = self._scene_manager.get_up_axis_matrix()
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
        draw_dict["up_axis"] = self._scene_manager.get_up_axis()
        return draw_dict 
            
    def _hydra_render_loop(self) -> None:
        """
        Render loop for the Hydra renderer.
        """
        try:
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            display_size = glfw.get_window_size(self._window)
            self._hydra_x_min = int(self._panel_position[0])
            self._hydra_y_min = int(display_size[1] - self._panel_position[1] - self._panel_height)
            self._hydra.SetRenderViewport((self._hydra_x_min, self._hydra_y_min, self._panel_width, self._panel_height))
            self._hydra.SetRenderBufferSize(pgf.Vec2i(int(self._panel_width), int(self._panel_height))) 
            self._update_hydra_time()
            self._update_viewport_input()
            if self._user_cfg["show"]["mesh"]:
                self._hydra.Render(self._stage.GetPseudoRoot(), self._hydra_rend_params)
            if self._user_cfg["show"]["grid"]:
                cdraw.c_draw_opengl_grid(self._create_c_opengl_draw_dict())
            if self._user_cfg["show"]["gizmo"]:
                cdraw.c_draw_opengl_gizmo(self._create_c_opengl_draw_dict())    
            if self._user_cfg["show"]["lights"]:
                cdraw.c_draw_opengl_light(self._create_c_opengl_draw_dict(), self._create_light_info_dict())  
            if self._user_cfg["show"]["camera"]:
                cdraw.c_draw_opengl_camera(self._create_c_opengl_draw_dict(), self._create_camera_info_dict())                      
            if self._user_cfg["show"]["bones"]:
                cdraw.c_draw_opengl_bone(self._scene_manager.get_data_node_list_by_type(cbase.Bone), self._create_c_opengl_draw_dict())
            if self._user_cfg["show"]["xray"]:
                cdraw.c_draw_opengl_bone_xray(self._scene_manager.get_data_node_list_by_type(cbase.Bone), self._create_c_opengl_draw_dict())
        except Exception as e:
            print(e)

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
                    selected, clicked = imgui.checkbox(f"  {axis}  ", self._scene_manager.get_up_axis() == axis)
                    if selected:
                        self._scene_manager.set_up_axis(axis)
            imgui.end_combo()
        imgui.same_line()
        icon = cstat.Icon.ICON_VIEWPORT_AXIS_Y if self._scene_manager.get_up_axis() == "Y" else cstat.Icon.ICON_VIEWPORT_AXIS_Z
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
                    self._default_light = self._scene_manager.enable_default_lights()
                    self._scene_light = self._scene_manager.disable_scene_lights()
                selected, clicked = imgui.checkbox("Scene", self._scene_light)
                if selected:
                    self._scene_light = self._scene_manager.enable_scene_lights()
                    self._default_light = self._scene_manager.disable_default_lights()
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
                pimg.DrawMode.DRAW_WIREFRAME_ON_SURFACE
            imgui.pop_id()
            imgui.same_line()
            icon_size = (16, 16)
            icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, getattr(cstat.Icon, icon), icon_size)
            imgui.image(icon_id, icon_size)
            imgui.new_line()

        imgui.pop_style_var(4)
        imgui.pop_style_color(4)
        imgui.pop_font()

    def draw(self) -> None:
        """
        Draw the outliner panel.
        """ 
        self._process_glfw_events()
        if self._stage:
            self._hydra_render_loop()
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        self._options_backdrop()
        self._draw_user_settings_dropdown()
        self._draw_draw_style_radio()
        self._draw_up_axis_dropdown()
        self._draw_light_dropdown()
        self._draw_camera_dropdown()
    
    def update_usd(self):
        super().update_usd()
        self._init_hydra()
