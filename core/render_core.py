#####################################################################################################################################
# USD Asset Viewer | Core | Imgui Render 
# TODO:
# -
#####################################################################################################################################
# PYTHON


# ADDONS
from imgui_bundle import imgui
from pxr import Usd, UsdImaging, Hd, Glf
import glfw

# PROJECT

#####################################################################################################################################



class RenderContextManager:
    """
    Render and context manager.
    """
    _instance = None
    _hydra = False
    def __new__(cls):
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

    def _init_hydra(self):
        """
        Initialize Hydra for USD rendering.
        """
        if self._hydra:
            self.hydra_delegate = Hd.StormRenderDelegate()
            self.hydra_render_index = Hd.RenderIndex(self.hydra_delegate)
            self.hydra_engine = Hd.Engine()
            self.scene_delegate = None

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

    def load_usd_scene(self, usd_file_path):
        """
        Load a USD scene and set up the Hydra scene delegate.
        """
        stage = Usd.Stage.Open(usd_file_path)
        if not stage:
            raise ValueError(f"Failed to open USD file: {usd_file_path}")
        if self._hydra:
            self.scene_delegate = UsdImaging.SceneDelegate(self.hydra_render_index, stage.GetPseudoRoot())

    def render_usd_scene(self):
        """
        Render the USD scene using Hydra.
        """
        if not self.scene_delegate:
            raise RuntimeError("No USD scene loaded for rendering.")
        imgui.set_current_context(self.context_list[-1])
        Glf.GLContext.BindDefaultFramebuffer()
        self.hydra_engine.Execute(self.hydra_render_index, Hd.TaskSharedPtrVector())
    
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
        self.width = width
        self.height = height
        self.title = title
        self.window = None
        self._init_frame()

    def _init_frame(self):
        """
        Initialize the GLFW window.
        """
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        glfw.make_context_current(self.window)