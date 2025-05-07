#####################################################################################################################################
# USD Asset Viewer | Core | Render 
# TODO:
# - Integrate Hydra
#####################################################################################################################################
# PYTHON
import ctypes
import os
from typing import Callable

# ADDONS
from imgui_bundle import imgui
import glfw
import OpenGL.GL as gl
import pxr.Usd as pusd
import pxr.UsdGeom as pgeo
import pxr.UsdImagingGL as pimg
import pxr.Gf as pgf

# PROJECT
import core.utils_core as cutils
import core.static.static_core as cstat
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
        imgui.backends.opengl3_new_frame()

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
        self._hydra_rend_params.enableLighting = False
        self._hydra_rend_params.enableIdRender = False
        self._hydra_rend_params.complexity = 1.0
        self._hydra_rend_params.enableSampleAlphaToCoverage = False

        render_plugins = self._hydra.GetRendererPlugins()
        if render_plugins:
            self._hydra.SetRendererPlugin(render_plugins[0])
            camera = self._stage.GetPrimAtPath("/Camera")
            if camera:
                self._hydra.SetCameraPath(camera.GetPath())
        else:
            raise RuntimeError("No renderer plugins available")

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

    def _render_loop(self):
        """
        Render loop for the GLFW window with Hydra rendering.
        """
        previous_stage = None
        while not glfw.window_should_close(self._window):
            self._set_imgui_window_size()
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
        self._hydra.Render(self._stage.GetPseudoRoot(), self._hydra_rend_params)

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
        
        
