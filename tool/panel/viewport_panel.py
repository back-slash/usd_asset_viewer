#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Viewport
# TODO:
# -
#####################################################################################################################################

# PYTHON
from typing import Any

# ADDONS
from imgui_bundle import imgui
import glfw
import OpenGL.GL as gl
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
      
class ViewportPanel(cbase.Panel):
    """
    Viewport for USD Scene.
    """
    _key_scroll_up = False
    _key_scroll_down = False
    def __init__(self, frame: cbase.Frame):
        super().__init__("viewport", frame)
        self._window = frame.get_window()

    def _init_hydra(self):
        """
        Initialize the Hydra renderer.
        """        
        self._hydra = pimg.Engine()

        self._hydra_rend_params = pimg.RenderParams()
        self._hydra_rend_params.drawMode = pimg.DrawMode.DRAW_SHADED_SMOOTH
        self._hydra_rend_params.gammaCorrectColors = False
        self._hydra_rend_params.enableLighting = True
        self._hydra_rend_params.enableIdRender = True
        self._hydra_rend_params.enableSampleAlphaToCoverage = True
        self._hydra_rend_params.enableUsdDrawModes = True



        render_plugins = self._hydra.GetRendererPlugins()
        if render_plugins:
            self._hydra.SetRendererPlugin(render_plugins[0])
            self._camera = self._create_camera()
            self._hydra.SetCameraPath(self._camera.GetPath())
        else:
            raise RuntimeError("No renderer plugins available")

    def _process_glfw_events(self):
        """
        Process GLFW events.
        """
        self._key_f = glfw.get_key(self._window, glfw.KEY_F)
        self._key_esc = glfw.get_key(self._window, glfw.KEY_ESCAPE)
        self._key_alt = glfw.get_key(self._window, glfw.KEY_LEFT_ALT) or glfw.get_key(self._window, glfw.KEY_RIGHT_ALT)
        self._key_shift = glfw.get_key(self._window, glfw.KEY_LEFT_SHIFT) or glfw.get_key(self._window, glfw.KEY_RIGHT_SHIFT)
        
        self._key_mouse_position = glfw.get_cursor_pos(self._window)
        self._key_mouse_left = glfw.get_mouse_button(self._window, glfw.MOUSE_BUTTON_LEFT)
        self._key_mouse_right = glfw.get_mouse_button(self._window, glfw.MOUSE_BUTTON_RIGHT)
        self._key_mouse_middle = glfw.get_mouse_button(self._window, glfw.MOUSE_BUTTON_MIDDLE)

        
        self._orbit = False
        self._zoom = False
        self._pan = False
        self._incremental_zoom_in = False
        self._incremental_zoom_out = False
        self._frame_scene = False
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
        Update the Hydra camera.
        """
        bbox_center, bbox_size = self._create_scene_bounding_box()
        bbox_quatified = bbox_size.GetLength() / 5000.0
        cursor_pos = glfw.get_cursor_pos(self._window)
        if self._orbit or self._zoom or self._pan:
            cursor_pos = glfw.get_cursor_pos(self._window)
            delta_x = cursor_pos[0] - self._prev_cursor_pos[0]
            delta_y = cursor_pos[1] - self._prev_cursor_pos[1]
            self._prev_cursor_pos = cursor_pos
            if self._orbit:
                transform = pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(0, 1, 0), -delta_x * 0.1 * bbox_quatified))
                transform *= pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(1, 0, 0), -delta_y * 0.1 * bbox_quatified))
                self._camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
                self._camera_xform = transform * self._camera_xform
                self._camera.GetAttribute("xformOp:transform").Set(self._camera_xform)
            elif self._zoom:
                transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, delta_x * 1 * bbox_quatified))
                self._camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
                self._camera_xform = transform * self._camera_xform
                self._camera.GetAttribute("xformOp:transform").Set(self._camera_xform)
            elif self._pan:
                transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(-delta_x * 1 * bbox_quatified, delta_y * 1 * bbox_quatified, 0))
                self._camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
                self._camera_xform = transform * self._camera_xform
                self._camera.GetAttribute("xformOp:transform").Set(self._camera_xform)
        if self._incremental_zoom_in:
            transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, -10 * bbox_quatified))
            self._camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
            self._camera_xform = transform * self._camera_xform
            self._camera.GetAttribute("xformOp:transform").Set(self._camera_xform)
        if self._incremental_zoom_out:
            transform = pgf.Matrix4d().SetTranslate(pgf.Vec3d(0, 0, 10 * bbox_quatified))
            self._camera_xform = self._camera.GetAttribute("xformOp:transform").Get()
            self._camera_xform = transform * self._camera_xform
            self._camera.GetAttribute("xformOp:transform").Set(self._camera_xform)
        if self._frame_scene:
            distance = max(bbox_size) * 4.0
            existing_transform: pgf.Matrix4d = self._camera.GetAttribute("xformOp:transform").Get()
            existing_position = existing_transform.ExtractTranslation()
            existing_distance = ((existing_position - bbox_center).GetLength())
            scale_factor = distance / existing_distance
            if existing_position != pgf.Vec3d(0, 0, 0):
                altered_position = existing_position * scale_factor
            else:
                altered_position = pgf.Vec3d(bbox_center[0], bbox_center[1], bbox_center[2] + distance)
            transform = existing_transform
            transform = transform.SetTranslateOnly(altered_position) 
            self._camera.GetAttribute("xformOp:transform").Set(transform)
        self._prev_cursor_pos = cursor_pos

    
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
        imgui.text("Viewport")

    def update_usd(self):
        super().update_usd()
        self._init_hydra()
