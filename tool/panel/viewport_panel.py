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
import core.c_draw_opengl as cdraw

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
    _key_scroll_up = False
    _key_scroll_down = False
    _current_draw_style = None
    def __init__(self, frame: cbase.Frame):
        super().__init__("viewport", frame)
        self._window = frame.get_window()
        self._init_viewport_draw_styles()
        self._update_hydra_render_params()
        self._calc_up_axis()

    def _init_config(self):
        super()._init_config()
        self._up_axis = self._cfg["viewport"]["up_axis"]
        self._user_cfg = {}
        self._user_cfg["show"] = {}
        self._user_cfg["show"]["grid"] = True
        self._user_cfg["show"]["gizmo"] = True
        self._user_cfg["show"]["lights"] = True
        self._user_cfg["show"]["camera"] = True
        self._user_cfg["show"]["bones"] = True

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
        self._hydra = pimg.Engine()
        render_plugins = self._hydra.GetRendererPlugins()
        if render_plugins:
            glfw.set_scroll_callback(self._window, self._mouse_scroll_callback)
            self._hydra.SetRendererPlugin(render_plugins[0])
            self._scene_bbox_center, self._scene_bbox_size = self._create_scene_bounding_box()
            self._camera = self._create_camera()
            self._hydra.SetCameraPath(self._camera.GetPath())
            cdraw.c_init_glad()
            self._init_opengl_settings()
            self._create_lighting()
            self._disable_scene_lights()
            self._enable_default_lights()
            self._calc_frame_scene()
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

    def _calc_up_axis(self):
        """
        Initialize up axis matrix.
        """
        if self._up_axis == "Y":
            self._up_axis_matrix = pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(1, 0, 0), 0))
        elif self._up_axis == "Z":
            self._up_axis_matrix = pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(1, 0, 0), -90))
        else:
            raise ValueError("Invalid up axis specified")

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

    def _create_camera(self):
        """
        Create a camera with default attributes and a transformation matrix.
        """
        clipping_range = self._cfg["viewport"]["clipping_range"]
        focal_length = self._cfg["viewport"]["focal_length"]
        camera = pgeo.Camera.Define(self._stage, "/OrbitCamera")
        camera.CreateFocalLengthAttr(focal_length)
        camera.CreateHorizontalApertureAttr(24.0)
        camera.CreateVerticalApertureAttr(18.0)
        camera.CreateHorizontalApertureOffsetAttr(0.0)
        camera.CreateVerticalApertureOffsetAttr(0.0)
        camera.CreateClippingRangeAttr(pgf.Vec2f(clipping_range))
        xform_attr = camera.GetPrim().CreateAttribute("xformOp:transform", psdf.ValueTypeNames.Matrix4d)
        xform_attr.Set(pgf.Matrix4d().SetIdentity())
        xform_op_order = camera.GetPrim().GetAttribute("xformOpOrder")
        if not xform_op_order:
           xform_op_order = camera.GetPrim().CreateAttribute("xformOpOrder", psdf.ValueTypeNames.TokenArray)
        xform_op_order.Set(["xformOp:transform"])
        return camera.GetPrim()

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
                    camera_dict[prim] = {
                        "transform": world_transform,
                        "visibility": prim.GetAttribute("visibility").Get()
                    }
        return camera_dict

    def _create_light_info_dict(self):
        """
        Create a list of lights in the scene.
        """
        if not self._stage:
            return []
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
                light_dict[prim] = {
                    "transform": world_transform,
                    "color": prim.GetAttribute("inputs:color").Get(),
                    "visibility": prim.GetAttribute("visibility").Get(),
                }
        return light_dict

    def _disable_scene_lights(self):
        """
        Disable all lights in the scene.
        """
        self._scene_light = False
        self._light_disable_list: list[pusd.Prim] = []
        prim_list = self._stage.Traverse()
        for prim in prim_list:
            if prim.HasAPI(plux.LightAPI) and prim not in [self._light_key, self._light_fill, self._light_back]:
                if prim.GetAttribute("visibility").Get() != pgeo.Tokens.invisible:
                    self._light_disable_list.append(prim)
                    prim.GetAttribute("visibility").Set(pgeo.Tokens.invisible)

    def _enable_scene_lights(self):
        """
        Enable all lights in the scene.
        """
        self._scene_light = True
        for light in self._light_disable_list:
            light.GetAttribute("visibility").Set(pgeo.Tokens.inherited)
        self._light_disable_list = []

    def _disable_default_lights(self):
        """
        Disable all default lights in the scene.
        """
        self._default_light = False
        for light in [self._light_key, self._light_fill, self._light_back]:
            light.GetAttribute("visibility").Set(pgeo.Tokens.invisible)

    def _enable_default_lights(self):
        """
        Enable all default lights in the scene.
        """
        self._default_light = True
        for light in [self._light_key, self._light_fill, self._light_back]:
            light.GetAttribute("visibility").Set(pgeo.Tokens.inherited)

    def _calc_light_transform(self, light_position, target_position):
        """
        Calculate the light transform matrix.
        """
        world_up = pgf.Vec3d(0, 1, 0) if self._up_axis == "Y" else pgf.Vec3d(0, 0, 1)
        light_matrix = cutils.calc_look_at(light_position, target_position, world_up, flip_forward=True)
        return light_matrix

    def _create_lighting(self):
        """
        Create default 3-point lighting.
        """
        light_xform = pgeo.Xform.Define(self._stage, "/LightNull")
        light_xform.GetPrim().CreateAttribute("xformOp:transform", psdf.ValueTypeNames.Matrix4d)
        light_xform.GetPrim().GetAttribute("xformOp:transform").Set(pgf.Matrix4d().SetIdentity())
        lights_xform_op_order = light_xform.GetPrim().CreateAttribute("xformOpOrder", psdf.ValueTypeNames.TokenArray)
        lights_xform_op_order.Set(["xformOp:transform"])
        self._light_xform = light_xform.GetPrim()
        
        zero_position = pgf.Vec3d(0.0, 0.0, 0.0)
        distance = 100
        key_position = pgf.Vec3d(5.0, 5.0, 5.0).GetNormalized() * distance
        fill_position = pgf.Vec3d(-5.0, 3.0, 5.0).GetNormalized() * distance
        back_position = pgf.Vec3d(0.0, 5.0, -5.0).GetNormalized() * distance

        key_transform = self._calc_light_transform(key_position, zero_position)
        fill_transform = self._calc_light_transform(fill_position, zero_position)
        back_transform = self._calc_light_transform(back_position, zero_position)

        self._light_key = self._create_light("/LightNull/KeyLight", (1.0, 0.95, 0.9), 15.0, key_transform)
        self._light_fill = self._create_light("/LightNull/FillLight", (0.9, 0.9, 1.0), 8.0, fill_transform)
        self._light_back = self._create_light("/LightNull/BackLight", (1.0, 1.0, 1.0), 10.0, back_transform)

    def _create_light(self, path: str, color: tuple, intensity: float, transform: pgf.Matrix4d) -> pusd.Prim:
        """
        Create a light for the scene with a specified intensity.
        """
        light = plux.DistantLight.Define(self._stage, path)
        light.CreateIntensityAttr(intensity)
        light.CreateColorAttr(pgf.Vec3f(*color))
        light.CreateAngleAttr(35.0)
        light.GetPrim().CreateAttribute("xformOp:transform", psdf.ValueTypeNames.Matrix4d)
        light.GetPrim().GetAttribute("xformOp:transform").Set(transform)
        light_xform_op_order = light.GetPrim().CreateAttribute("xformOpOrder", psdf.ValueTypeNames.TokenArray)
        light_xform_op_order.Set(["xformOp:transform"])
        light.GetPrim().GetAttribute("visibility").Set(pgeo.Tokens.inherited)
        return light.GetPrim()

    def _calc_lighting_rotate(self, delta_x:float, delta_y:float) -> None:
        """
        Calculate the user rotation of the lights.
        """
        rot_axis = pgf.Vec3d(0, 1, 0) if self._up_axis == "Y" else pgf.Vec3d(0, 0, 1)
        rot_y_matrix = pgf.Matrix4d().SetRotate(pgf.Rotation(rot_axis, -delta_x * 0.5))
        light_transform = self._light_xform.GetAttribute("xformOp:transform").Get()
        light_transform = light_transform * rot_y_matrix
        self._light_xform.GetAttribute("xformOp:transform").Set(light_transform)

    def _calc_fov(self):
        """
        Calculate the field of view for the camera.
        """
        camera = pgeo.Camera(self._camera)
        fov = 2 * math.atan(camera.GetVerticalApertureAttr().Get() / (2 * camera.GetFocalLengthAttr().Get()))
        return math.degrees(fov)

    def _create_scene_bounding_box(self):
        """
        Create a bounding box for the scene.
        """
        bbox_cache = pgeo.BBoxCache(pusd.TimeCode.Default(), includedPurposes=[pgeo.Tokens.default_, pgeo.Tokens.render]) ########################
        bbox = bbox_cache.ComputeWorldBound(self._stage.GetPseudoRoot())
        bbox_min = bbox.GetRange().GetMin()
        bbox_max = bbox.GetRange().GetMax()
        bbox_center: pgf.Vec3d = (bbox_min + bbox_max) * 0.5
        bbox_size: pgf.Vec3d = bbox_max - bbox_min
        return bbox_center, bbox_size

    def _update_hydra_scene(self):
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
            self._calc_frame_scene()
        self._prev_cursor_pos = cursor_pos

    def _calc_viewport_orbit(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the orbit transformation for the viewport.
        """
        pivot_point = self._scene_bbox_center
        camera_xform: pgf.Matrix4d = self._camera.GetAttribute("xformOp:transform").Get()        
        camera_position = camera_xform.ExtractTranslation()
        x_rotation_axis = camera_xform.TransformDir(pgf.Vec3d(1, 0, 0))
        rot_axis = pgf.Vec3d(0, 1, 0) if self._up_axis == "Y" else pgf.Vec3d(0, 0, 1)
        rot_matrix_y = pgf.Matrix4d().SetRotate(pgf.Rotation(rot_axis, -delta_x * 0.1))
        rot_matrix_x = pgf.Matrix4d().SetRotate(pgf.Rotation(x_rotation_axis, -delta_y * 0.1))
        world_rotation: pgf.Matrix4d = (rot_matrix_x * rot_matrix_y)
        relative_pos: pgf.Vec3d = camera_position - pivot_point
        new_position = world_rotation.Transform(relative_pos) + pivot_point
        new_transform: pgf.Matrix4d =  camera_xform * world_rotation
        new_transform.SetTranslateOnly(new_position)
        self._camera.GetAttribute("xformOp:transform").Set(new_transform)

    def _calc_viewport_zoom(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the zoom transformation for the viewport.
        """
        transform_factor = self._scene_bbox_size.GetLength() / 1000.0
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, -delta_x * transform_factor))
        camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._camera.GetAttribute("xformOp:transform").Set(transform)

    def _calc_incremental_zoom(self, out=True) -> None:
        """
        Calculate the incremental zoom transformation for the viewport.
        """
        factor = self._scene_bbox_size.GetLength() / 10.0
        zoom_factor = factor if out else -factor
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, zoom_factor))
        camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._camera.GetAttribute("xformOp:transform").Set(transform)

    def _calc_viewport_pan(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the pan transformation for the viewport.
        """
        transform_factor = self._scene_bbox_size.GetLength() / 1000.0
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(-delta_x * transform_factor, delta_y * transform_factor, 0))
        camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._camera.GetAttribute("xformOp:transform").Set(transform)

    def _calc_frame_scene(self) -> None:
        """
        Frame the scene in the viewport.
        """
        bbox_size_factor = self._scene_bbox_size.GetLength()
        if bbox_size_factor <= 0:
            bbox_size_factor = 1.0
        distance_factor = 2.0
        distance = bbox_size_factor * distance_factor
        world_up = pgf.Vec3d(0, 1, 0) if  self._up_axis == "Y" else pgf.Vec3d(0, 0, 1)
        camera_position = self._camera.GetAttribute("xformOp:transform").Get().ExtractTranslation()
        if camera_position == pgf.Vec3d(0, 0, 0):
            camera_position = pgf.Vec3d(1000, 1000, 1000)
        current_distance = (self._scene_bbox_center - camera_position).GetLength()
        target_distance = distance / current_distance
        transform = cutils.calc_look_at(camera_position * target_distance, self._scene_bbox_center, world_up, flip_forward=True)
        self._camera.GetAttribute("xformOp:transform").Set(transform)
        target_scale = distance / 314
        light_scale = pgf.Vec3d(target_scale, target_scale, target_scale)
        self._light_xform.GetAttribute("xformOp:transform").Set(pgf.Matrix4d().SetScale(light_scale) * self._up_axis_matrix.GetInverse())

    def _init_opengl_settings(self) -> None:
        """
        Initialize OpenGL settings.
        """
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_MULTISAMPLE)

    def _setup_opengl_viewport(self) -> None:
        """
        Setup OpenGL viewport and perspective.
        """
        gl.glViewport(int(self._hydra_x_min), int(self._hydra_y_min), int(self._panel_width), int(self._panel_height))
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        fov = self._calc_fov()
        aspect_ratio = self._panel_width / self._panel_height
        near = self._cfg["viewport"]["clipping_range"][0]
        far = self._cfg["viewport"]["clipping_range"][1]
        top = near * math.tan(math.radians(fov) / 2)
        bottom = -top
        right = top * aspect_ratio
        left = -right
        gl.glFrustum(left, right, bottom, top, near, far)

        gl.glMatrixMode(gl.GL_MODELVIEW)        
        gl.glLoadIdentity()
        camera_transform: pgf.Matrix4d = self._camera.GetAttribute("xformOp:transform").Get() * self._up_axis_matrix
        camera_transform_offset = camera_transform.GetInverse()
        camera_transform_offset_np = np.array([camera_transform_offset.GetRow(i) for i in range(4)])
        gl.glLoadMatrixf(camera_transform_offset_np.flatten())

    def _draw_opengl_grid(self) -> None:
        """
        Draw a grid.
        """
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TRANSFORM_BIT | gl.GL_VIEWPORT_BIT)
        gl.glPushMatrix()

        self._setup_opengl_viewport()

        grid_density = self._cfg["viewport"]["grid_density"]
        
        #TEST
        grid_size = int(self._scene_bbox_size.GetLength() * 2.0)
        grid_color = self._cfg["viewport"]["grid_color"]
        step = grid_size / grid_density

        gl.glLineWidth(0.75)
        gl.glColor4f(*grid_color)
        gl.glBegin(gl.GL_LINES)        
        for index in range(-grid_density, grid_density + 1):
            gl.glVertex3f(index * step, 0.0, -grid_size)
            if index == 0:
                gl.glColor4f(0,0,1,1)  if self._up_axis == "Y" else gl.glColor4f(0,1,0,1)
            gl.glVertex3f(index * step, 0.0, 0.0)
            if index == 0:
                gl.glColor4f(*grid_color)
            gl.glVertex3f(index * step, 0.0, grid_size)
            if index == 0:
                gl.glColor4f(0,0,1,1)  if self._up_axis == "Y" else gl.glColor4f(0,1,0,1) 
            gl.glVertex3f(index * step, 0.0, 0.0)
            if index == 0:
                gl.glColor4f(*grid_color)           
            gl.glVertex3f(-grid_size, 0.0, index * step)
            if index == 0:
                gl.glColor4f(1,0,0,1)          
            gl.glVertex3f(0.0, 0.0, index * step)
            if index == 0:
                gl.glColor4f(*grid_color)
            gl.glVertex3f(grid_size, 0.0, index * step)
            if index == 0:
                gl.glColor4f(1,0,0,1)            
            gl.glVertex3f(0.0, 0.0, index * step)
            if index == 0:
                gl.glColor4f(*grid_color)        
        gl.glEnd()
        gl.glPopMatrix()
        gl.glPopAttrib()

    def _draw_opengl_gizmo(self) -> None:
        """
        Draw a small orientation gizmo.
        """
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TRANSFORM_BIT | gl.GL_VIEWPORT_BIT)

        gl.glPushMatrix()

        gizmo_size = 60
        gl.glViewport(int(self._hydra_x_min) + 10, int(self._hydra_y_min), gizmo_size, gizmo_size)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        camera_transform: pgf.Matrix4d = self._camera.GetAttribute("xformOp:transform").Get()
        camera_rotation_matrix = pgf.Matrix4d().SetRotate(camera_transform.ExtractRotation()).GetInverse()
        camera_rotation_matrix_np = np.array([camera_rotation_matrix.GetRow(i) for i in range(4)]) 
        gl.glLoadMatrixf(camera_rotation_matrix_np.flatten())

        axis_length = 0.5
        gl.glLineWidth(2.0)
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(axis_length, 0.0, 0.0)
        gl.glColor3f(0.0, 1.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(0.0, axis_length, 0.0)
        gl.glColor3f(0.0, 0.0, 1.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, axis_length)
        gl.glEnd()

        quad_size_min = axis_length * 0.1
        quad_size_max = axis_length
        gl.glBegin(gl.GL_QUADS)

        gl.glColor4f(1, 1, 1, 0.2)
        gl.glVertex3f(quad_size_min, 0.0, quad_size_min)
        gl.glVertex3f(quad_size_max, 0.0, quad_size_min)
        gl.glVertex3f(quad_size_max, 0.0, quad_size_max)
        gl.glVertex3f(quad_size_min, 0.0, quad_size_max)

        gl.glColor4f(1, 1, 1, 0.2)
        gl.glVertex3f(quad_size_min, quad_size_min, 0.0)
        gl.glVertex3f(quad_size_max, quad_size_min, 0.0)
        gl.glVertex3f(quad_size_max, quad_size_max, 0.0)
        gl.glVertex3f(quad_size_min, quad_size_max, 0.0)

        gl.glColor4f(1, 1, 1, 0.2)
        gl.glVertex3f(0.0, quad_size_min, quad_size_min)
        gl.glVertex3f(0.0, quad_size_max, quad_size_min)
        gl.glVertex3f(0.0, quad_size_max, quad_size_max)
        gl.glVertex3f(0.0, quad_size_min, quad_size_max)
        gl.glEnd()        

        gl.glPopMatrix()
        gl.glPopAttrib()
    
    def _draw_opengl_lights(self) -> None:
        """
        Draw a direction/distance light represenatation in OpenGL.
        """
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TRANSFORM_BIT | gl.GL_VIEWPORT_BIT)
        gl.glPushMatrix()
        self._setup_opengl_viewport()

        light_dict = self._create_light_info_dict()
        for light_prim in light_dict:
            scale_factor = (20.0 if light_dict[light_prim]["visibility"] == pgeo.Tokens.inherited else 60.0)
            widget_size = self._scene_bbox_size.GetLength() / scale_factor
            light_color = light_dict[light_prim]["color"] if light_dict[light_prim]["visibility"] == pgeo.Tokens.inherited else (0.0, 0.0, 0.0)
            transform_matrix: pgf.Matrix4d = light_dict[light_prim]["transform"]
            forward_vector= pgf.Vec3d(0.0, 0.0, -1.0)

            light_outer_color = (1.0, 1.0, 0.0) if light_dict[light_prim]["visibility"] == pgeo.Tokens.inherited else (0.0, 0.0, 0.0)  

            gl.glLineWidth(1.0)
            gl.glBegin(gl.GL_LINES)
            gl.glColor3f(*light_outer_color)
            transform_matrix = transform_matrix * self._up_axis_matrix
            box_vertex_1_matrix: pgf.Matrix4d = pgf.Matrix4d().SetTranslate(pgf.Vec3d(widget_size, widget_size, 0.0)) * transform_matrix
            box_vertex_2_matrix: pgf.Matrix4d = pgf.Matrix4d().SetTranslate(pgf.Vec3d(-widget_size, widget_size, 0.0)) * transform_matrix
            box_vertex_3_matrix: pgf.Matrix4d = pgf.Matrix4d().SetTranslate(pgf.Vec3d(-widget_size, -widget_size, 0.0)) * transform_matrix
            box_vertex_4_matrix: pgf.Matrix4d = pgf.Matrix4d().SetTranslate(pgf.Vec3d(widget_size, -widget_size, 0.0)) * transform_matrix 
            gl.glVertex3f(*box_vertex_1_matrix.ExtractTranslation())
            gl.glVertex3f(*box_vertex_2_matrix.ExtractTranslation())
            gl.glVertex3f(*box_vertex_2_matrix.ExtractTranslation())
            gl.glVertex3f(*box_vertex_3_matrix.ExtractTranslation())
            gl.glVertex3f(*box_vertex_3_matrix.ExtractTranslation())
            gl.glVertex3f(*box_vertex_4_matrix.ExtractTranslation())
            gl.glVertex3f(*box_vertex_4_matrix.ExtractTranslation())
            gl.glVertex3f(*box_vertex_1_matrix.ExtractTranslation())
            gl.glEnd()

            gl.glBegin(gl.GL_LINES)
            direction_vertex_1 = transform_matrix.Transform(pgf.Vec3d(0.0, 0.0, 0.0))
            direction_vertex_2 = transform_matrix.Transform(forward_vector * widget_size)
            gl.glColor3f(*light_color)
            gl.glVertex3f(*direction_vertex_1)
            gl.glVertex3f(*direction_vertex_2)
            gl.glEnd()

            gl.glBegin(gl.GL_LINE_LOOP)
            gl.glColor3f(*light_outer_color)
            num_segments = 128
            radius = widget_size * 0.75
            for index in range(num_segments):
                theta = 2.0 * math.pi * index / num_segments
                x = radius * math.cos(theta)
                y = radius * math.sin(theta)
                transformed_vertex = transform_matrix.Transform(pgf.Vec3d(x, y, 0.0))
                gl.glVertex3f(*transformed_vertex)
            gl.glEnd()
        gl.glPopMatrix()
        gl.glPopAttrib()


    def _draw_opengl_cameras(self) -> None:
        """
        Draw a direction/distance light represenatation in OpenGL.
        """
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TRANSFORM_BIT | gl.GL_VIEWPORT_BIT)
        gl.glPushMatrix()
        self._setup_opengl_viewport()

        camera_dict = self._create_camera_info_dict()
        for camera_prim in camera_dict:
            scale_factor = (50.0 if camera_dict[camera_prim]["visibility"] == pgeo.Tokens.inherited else 150.0)
            widget_size = self._scene_bbox_size.GetLength() / scale_factor
            transform_matrix: pgf.Matrix4d = camera_dict[camera_prim]["transform"]
            forward_vector= pgf.Vec3d(0.0, 0.0, -1.0)
            camera_color = (0.2, 0.2, 0.2) if camera_dict[camera_prim]["visibility"] == pgeo.Tokens.inherited else (0.0, 0.0, 0.0)
            gl.glLineWidth(1.0)
            gl.glBegin(gl.GL_LINES)
            direction_vertex_1 = transform_matrix.Transform(pgf.Vec3d(0.0, 0.0, 0.0))
            direction_vertex_2 = transform_matrix.Transform(forward_vector * widget_size)
            gl.glColor3f(*camera_color)
            gl.glVertex3f(*direction_vertex_1)
            gl.glVertex3f(*direction_vertex_2)
            gl.glEnd()

            gl.glBegin(gl.GL_LINE_LOOP)
            gl.glColor3f(*camera_color)
            num_segments = 128
            radius = widget_size * 0.75
            for index in range(num_segments):
                theta = 2.0 * math.pi * index / num_segments
                x = radius * math.cos(theta)
                y = radius * math.sin(theta)
                transformed_vertex = transform_matrix.Transform(pgf.Vec3d(x, y, 0.0))
                gl.glVertex3f(*transformed_vertex)
            gl.glEnd()

            gl.glBegin(gl.GL_LINE_LOOP)
            gl.glColor3f(*camera_color)
            num_segments = 128
            radius = widget_size * 0.75
            for index in range(num_segments):
                theta = 2.0 * math.pi * index / num_segments
                x = radius * math.cos(theta)
                y = radius * math.sin(theta)
                transformed_vertex = transform_matrix.Transform(pgf.Vec3d(x, y, widget_size))
                gl.glVertex3f(*transformed_vertex)
            gl.glEnd()

            gl.glBegin(gl.GL_LINES)
            gl.glColor3f(*camera_color)
            camera_edge_vert_1 = transform_matrix.Transform(pgf.Vec3d(radius, 0.0, 0.0))
            camera_edge_vert_2 = transform_matrix.Transform(pgf.Vec3d(radius, 0.0, widget_size))
            camera_edge_vert_3 = transform_matrix.Transform(pgf.Vec3d(0.0, radius, 0.0))
            camera_edge_vert_4 = transform_matrix.Transform(pgf.Vec3d(0.0, radius, widget_size))
            camera_edge_vert_5 = transform_matrix.Transform(pgf.Vec3d(-radius, 0.0, 0.0))
            camera_edge_vert_6 = transform_matrix.Transform(pgf.Vec3d(-radius, 0.0, widget_size))
            camera_edge_vert_7 = transform_matrix.Transform(pgf.Vec3d(0.0, -radius, 0.0))
            camera_edge_vert_8 = transform_matrix.Transform(pgf.Vec3d(0.0, -radius, widget_size))
            gl.glVertex3f(*camera_edge_vert_1)
            gl.glVertex3f(*camera_edge_vert_2)
            gl.glVertex3f(*camera_edge_vert_3)
            gl.glVertex3f(*camera_edge_vert_4)
            gl.glVertex3f(*camera_edge_vert_5)
            gl.glVertex3f(*camera_edge_vert_6)
            gl.glVertex3f(*camera_edge_vert_7)
            gl.glVertex3f(*camera_edge_vert_8)
            gl.glEnd()

        gl.glPopMatrix()
        gl.glPopAttrib()

    def _create_c_opengl_draw_dict(self) -> dict:
        """
        Create a dictionary for OpenGL drawing.
        """
        camera_matrix = self._camera.GetAttribute("xformOp:transform").Get()
        camera_matrix_np = np.array(camera_matrix).flatten()
        up_axis_marix_np = np.array(self._up_axis_matrix).flatten()
        draw_dict = {}
        draw_dict["camera_matrix"] = camera_matrix_np
        draw_dict["up_axis_matrix"] = up_axis_marix_np
        draw_dict["panel_width"] = self._panel_width
        draw_dict["panel_height"] = self._panel_height
        draw_dict["hydra_x_min"] = self._hydra_x_min
        draw_dict["hydra_y_min"] = self._hydra_y_min
        draw_dict["fov"] = self._calc_fov()
        draw_dict["near_z"] = self._cfg["viewport"]["clipping_range"][0]
        draw_dict["far_z"] = self._cfg["viewport"]["clipping_range"][1]
        return draw_dict

    def _draw_c_opengl_bones(self) -> None:
        camera_matrix: pgf.Matrix4d = self._camera.GetAttribute("xformOp:transform").Get()
        cdraw.c_draw_opengl_bones(self._scene_manager.get_data_node_list(), self._create_c_opengl_draw_dict())
            
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
        self._update_hydra_scene()
        self._hydra.Render(self._stage.GetPseudoRoot(), self._hydra_rend_params)
        if self._user_cfg["show"]["bones"]:
            self._draw_c_opengl_bones()
        if self._user_cfg["show"]["grid"]:
            self._draw_opengl_grid()
        if self._user_cfg["show"]["lights"]:
            self._draw_opengl_lights()
        if self._user_cfg["show"]["camera"]:
            self._draw_opengl_cameras()
        if self._user_cfg["show"]["gizmo"]:
            self._draw_opengl_gizmo()


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
                    selected, clicked = imgui.checkbox(f"  {axis}  ", self._up_axis == axis)
                    if selected:
                        self._up_axis = axis
                        self._calc_up_axis()
                        self._calc_frame_scene()
            imgui.end_combo()
        imgui.same_line()
        icon = cstat.Icon.ICON_VIEWPORT_AXIS_Y if self._up_axis == "Y" else cstat.Icon.ICON_VIEWPORT_AXIS_Z
        axis_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, icon, (15, 15))
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 2)
        imgui.image(axis_icon_id, (15, 15), tint_col=(0.75, 0.75, 0.75, 1))
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
                    self._enable_default_lights()
                    self._disable_scene_lights()
                selected, clicked = imgui.checkbox("Scene", self._scene_light)
                if selected:
                    self._disable_default_lights()
                    self._enable_scene_lights()
            imgui.end_combo()
        imgui.same_line()
        icon = cstat.Icon.ICON_VIEWPORT_LIGHT
        light_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, icon, (15, 15))
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 2)
        imgui.image(light_icon_id, (15, 15), tint_col=(0.75, 0.75, 0.75, 1))
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
        imgui.image(camera_icon_id, (15, 15), tint_col=(0.75, 0.75, 0.75, 1))
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
        imgui.image(settings_icon_id, (15, 15), tint_col=(0.75, 0.75, 0.75, 1))
        
        imgui.same_line()
        imgui.push_item_width(30)
        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() - 8)
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        if imgui.begin_combo("##user_settings", "", imgui.ComboFlags_.height_largest):
            for vis_setting in self._user_cfg["show"]:
                vis_setting: str
                selected, clicked = imgui.checkbox(f" {vis_setting.title()}", self._user_cfg["show"][vis_setting])
                if selected:
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
            imgui.image(icon_id, icon_size, tint_col=(0.75, 0.75, 0.75, 1))
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
