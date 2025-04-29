#####################################################################################################################################
# USD Outliner | Core
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON


# ADDONS
from imgui_bundle import imgui

# PROJECT
import core.static.static_core as cstat
import core.utils_core as cutils

#####################################################################################################################################


class Node:
    """
    Class representing a prototype node.
    """
    def __init__(self, source_object: dict, parent_node: 'Node', path):
        self.source_object = source_object
        self.parent_node = parent_node
        self.child_list: list[dict] = []
        self.input_list: list['Node'] = []
        self.output_list: list['Node'] = []
        self.item_type = source_object['type']
        self.item_name = source_object['name']
        self.item_path = source_object['path']
        self.floating = False
        self.drop_target = False

    def _set_attributes(self, source_object: dict):
        pass

    def add_child(self, child: 'Node'):
        if child not in self.child_list:
            self.child_list.append(child)

    def add_input(self, input_node: 'Node'):
        """
        Add an input node to the node.
        """
        if input_node not in self.input_list:
            self.input_list.append(input_node)

    def add_output(self, output_node: 'Node'):
        """
        Add an output node to the node.
        """
        if output_node not in self.output_list:
            self.output_list.append(output_node)





class MeshNode(Node):
    """
    Class representing a mesh node.
    """
    def __init__(self, source_object: dict, parent_node: Node):
        super().__init__(source_object, parent_node)


class LightNode(Node):
    """
    Class representing a light node.
    """
    def __init__(self, source_object: dict, parent_node: Node):
        super().__init__(source_object, parent_node)


class CameraNode(Node):
    """
    Class representing a camera node.
    """
    def __init__(self, source_object: dict, parent_node: Node):
        super().__init__(source_object, parent_node)


class BoneNode(Node):
    """
    Class representing a bone node.
    """
    def __init__(self, source_object: dict, parent_node: Node):
        super().__init__(source_object, parent_node)


class NullNode(Node):
    """
    Class representing a null node.
    """
    def __init__(self, source_object: dict, parent_node: Node):
        super().__init__(source_object, parent_node)


class LocatorNode(Node):
    """
    Class representing a locator node.
    """
    def __init__(self, source_object: dict, parent_node: Node):
        super().__init__(source_object, parent_node)


class MaterialNode(Node):
    """
    Class representing a material node.
    """
    def __init__(self, source_object: dict, parent_node: Node):
        super().__init__(source_object, parent_node)


class TextureNode(Node):
    """
    Class representing a texture node.
    """
    def __init__(self, source_object: dict, parent_node: Node):
        super().__init__(source_object, parent_node)




class NodeAttribute:
    """
    Class representing a property of an node.
    """
    def __init__(self, data: Any, data_type: str):
        self.data = data
        self.data_type = data_type






#####################################################################################################################################

class Panel:
    """
    Class representing a panel in the outliner.
    """
    def __init__(self, name: str):
        self.name = name
        self._init_render_context()

    def _set_panel_default_style(self):
        """
        Set the default style for the panel.
        """
        pass

    def _load_config(self):
        """
        Load the configuration file.
        """
        pass

    def _init_render_context(self):
        """
        Initialize the renderer for the panel.
        """
        self._render_manager = RenderContextManager()
        self._context = self._render_manager.context_list[-1]

    def _draw(self):
        """
        Draw the panel in the outliner.
        """
        imgui.set_current_context(self._context)
        self.draw()

    def draw(self):
        """
        Draw the panel in the outliner.
        """
        raise NotImplementedError("The 'draw' method must be implemented by subclasses.")




class DetailsPanel(Panel):
    """
    Class representing the details panel in the outliner.
    """
    def __init__(self, source_object: dict, parent_object):
        super().__init__(source_object, parent_object)
        self.source_object = source_object
        self.parent_object = parent_object

    def draw(self):
        """
        Draw the details panel in the outliner.
        """
        imgui.begin("Details Panel")
        imgui.text("Details Panel")
        imgui.end()


class TimelinePanel(Panel):
    """
    Class representing the timeline panel in the outliner.
    """
    def __init__(self, source_object: dict, parent_object):
        super().__init__(source_object, parent_object)
        self.source_object = source_object
        self.parent_object = parent_object

    def draw(self):
        """
        Draw the timeline panel in the outliner.
        """
        imgui.begin("Timeline Panel")
        imgui.text("Timeline Panel")
        imgui.end()



class RenderContextManager:
    """Render/Context manager."""
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
        """Initialize the renderer."""
        imgui.set_current_context(self.context_list[-1])
        imgui.backends.opengl3_init("#version 330")

    def remove_context(self, context):
        """Remove a context from the context list."""
        if context in self.context_list:
            self.context_list.remove(context)
            imgui.set_current_context(context)
            imgui.backends.opengl3_shutdown()
            imgui.destroy_context(context)
    