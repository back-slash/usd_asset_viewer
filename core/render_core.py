#####################################################################################################################################
# USD Asset Viewer | Core | Render 
# TODO:
# - Integrate Hydra
#####################################################################################################################################
# PYTHON
import ctypes


# ADDONS
from imgui_bundle import imgui
import glfw
import OpenGL.GL as gl
import pxr.Usd as pusd
import pxr.UsdGeom as pgeo
import pxr.UsdImagingGL as pimg
import pxr.Gf as pgf
import pxr.Sdf as psdf

# PROJECT
import core.utils_core as cutils
import core.static_core as cstat
#####################################################################################################################################



class RenderContextManager:
    """
    Render and context manager.
    """
    _instance = None
    _render_loop_function =  None
    def __new__(cls, render_loop_function):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, render_loop_function):
        self._render_loop_function = render_loop_function
        if hasattr(self, 'context_list') and len(self.context_list) > 0:
            imgui.set_current_context(self.context_list[-1])
            self.context_list.append(imgui.create_context())
            self._init_renderer()
            return
        self.context_list = []
        self.context_list.append(imgui.create_context())
        self._cfg = cutils.get_core_config()   
        self._init_renderer()

    def _init_renderer(self):
        """
        Initialize the ImGui renderer.
        """
        imgui.set_current_context(self.context_list[-1])
        self._init_glfw()
        
    def _init_glfw(self):
        """
        Initialize GLFW for window management.
        """
        use_hydra = self._cfg['settings']['use_hydra']
        if use_hydra:
            self._glfw = GLFWHydraOpenGLWindow(self._render_loop_function)
        else:
            self._glfw = GLFWOpenGLWindow(self._render_loop_function)
        self._glfw_window = self._glfw.get_window()
        self._glfw_window_address = self._glfw.get_window_address()
        imgui.backends.glfw_init_for_opengl(self._glfw_window_address, True)
        imgui.backends.opengl3_init("#version 450")

    def _update_window_size(self):
        """ 
        Update the size of the panels.
        """
        self._display_size = imgui.get_io().display_size 

    def get_frame_size(self):
        """
        Get the size of the frame.
        """
        self._update_window_size()
        return self._display_size
    
    def remove_context(self, context):
        """
        Remove a context from the context list.
        """
        if context in self.context_list:
            self.context_list.remove(context)
            imgui.set_current_context(context)
            imgui.backends.opengl3_shutdown()
            imgui.destroy_context(context)

    def render(self, draw_data, context):
        """
        Render the ImGui context.
        """
        imgui.set_current_context(context)
        imgui.backends.opengl3_render_draw_data(draw_data)

    def get_glfw(self):
        """
        Get the GLFW class.
        """
        return self._glfw

    def set_usd_stage(self, stage: pusd.Stage):
        """
        Set the USD stage.
        """
        if self._cfg['settings']['use_hydra']:
            self._glfw.set_usd_stage(stage)

    def refresh_font_texture(self):
        font_atlas = imgui.get_io().fonts
       
        pixels = imgui.font_atlas_get_tex_data_as_rgba32(font_atlas)

        width = font_atlas.tex_width
        height = font_atlas.tex_height

        if hasattr(self, "_font_texture") and self._font_texture:
            gl.glDeleteTextures([self._font_texture])

        self._font_texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._font_texture)
        
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, 
            width, height, 0, 
            gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, 
            pixels
        )
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        font_atlas.set_tex_id(self._font_texture)



class GLFWOpenGLWindow:
    """
    GLFW Window class for rendering.
    """
    def __init__(self, render_loop_function):
        self._render_loop_function = render_loop_function
        self._init_config()
        self._init_frame()

    def _init_config(self):
        """
        Initialize the core config.
        """
        self._cfg = cutils.get_core_config()
        self._cfg_width = self._cfg["glfw"]["window_size"][0]
        self._cfg_height = self._cfg["glfw"]["window_size"][1]
        self._cfg_title = self._cfg["glfw"]["title"]
        self._cfg_gl_color = self._cfg["glfw"]["gl_color"]

    def _init_frame(self):
        """
        Initialize the GLFW window.
        """
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        self._window = glfw.create_window(self._cfg_width, self._cfg_height, self._cfg_title, None, None)
        if not self._window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        glfw.make_context_current(self._window)

    def _render_loop(self):
        """
        Render loop for the GLFW window.
        """
        while not glfw.window_should_close(self._window):
            self._set_imgui_window_size()
            glfw.poll_events()
            gl.glClearColor(*self._cfg_gl_color)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            self._render_loop_function()
            glfw.swap_buffers(self._window)
        glfw.terminate()

    def _set_imgui_window_size(self):
        """
        Set the size of the GLFW window.
        """
        imgui.get_io().display_size = glfw.get_window_size(self.get_window())

    def begin_render_loop(self):
        """
        Start the render loop.
        """
        self._render_loop()

    def get_window(self):
        """
        Get the GLFW window.
        """
        return self._window
    
    def get_window_address(self):
        """
        Get the address of the GLFW window.
        """
        return ctypes.cast(self._window, ctypes.c_void_p).value
    


class GLFWHydraOpenGLWindow:
    """
    GLFW Window class for rendering Hydra.
    """
    _key_scroll_up = False
    _key_scroll_down = False
    def __init__(self, render_loop_function, stage: pusd.Stage = None):
        self._render_loop_function = render_loop_function
        self._stage = stage
        self._init_config()
        self._init_frame()

    def _init_config(self):
        """
        Initialize the core config.
        """
        self._cfg = cutils.get_core_config()
        self._cfg_width = self._cfg["glfw"]["window_size"][0]
        self._cfg_height = self._cfg["glfw"]["window_size"][1]
        self._cfg_title = self._cfg["glfw"]["title"]
        self._cfg_gl_color = self._cfg["glfw"]["gl_color"]
        self._cfg_vsync = self._cfg["glfw"]["vsync"]

    def _init_hydra(self):
        """
        Initialize the Hydra renderer.
        """        
        self._hydra = pimg.Engine()

        self._hydra_rend_params = pimg.RenderParams()
        self._hydra_rend_params.drawMode = pimg.DrawMode.DRAW_WIREFRAME_ON_SURFACE
        self._hydra_rend_params.gammaCorrectColors = False
        self._hydra_rend_params.enableLighting = True
        self._hydra_rend_params.enableSceneLights = True
        self._hydra_rend_params.enableIdRender = True

        render_plugins = self._hydra.GetRendererPlugins()
        if render_plugins:
            self._hydra.SetRendererPlugin(render_plugins[0])
            self._camera = self._create_camera()
            self._hydra.SetCameraPath(self._camera.GetPath())
        else:
            raise RuntimeError("No renderer plugins available")

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

    def _init_frame(self):
        """
        Initialize the GLFW window.
        """
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        self._window = glfw.create_window(self._cfg_width, self._cfg_height, self._cfg_title, None, None)
        if not self._window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        glfw.make_context_current(self._window)
        if self._cfg_vsync:
            glfw.swap_interval(1) 
        glfw.set_scroll_callback(self._window, self._mouse_scroll_callback)

    def _mouse_scroll_callback(self, window, x_offset, y_offset):
        """
        Mouse scroll callback for GLFW window.
        """
        if y_offset > 0:
            self._key_scroll_up = True
        elif y_offset < 0:
            self._key_scroll_down  = True

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

    def _render_loop(self):
        """
        Render loop for the GLFW window with Hydra rendering.
        """
        while not glfw.window_should_close(self._window):
            self._set_imgui_window_size()
            self._process_glfw_events()
            glfw.poll_events()
            gl.glClearColor(*self._cfg_gl_color)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)                    
            if self._stage:
                self._hydra_render_loop()  
            self._render_loop_function()   
            glfw.swap_buffers(self._window)
        glfw.terminate()

    def _hydra_render_loop(self):
        """
        Render loop for the Hydra renderer.
        """
        size = glfw.get_framebuffer_size(self._window)
        self._hydra.SetRenderViewport((0, 0, size[0], size[1]))
        self._hydra.SetRenderBufferSize(size)
        self._update_hydra_camera()
        self._hydra.Render(self._stage.GetPseudoRoot(), self._hydra_rend_params)

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

    def _update_hydra_camera(self):
        """
        Update the Hydra camera.
        """
        bbox_center, bbox_size = self._create_scene_bounding_box()
        bbox_quatified = (bbox_size.GetLength()) / 1000.0
        cursor_pos = glfw.get_cursor_pos(self._window)
        if self._orbit or self._zoom or self._pan:
            cursor_pos = glfw.get_cursor_pos(self._window)
            delta_x = cursor_pos[0] - self._prev_cursor_pos[0]
            delta_y = cursor_pos[1] - self._prev_cursor_pos[1]
            self._prev_cursor_pos = cursor_pos
            if self._orbit:
                transform = pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(0, 1, 0), -delta_x * 0.1))
                transform *= pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(1, 0, 0), -delta_y * 0.1))
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


                     


    def _set_imgui_window_size(self):
        """
        Set the size of the GLFW window.
        """
        imgui.get_io().display_size = glfw.get_window_size(self.get_window())

    def begin_render_loop(self):
        """
        Start the render loop.
        """
        self._render_loop()

    def get_window(self):
        """
        Get the GLFW window.
        """
        return self._window

    def get_window_address(self):
        """
        Get the address of the GLFW window.
        """
        return ctypes.cast(self._window, ctypes.c_void_p).value
    
    def set_usd_stage(self, stage: pusd.Stage):
        """
        Set the USD stage.
        """
        self._stage = stage
        self._init_hydra()


