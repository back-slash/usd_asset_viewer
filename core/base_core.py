#####################################################################################################################################
# USD Outliner | Core | Base
# TODO:
#
#####################################################################################################################################
# PYTHON
from typing import Any
import os

# ADDONS
from imgui_bundle import imgui
import pxr.Usd as pusd
import pxr.Gf as pgf
import pxr.Sdf as psdf
import pxr.UsdGeom as pgeo
import pxr.UsdShade as pshd
import pxr.UsdLux as plux
import pxr.UsdSkel as pskl
import pxr.UsdUtils as putils


# PROJECT
import core.static.static_core as cstat
import core.utils_core as cutils
import core.render_core as crend
#####################################################################################################################################


class Node:
    """
    Class representing a node.
    """
    _parent_node = None
    _data_object = None
    _node_color = None
    _node_icon = None
    _pencil_list: list['Pencil'] = []
    _name = None
    def __init__(self, data_object: pusd.Prim=None):
        self._data_object: pusd.Prim = data_object
        self._parent_node = self._data_object.GetParent()
        self._data_object_type = data_object.GetTypeName()
        self._init_scene_manager()
        self._init_generic_data()

    def _init_scene_manager(self):
        """
        Initialize the scene manager.
        """
        self._scene_manager = SceneManager()

    def _init_generic_data(self):
        """
        Set the default values for the node.
        """

    def _attach_pencil(self, pencil_class: 'Pencil', position: tuple[int, int]=None, size: tuple[int, int]=None):
        """
        Attach the pencil to the node.
        """
        self._pencil_list.append(pencil_class(self, position, size))

    def update_pencil_list(self):
        """
        Update data and pencil.
        """
        for pencil in self._pencil_list:
            pencil.update_draw()

    def get_parent_node(self) -> 'Node':
        """
        Get the parent node.
        """
        return self._parent_node
    
    def get_data_object(self) -> pusd.Prim:
        """
        Get the data object of the node.
        """
        return self._data_object

    def get_scene_manager(self) -> 'SceneManager':
        """
        Get the scene manager.
        """
        return self._scene_manager

    def get_icon(self) -> cstat.NodeIcon:
        """
        Get the icon of the node.
        """
        return self._node_icon
    
    def get_name(self) -> str:
        """
        Get the name of the node.
        """
        return self._name
    



class PathNode(Node):
    """
    Class representing a path node.
    """
    _path = None
    def __init__(self, data_object: pusd.Prim):
        super().__init__(data_object)
        self._init_node_children()
        self._path = self._data_object.GetPath()
    
    def _init_generic_data(self):
        super()._init_generic_data()
        self._name = self._data_object.GetName()

    def _init_node_children(self):
        """
        Load the children of the node.
        """
        self._child_list = []
        for child in self._data_object.GetChildren():
            node_child = Node(self, child)
            self._add_child(node_child)

    def _add_child(self, child: 'Node'):
        """
        Add a child node to the node.
        """
        if child not in self._child_list:
            self._child_list.append(child)

    def get_child_nodes(self) -> list['Node']:
        """
        Get the child nodes.
        """
        return self._child_list   

    def get_path(self) -> psdf.Path:
        """
        Get the path of the node.
        """
        return self._path


class Primative(PathNode):
    """
    Class representing a primitive node.
    """
    _input_list = []
    _output_list = []
    _child_list = []
    _attribute_list = []   
    _display_color = None
    _opacity = 1.0
    def __init__(self, data_object: pusd.Prim):
        super().__init__(data_object)
        self._data_object: pusd.Prim #Hacky
        self._init_node_attributes()

    def _init_generic_data(self):
        super()._init_generic_data()
        display_color_attr = self._data_object.GetAttribute('displayColor').Get()
        visibility_attr = self._data_object.GetAttribute('visibility')
        self._opacity = visibility_attr.Get() != 'invisible' if visibility_attr else True

    def _init_node_attributes(self):
        """
        Load the attributes of the node.
        """
        self._attribute_list: list[Attribute] = []
        for attribute in self._data_object.GetAttributes():
            node_attribute = Attribute(self, attribute)
            self._add_attribute(node_attribute)

    def _add_attribute(self, attribute: 'Attribute'):
        """
        Add an attribute to the node.
        """
        if attribute not in self._attribute_list:
            self._attribute_list.append(attribute)

    def get_display_color(self) -> tuple[float, float, float, float]:
        """
        Get the display color of the node.
        """
        return self._display_color 


class Attribute(PathNode):
    """
    Class representing an attribute of a node.
    """
    _connected = False
    def __init__(self, data_object: pusd.Attribute):
        super().__init__(data_object)
        self._parent_node = data_object.GetPrim()
        self._data_object: pusd.Attribute = data_object

    def _init_generic_data(self):
        super()._init_generic_data()
        self._name = self._data_object.GetName()

    def _init_connections(self) -> list[psdf.Path]:
        """
        Get any connections.
        """
        self._connection_paths = []
        connection_paths = self._data_object.GetConnections()
        for path in connection_paths:
            if path.IsPropertyPath():
                self._add_connection(path)
        if self._connection_paths:
            self._connected = True

    def _add_connection(self, path: psdf.Path):
        """
        Add an input node to the node.
        """
        attribute = self._scene_manager.get_stage().GetPrimAtPath(path.pathString)
        attribute_node = Attribute(attribute)
        if attribute_node not in self._connection_paths:
            self._connection_paths.append(attribute_node)

    def get_data(self, time: float = None) -> Any:
        """
        Get the data of the attribute.
        """
        return self._data_object.Get(time)
    
    def get_data_type(self):
        """
        Get the type of the attribute.
        """
        data_type = self._data_object.GetTypeName()
        data_type_dict = {
            'float': float,
            'double': float,
            'int': int,
            'bool': bool,
            'string': str,
            'token': str,
            'vector3d': pgf.Vec3d,
            'vector4d': pgf.Vec4d,            
            'matrix3d': pgf.Matrix3d,
            'matrix4d': pgf.Matrix4d,
        }
        return data_type_dict[data_type]


class Mesh(Primative):
    """
    Class representing a mesh node.
    """
    def __init__(self, data_object: pusd.Prim):
        super().__init__(data_object)
        self._node_color = (0.8, 0.4, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.MESH_ICON
        self._init_materials()

    def _init_materials(self):
        """
        Load the materials of the mesh node.
        """


class Light(Primative):
    """
    Class representing a light node.
    """
    def __init__(self, data_object: plux.DistantLight):
        super().__init__(data_object)
        self._node_color = (0.9, 0.9, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.LIGHT_ICON


class Camera(Primative):
    """
    Class representing a camera node.
    """
    def __init__(self, data_object: pgeo.Camera):
        super().__init__(data_object)
        self._node_color = (0.4, 0.4, 0.8, 1.0)
        self._node_icon = cstat.NodeIcon.CAMERA_ICON


class Skeleton(Primative):
    """
    Class representing a skeleton node.
    """
    def __init__(self, data_object: pskl.Skeleton):
        super().__init__(data_object)
        self._node_color = (0.6, 0.4, 0.8, 1.0)
        self._node_icon = cstat.NodeIcon.SKELETON_ICON
    
    def _init_skeleton_bones(self):
        """
        Load the skeleton of the node.
        """


class Material(Primative):
    """
    Class representing a material node.
    """
    def __init__(self, data_object: pshd.Material):
        super().__init__(data_object)
        self._node_color = (0.8, 0.4, 0.6, 1.0)
        self._node_icon = cstat.NodeIcon.MATERIAL_ICON

    def _init_textures(self):
        """
        Load the textures of the material node.
        """

class Curve(Primative):
    """
    Class representing a curve node.
    """
    def __init__(self, data_object: pgeo.BasisCurves):
        super().__init__(data_object)
        self._node_color = (0.8, 0.8, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.CURVE_ICON


class Data(Node):
    """
    Class representing a data node.
    """
    def __init__(self, data_object_owner: pusd.Prim=None, relative_path: str=None):
        self._parent_node = data_object_owner
        self._relative_path = relative_path

    def get_relateive_path(self) -> str:
        """
        Get the relative path of the node.
        """
        return self._relative_path


class Texture(Data):
    """
    Class representing a texture node.
    """
    def __init__(self, data_object_owner: pusd.Prim, data_object: str, relative_path: str):
        super().__init__(data_object_owner, data_object, relative_path)
        self._node_color = (0.4, 0.8, 0.8, 1.0)
        self._node_icon = cstat.NodeIcon.TEXTURE_ICON


class Bone(Data):
    """
    Class representing a bone node.
    """
    def __init__(self, data_object_owner: pusd.Prim, data_object: dict, relative_path: str):
        super().__init__(data_object_owner, data_object, relative_path)
        self._node_color = (0.8, 0.6, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.BONE_ICON


#####################################################################################################################################


class Pencil:
    """
    Class representing an draw pencil.
    """
    def __init__(self, node: Node, position: tuple[int, int]=None, size: tuple[int, int]=None):
        self._node = node
        self._position = position
        self._size = size
        self._init_node_data()

    def _init_node_data(self):
        """
        Initialize the node data.
        """
        self._data_object = self._node.get_data_object()
        self._visible = self._data_object.IsActive() and self._data_object.IsDefined()
        self._name = self._data_object.GetName()
        self._path = self._data_object.GetPath()

    def _draw(self):
        """
        Draw the node.
        """

    def update_draw(self):
        """
        Update and draw the node.
        """


#####################################################################################################################################

class Frame:
    """
    Class representing the tool frame.
    """
    _config = None
    def __init__(self, title: str):
        self.title = title
        self._init_panels()
        
    def _init_render_context(self):
        """
        Initialize the renderer for the panel.
        """
        self._render_manager = crend.RenderContextManager()
        self._context = self._render_manager.context_list[-1]

    def _init_panels(self):
        """
        Initialize the frame panels.
        """
        raise NotImplementedError("The '_init_panels' method must be implemented by subclasses.")

    def _load_config(self):
        """
        Load the configuration file.
        """
        directory = os.path.join(os.path.dirname(__file__), "static" "config_core.toml")
        if os.path.exists(directory):
            self._config: dict = cutils.FileHelper.read(directory, cstat.Filetype.TOML)

    def _push_default_style(self):
        """
        Set the default style for the frame.
        """

    def _pop_default_style(self):
        """
        Pop the default style for the frame.
        """

    def _set_flags(self):
        """
        Set the flags for the frame.
        """
    
    def _draw(self):
        """
        Draw the frame and its panels.
        """
        imgui.set_current_context(self._context)
        self._push_default_style()
        imgui.new_frame()
        self.draw()
        self._pop_default_style()
        imgui.render()

    def draw(self):
        """
        Draw the frame.
        """
        raise NotImplementedError("The 'draw' method must be implemented by subclasses.")
        
    def update(self):
        """
        Update the frame.
        """
        self._draw()

#####################################################################################################################################

class Panel:
    """
    Class representing a panel.
    """
    def __init__(self, name: str, frame: Frame, context: imgui.internal.Context):
        self._frame = frame
        self._name = name
        self._context = context

    def _set_default_panel_style(self):
        """
        Set the default style for the panel.
        """
        pass

    def _draw(self, size: tuple[int, int], position: tuple[int, int]):
        """
        Draw the panel.
        """
        imgui.set_current_context(self._context)
        imgui.set_next_window_size(size[0], size[1])
        imgui.set_next_window_pos(position[0], position[1])
        self.draw()

    def draw(self):
        """
        Draw the panel.
        """
        raise NotImplementedError("The 'draw' method must be implemented by subclasses.")

    def update(self, size: tuple[int, int], position: tuple[int, int]):
        """
        Update the frame.
        """
        self._draw(size, position)


#####################################################################################################################################

class SceneManager:
    """
    Class for managing the scene.
    """
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, usd_path):
        if not self._initialized:
            self._usd_path = usd_path
            self._path_node_list: list[PathNode] = []
            self._data_node_list: list[Data] = []
            self._init_usd_scene()
            self._init_time_manager()
            self._initialized = True

    def _init_usd_scene(self):
        """
        Initialize the USD scene.
        """
        self._stage = pusd.Stage.Open(self._usd_path)
        self._root = self._stage.GetPseudoRoot()

    def _init_nodes(self):
        """
        Process the USD scene and init nodes.
        """
        for child in self._root.GetChildren():
            self._recursive_child_node(child)

    def _recursive_child_node(self, node: pusd.Prim):
        """
        Recursively process the USD scene and init nodes.
        """
        internal_node = self._init_node_type(node)
        if internal_node:
            self._add_path_node(internal_node)
            for attribute in node.GetAttributes():
                self._recursive_child_node(attribute)
            for child in node.GetChildren():
                self._recursive_child_node(child)
        
    def _init_node_type(self, node: pusd.Prim):
        """
        Get appropriate node type.
        """
        usd_node_types = {
            pgeo.Mesh: Mesh,
            plux.DistantLight: Light,
            pgeo.Camera: Camera,
            pskl.Skeleton: Skeleton,
            pshd.Material: Material,
            pgeo.BasisCurves: Curve,
        }
        for node_type, class_type in usd_node_types.items():
            if isinstance(node, node_type):
                internal_node = class_type(node)
                self._add_data_node(internal_node)
                return internal_node
        return None

    def _create_data_skeleton(self, skeleton: Skeleton):
        """
        Create a data skeleton from the USD skeleton.
        """

    def _init_time_manager(self):
        """
        Initialize the time manager.
        """
        self._current_time = self._stage.GetStartTimeCode()
        self._start_time = self._stage.GetStartTimeCode()
        self._end_time = self._stage.GetEndTimeCode()

    def _add_path_node(self, node: PathNode):
        """
        Add a node to the scene manager.
        """
        self._path_node_list.append(node)

    def _add_data_node(self, node: Data):
        """
        Add a data node to the scene manager.
        """
        self._data_node_list.append(node)

    def get_stage(self) -> pusd.Stage:
        """
        Get the USD stage.
        """
        return self._stage
    
    def get_root(self) -> pusd.Prim:
        """
        Get the root of the stage.
        """
        return self._root

    def get_current_time(self) -> float:
        """
        Get the current time.
        """
        return self._current_time

    def set_current_time(self, time: float):
        """
        Set the current time.
        """
        if self._start_time <= time <= self._end_time:
            self._current_time = time

    def get_time_range(self) -> tuple[float, float]:
        """
        Get the start and end time.
        """
        return self._start_time, self._end_time
    
    def get_path_node(self, path: psdf.Path) -> PathNode:
        """
        Get the path node by its path.
        """
        for node in self._path_node_list:
            if node.get_path() == path:
                return node
    
    def get_data_node(self, relative_path: str) -> Data:
        """
        Get the data node by its relative path.
        """
        for node in self._data_node_list:
            if node.get_relateive_path() == relative_path:
                return node