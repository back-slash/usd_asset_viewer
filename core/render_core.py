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
    _render_loop_function =  None
    def __new__(cls, title, width, height, render_loop_function):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, title, width, height, render_loop_function):
        self._title = title
        self._width = width
        self._height = height
        self._render_loop_function = render_loop_function
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
        
    def _init_glfw(self):
        """
        Initialize GLFW for window management.
        """
        self._glfw_frame = GLFWFrame(self._title, self._width, self._height, self._render_loop_function)
        
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

    def get_glfw_frame(self):
        """
        Get the GLFW frame.
        """
        return self._glfw_frame


class GLFWFrame:
    """
    GLFW Window class for rendering.
    """
    def __init__(self, title, width, height, render_loop_function):
        self._title = title        
        self._width = width
        self._height = height
        self._render_loop_function = render_loop_function
        self._init_frame()

    def _init_frame(self):
        """
        Initialize the GLFW window.
        """
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        self._window = glfw.create_window(self._width, self._height, self._title, None, None)
        if not self._window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        glfw.make_context_current(self._window)

    def _render_loop(self):
        """
        Render loop for the GLFW window.
        """
        while not glfw.window_should_close(self._window):
            glfw.poll_events()
            try:
                self._render_loop_function()
            except Exception as e:
                print(f"Error in render loop: {e}")
            glfw.swap_buffers(self._window)
        glfw.terminate()

    def start_rendering(self):
        """
        Start the rendering loop.
        """
        self._render_loop()

    def get_window(self):
        """
        Get the GLFW window.
        """
        return self._window