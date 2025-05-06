#####################################################################################################################################
# USD Asset Viewer | Core | Imgui Render 
# TODO:
# -
#####################################################################################################################################
# PYTHON


# ADDONS
from imgui_bundle import imgui
from pxr import Usd as pusd
import glfw

# PROJECT

#####################################################################################################################################



class RenderContextManager:
    """
    Render and context manager.
    """
    _instance = None
    _hydra = False
    def __new__(cls, title, width, height):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, title, width, height):
        self._title = title
        self._width = width
        self._height = height
        if hasattr(self, 'context_list') and len(self.context_list) > 0:
            imgui.set_current_context(self.context_list[-1])
            self.context_list.append(imgui.create_context())
            self._init_renderer()
            return
        self.context_list = []
        self.context_list.append(imgui.create_context())   
        self._init_renderer()

    def _init_renderer(self):
        """
        Initialize the ImGui renderer.
        """
        imgui.set_current_context(self.context_list[-1])
        self._init_glfw()
        imgui.backends.opengl3_init("#version 330")

    def _init_glfw(self):
        """
        Initialize GLFW for window management.
        """
        self._glfw_frame = GLFWFrame(self._title, self._width, self._height)

    def _update_size(self):
        """
        Update the size of the panels.
        """
        self._display_size = imgui.get_io().display_size 

    def get_frame_size(self):
        """
        Get the size of the frame.
        """
        self._update_size() 
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



class GLFWFrame:
    """
    GLFW Window class for rendering.
    """
    def __init__(self, title, width, height):
        self._title = title        
        self._width = width
        self._height = height

        self.window = None
        self._init_frame()

    def _init_frame(self):
        """
        Initialize the GLFW window.
        """
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        self.window = glfw.create_window(self._width, self._height, self._title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        glfw.make_context_current(self.window)