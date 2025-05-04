#####################################################################################################################################
# USD Outliner | Core | Imgui Render 
# TODO:
# -
#####################################################################################################################################
# PYTHON


# ADDONS
from imgui_bundle import imgui

# PROJECT

#####################################################################################################################################



class RenderContextManager:
    """
    Render/Context manager.
    """
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
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
        Initialize the renderer.
        """
        imgui.set_current_context(self.context_list[-1])
        imgui.backends.opengl3_init("#version 330")

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
        Render the context.
        """
        imgui.set_current_context(context)
        imgui.backends.opengl3_render_draw_data(draw_data)