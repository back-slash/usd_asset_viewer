#####################################################################################################################################
# USD Outliner | Core
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON
from typing import Any


# ADDONS
from imgui_bundle import imgui
import pxr.Usd as pusd

# PROJECT
import core.static.static_core as cstat
import core.utils_core as cutils

#####################################################################################################################################


class Node:
    """
    Class representing a prototype node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        self._parent_node = parent_node
        self._path = path        
        self._data_object = data_object
        self._child_list = []
        self._input_list = []
        self._output_list = []
        self._attribute_list = []

    def _add_attributes(self, attribute: 'NodeAttribute'):
        """
        Add an output node to the node.
        """
        if attribute not in self._attribute_list:
            self._attribute_list.append(attribute)

    def _add_child(self, child: 'Node'):
        if child not in self._child_list:
            self._child_list.append(child)

    def _add_input(self, input_node: 'Node'):
        """
        Add an input node to the node.
        """
        if input_node not in self._input_list:
            self._input_list.append(input_node)

    def _add_output(self, output_node: 'Node'):
        """
        Add an output node to the node.
        """
        if output_node not in self._output_list:
            self._output_list.append(output_node)

    def _draw(self):
        """
        Draw the node.
        """
        pass

    def get_path(self) -> pusd.SdfPath:
        """
        Get the path of the node.
        """
        return self._path

    def get_parent_node(self) -> 'Node':
        """
        Get the parent node.
        """
        return self._parent_node
    
    def get_child_nodes(self) -> list['Node']:
        """
        Get the child nodes.
        """
        return self._child_list
    
    def get_input_nodes(self) -> list['Node']:
        """
        Get the input nodes.
        """
        return self._input_list

    def get_output_nodes(self) -> list['Node']:
        """
        Get the output nodes.
        """
        return self._output_list
    




class MeshNode(Node):
    """
    Class representing a mesh node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class LightNode(Node):
    """
    Class representing a light node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class CameraNode(Node):
    """
    Class representing a camera node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class BoneNode(Node):
    """
    Class representing a bone node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class NullNode(Node):
    """
    Class representing a null node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class LocatorNode(Node):
    """
    Class representing a locator node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class MaterialNode(Node):
    """
    Class representing a material node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class TextureNode(Node):
    """
    Class representing a texture node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class CurveNode(Node):
    """
    Class representing a curve node.
    """
    def __init__(self, parent_node: 'Node', path: pusd.SdfPath, data_object: Any):
        super().__init__(parent_node, path, data_object)
        self._node_color = (0.4, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icons.MESH_ICON


class NodeAttribute:
    """
    Class representing a property of an node.
    """
    def __init__(self, parent_node: 'Node', data_object: Any):
        self._parent_node = parent_node
        self._data_object = data_object

    def get_data(self) -> Any:
        """
        Get the data of the attribute.
        """
        return self._data_object






#####################################################################################################################################

class Frame:
    """
    Class representing a the tool frame.
    """
    def __init__(self, name: str):
        self.name = name
        self._panel_list = []
        
    def _init_render_context(self):
        """
        Initialize the renderer for the panel.
        """
        self._render_manager = RenderContextManager()
        self._context = self._render_manager.context_list[-1]

    def _load_config(self):
        """
        Load the configuration file.
        """
        imgui.set_current_context(self._context)
        self._config = cutils.read_from_file(self._config_path, cstat.Filetype.TOML)

    def remove_panel(self, panel: 'Panel'):
        """
        Remove a panel from the frame.
        """
        if panel in self._panel_list:
            self._panel_list.remove(panel)

    def add_panel(self, panel: 'Panel'):
        """
        Add a panel to the frame.
        """
        if panel not in self._panel_list:
            self._panel_list.append(panel)
        else:
            self.remove_panel(panel)
            self.add_panel(panel)


class Panel:
    """
    Class representing a panel in the outliner.
    """
    def __init__(self, name: str, frame: Frame, size: tuple[int, int], position: tuple[int, int]):
        self._frame = frame
        self._name = name
        self._set_panel_default_style()

    def _set_panel_default_style(self):
        """
        Set the default style for the panel.
        """
        pass

    def _draw(self):
        """
        Draw the panel in the outliner.
        """
        self.draw()

    def draw(self):
        """
        Draw the panel in the outliner.
        """
        raise NotImplementedError("The 'draw' method must be implemented by subclasses.")


#####################################################################################################################################

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
    