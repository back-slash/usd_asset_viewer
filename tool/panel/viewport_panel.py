#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Viewport
# TODO:
# -
#####################################################################################################################################

# PYTHON
from argparse import FileType
from typing import Any

# ADDONS
from imgui_bundle import imgui
import glfw
import OpenGL.GL as gl
from numpy import double, size
import pxr.Usd as pusd
import pxr.UsdGeom as pgeo
import pxr.UsdImagingGL as pimg
import pxr.Gf as pgf
import pxr.Sdf as psdf
import pxr.UsdShade as pshd

# PROJECT
import core.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
#####################################################################################################################################
    
class ViewportDrawStyleOverlay():
    """
    Enum for viewport draw styles.
    """
    def __init__(self):
        pass
        



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

    def _init_viewport_draw_styles(self):
        """
        Initialize the viewport draw styles.
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
        Initialize the Hydra renderer.
        """
        self._hydra = pimg.Engine()
        render_plugins = self._hydra.GetRendererPlugins()
        if render_plugins:
            glfw.set_scroll_callback(self._window, self._mouse_scroll_callback)
            self._hydra.SetRendererPlugin(render_plugins[0])
            self._camera = self._create_camera()
            self._hydra.SetCameraPath(self._camera.GetPath())
        else:
            raise RuntimeError("No renderer plugins available")

    def _update_hydra_render_params(self):
        """
        Update the Hydra render parameters.
        """
        draw_style_dict = self._cfg["viewport"]["draw_style"]
        selected_draw_style_dict = draw_style_dict[self._current_draw_style]
        self._hydra_rend_params = pimg.RenderParams()
        self._hydra_rend_params.drawMode = getattr(pimg.DrawMode, selected_draw_style_dict["draw_mode"])
        self._hydra_rend_params.enableLighting = selected_draw_style_dict["enable_lighting"]
        self._hydra_rend_params.enableSampleAlphaToCoverage = True
        
        

    #CONVERT TO IMGUI
    def _process_glfw_events(self):
        """
        Process GLFW events.
        """
        self._orbit = False
        self._zoom = False
        self._pan = False
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
        camera = pgeo.Camera.Define(self._stage, "/OrbitCamera")
        camera.CreateFocalLengthAttr(50.0)
        camera.CreateHorizontalApertureAttr(20.955)
        camera.CreateVerticalApertureAttr(15.2908)
        camera.CreateClippingRangeAttr(pgf.Vec2f(self._cfg["camera"]["clipping_range"]))
        xform_attr = camera.GetPrim().CreateAttribute("xformOp:transform", psdf.ValueTypeNames.Matrix4d)
        xform_attr.Set(pgf.Matrix4d().SetIdentity())

        xform_op_order = camera.GetPrim().GetAttribute("xformOpOrder")
        if not xform_op_order:
           xform_op_order = camera.GetPrim().CreateAttribute("xformOpOrder", psdf.ValueTypeNames.TokenArray)
        xform_op_order.Set(["xformOp:transform"])

        return camera.GetPrim()    

    def _create_scene_bounding_box(self):
        """
        Create a bounding box for the scene.
        """
        bbox_cache = pgeo.BBoxCache(pusd.TimeCode.Default(), includedPurposes=[pgeo.Tokens.default_, pgeo.Tokens.render])
        bbox = bbox_cache.ComputeWorldBound(self._stage.GetPseudoRoot())
        bbox_min = bbox.GetRange().GetMin()
        bbox_max = bbox.GetRange().GetMax()
        bbox_center: pgf.Vec3d = (bbox_min + bbox_max) * 0.5
        bbox_size: pgf.Vec3d = bbox_max - bbox_min
        return bbox_center, bbox_size    

    #NEEDS WORK
    def _update_hydra_camera(self):
        """
        Update the viewport camera.
        """
        bbox_center, bbox_size = self._create_scene_bounding_box()
        bbox_quatified = bbox_size.GetLength() / 5000.0
        cursor_pos = glfw.get_cursor_pos(self._window)
        if self._orbit or self._zoom or self._pan:
            cursor_pos = glfw.get_cursor_pos(self._window)
            delta_x = cursor_pos[0] - self._prev_cursor_pos[0]
            delta_y = cursor_pos[1] - self._prev_cursor_pos[1]
            if self._orbit:
                self._calc_viewport_orbit(bbox_center, delta_x, delta_y)
            elif self._zoom:
                self._calc_viewport_zoom(delta_x, delta_y)
            elif self._pan:
                self._calc_viewport_pan(delta_x, delta_y)
        if self._incremental_zoom_in:
            self._calc_incremental_zoom(bbox_quatified, out=False)
        if self._incremental_zoom_out:
            self._calc_incremental_zoom(bbox_quatified, out=True)
        if self._frame_scene:
            self._calc_frame_scene(bbox_size, bbox_center)
        self._prev_cursor_pos = cursor_pos

    def _calc_viewport_orbit(self, bbox_center: pgf.Vec3d, delta_x: float, delta_y: float) -> None:
        """
        Calculate the orbit transformation for the viewport.
        """
        pivot_point = bbox_center
        camera_xform: pgf.Matrix4d = self._camera.GetAttribute("xformOp:transform").Get()        
        camera_position = camera_xform.ExtractTranslation()
        x_rotation_axis = camera_xform.TransformDir(pgf.Vec3d(1, 0, 0))
        rot_matrix_y = pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(0, 1, 0), -delta_x * 0.1))
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
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, -delta_x * 1))
        camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._camera.GetAttribute("xformOp:transform").Set(transform)

    def _calc_incremental_zoom(self, bbox_quatified: float, out=True) -> None:
        """
        Calculate the incremental zoom transformation for the viewport.
        """
        amount = 200 if out else -200
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, amount * bbox_quatified))
        camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
        camera_xform = transform * camera_xform
        self._camera.GetAttribute("xformOp:transform").Set(camera_xform)

    def _calc_viewport_pan(self, delta_x: float, delta_y: float) -> None:
        """
        Calculate the pan transformation for the viewport.
        """
        transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(-delta_x * 1, delta_y * 1, 0))
        camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
        transform = transform * camera_xform
        self._camera.GetAttribute("xformOp:transform").Set(transform)

    def _calc_frame_scene(self, bbox_size, bbox_center) -> None:
        """
        Frame the scene in the viewport.
        """
        max_dimension = max(bbox_size[0], bbox_size[1], bbox_size[2])
        if max_dimension <= 0:
            max_dimension = 1.0
        distance_factor = 2.0
        distance = max_dimension * distance_factor
        camera_position = bbox_center + pgf.Vec3d(0, 0, distance)
        transform = pgf.Matrix4d().SetIdentity()
        transform.SetTranslateOnly(camera_position)
        up = pgf.Vec3d(0, 1, 0)
        rotation = pgf.Matrix4d().SetLookAt(-camera_position, bbox_center, up)
        transform = transform * rotation

        self._camera.GetAttribute("xformOp:transform").Set(transform)

    def _hydra_render_loop(self, position: tuple[int, int]) -> None:
        """
        Render loop for the Hydra renderer.
        """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        display_size = glfw.get_window_size(self._window)
        hydra_x_min = position[0]
        hydra_y_min = display_size[1] - position[1] - self._panel_height
        self._hydra.SetRenderViewport((hydra_x_min, hydra_y_min, self._panel_width, self._panel_height))
        self._hydra.SetRenderBufferSize(pgf.Vec2i(int(self._panel_width), int(self._panel_height)))
        self._update_hydra_camera()
        self._hydra.Render(self._stage.GetPseudoRoot(), self._hydra_rend_params)

    # TEMPORARY
    def _draw_draw_style_radio(self):
        """
        Draw the render modes for the viewport.
        """
        imgui.set_cursor_pos_x(self._panel_width - 50)
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 3)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 1.0)
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (3, 3))
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (5, -5))

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
            imgui.image(icon_id, icon_size, tint_col=(0.5, 0.5, 0.5, 1))
            imgui.new_line()

        imgui.pop_style_var(4)
        imgui.pop_style_color(4)

    def draw(self, position: tuple[int, int]) -> None:
        """
        Draw the outliner panel.
        """ 
        self._process_glfw_events()
        if self._stage:
            self._hydra_render_loop(position)
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(position)
        imgui.begin(self._name, True, self._window_flags)
        self._draw_draw_style_radio()

    def update_usd(self):
        super().update_usd()
        self._init_hydra()

    def shutdown(self):
        """
        Shutdown the viewport panel.
        """
        self._hydra.StopRenderer()
        del(self._hydra)
