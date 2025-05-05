#####################################################################################################################################
# USD Asset Viewer | Core | Base
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
    _name = None
    def __init__(self, data_object: Any):
        self._data_object: pusd.Prim | dict = data_object
        self._init_scene_manager()
        self._init_node_data()

    def _init_scene_manager(self):
        """
        Initialize the scene manager.
        """
        self._scene_manager = SceneManager()

    def _init_node_data(self):
        """
        Set the default values for the node.
        """
        raise NotImplementedError("The '_init_node_data' method must be implemented by subclasses.")
    
    def _set_name(self, name: str=None):
        """
        Set the name of the node.
        """
        if name:
            self._name = name
        else:
            self._name = self._data_object.GetName()
    
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
    
    def get_color(self) -> tuple[float, float, float, float]:
        """
        Get the color of the node.
        """
        return self._node_color

    def get_name(self) -> str:
        """
        Get the name of the node.
        """
        return self._name


class Pathed(Node):
    """
    Class representing a path node.
    """
    _path = None
    def __init__(self, data_object: pusd.Prim | pusd.Attribute):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()
        self._set_name()
        self._parent_node = self._data_object.GetParent()
        self._path = self._data_object.GetPath()
        self._init_node_children()
        
    def _init_node_children(self):
        """
        Load the children of the node.
        """
        self._child_list = []
        for child in self._data_object.GetChildren():
            node_child = self._scene_manager.init_path_node(child)
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

    def get_parent_node(self) -> 'Node':
        """
        Get the parent node.
        """
        return self._parent_node

class Primative(Pathed):
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

    def _init_node_data(self):
        super()._init_node_data()
        self._init_node_attributes()

    def _init_node_attributes(self):
        """
        Load the attributes of the node.
        """
        self._attribute_list: list[Attribute] = []
        for attribute in self._data_object.GetAttributes():
            node_attribute = self._scene_manager.init_path_node(attribute)
            self._add_attribute(node_attribute)

    def _add_attribute(self, attribute: 'Attribute'):
        """
        Add an attribute to the node.
        """
        if attribute not in self._attribute_list:
            self._attribute_list.append(attribute)


class Attribute(Pathed):
    """
    Class representing an attribute of a node.
    """
    _connected = False
    def __init__(self, data_object: pusd.Attribute):
        super().__init__(data_object)
        self._data_object: pusd.Attribute

    def _init_node_data(self):
        super()._init_node_data()
        self._init_connections()

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
        attribute = self._scene_manager.get_stage().GetPrimAtPath(path)
        attribute_node = self._scene_manager.init_path_node(attribute)
        if attribute_node not in self._connection_paths:
            self._connection_paths.append(attribute_node)

    def get_data(self, time: float = None) -> Any:
        """
        Get the data of the attribute.
        """
        return self._data_object.Get(time)


class XForm(Primative):
    """
    Class representing a transform node.
    """
    def __init__(self, data_object: pgeo.Xform):
        super().__init__(data_object)

    def _init_node_data(self):
        super()._init_node_data()
        self._node_color = (0.4, 0.8, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.NULL_ICON


class Mesh(Primative):
    """
    Class representing a mesh node.
    """
    def __init__(self, data_object: pgeo.Mesh):
        super().__init__(data_object)

    def _init_node_data(self):
        super()._init_node_data()
        self._data_object: pgeo.Mesh
        self._display_color = self._data_object.GetDisplayColorAttr()        
        self._node_color = (0.8, 0.4, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.MESH_ICON
        self._init_materials()

    def _init_materials(self):
        """
        Load the materials of the mesh node.
        """
   
    def get_display_color(self) -> tuple[float, float, float, float]:
        """
        Get the display color of the node.
        """
        return self._display_color


class Light(Primative):
    """
    Class representing a light node.
    """
    def __init__(self, data_object: plux.BoundableLightBase | plux.NonboundableLightBase):
        super().__init__(data_object)

    def _init_node_data(self):
        super()._init_node_data()
        self._data_object: plux.BoundableLightBase | plux.NonboundableLightBase
        self._node_color = (0.9, 0.9, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.LIGHT_ICON



class Camera(Primative):
    """
    Class representing a camera node.
    """
    def __init__(self, data_object: pgeo.Camera):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()    
        self._node_color = (0.4, 0.4, 0.8, 1.0)
        self._node_icon = cstat.NodeIcon.CAMERA_ICON


class Skeleton(Primative):
    """
    Class representing a skeleton node.
    """
    def __init__(self, data_object: pskl.Skeleton):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()
        self._node_color = (0.6, 0.4, 0.8, 1.0)
        self._node_icon = cstat.NodeIcon.SKELETON_ICON
        self._init_skeleton_bones()

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
        
    def _init_node_data(self):
        super()._init_node_data()    
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
    def __init__(self, data_object: pgeo.Curves):
        super().__init__(data_object)
        self._node_color = (0.8, 0.8, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.CURVE_ICON


class Data(Node):
    """
    Class representing a data node.
    """
    def __init__(self, data_object: dict[str, pusd.Prim | str]):
        super().__init__(data_object)

    def _init_node_data(self):
        super()._init_node_data()
        self._parent_node: pusd.Prim = self._data_object["owner"]
        self._relative_path = self._data_object["relative_path"]

    def get_relateive_path(self) -> str:
        """
        Get the relative path of the node.
        """
        return self._relative_path


class Texture(Data):
    """
    Class representing a texture node.
    """
    def __init__(self, data_object: dict[str, pusd.Prim | str]):
        super().__init__(data_object)
        self._node_color = (0.4, 0.8, 0.8, 1.0)
        self._node_icon = cstat.NodeIcon.TEXTURE_ICON


class Bone(Data):
    """
    Class representing a bone node.
    """
    def __init__(self, data_object: dict[str, pusd.Prim | str]):
        super().__init__(data_object)
        self._node_color = (0.8, 0.6, 0.4, 1.0)
        self._node_icon = cstat.NodeIcon.BONE_ICON


#####################################################################################################################################


class Pencil:
    """
    Class representing an draw pencil.
    """
    _node_display_color = None
    def __init__(self, node: Node):
        self._node = node
        self._init_node_data()

    def _init_node_data(self):
        """
        Initialize the node data.
        """
        self._node_name = self._node.get_name()
        self._node_icon = self._node.get_icon()
        self._node_color = self._node.get_color()
        if hasattr(self._node, "get_display_color"):
            self._node_display_color = self._node.get_display_color()

    def _draw(self):
        """
        Draw the node.
        """

    def _update_transform(self, position: tuple[int, int]=None, size: tuple[int, int]=None):
        """
        Update the transform of the node.
        """
        if position:
            self._position = position
        if size:
            self._size = size

    def update_draw(self, size: tuple[int, int]=None, position: tuple[int, int]=None):
        """
        Update and draw the node.
        """
        self._update_transform(position, size)
        self._draw()



#####################################################################################################################################


class Frame:
    """
    Class representing the tool frame.
    """
    _config = None
    def __init__(self, title: str):
        self.title = title
        self._init_panels()
        
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
    def __init__(self, name: str, frame: Frame):
        self._name = name
        self._frame = frame

    def _set_default_panel_style(self):
        """
        Set the default style for the panel.
        """
        pass

    def _pop_default_panel_style(self):
        """
        Pop the default style for the panel.
        """
        pass

    def _draw(self, size: tuple[int, int], position: tuple[int, int]):
        """
        Draw the panel.
        """
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
    Class for managing scene nodes.
    """
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, usd_path: str=None):
        if usd_path and not self._initialized:
            self._usd_path = usd_path
            self._path_node_list: list[Pathed] = []
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
        self._traverse_hierarchy()

    def _traverse_hierarchy(self):
        """
        Traverse the hierarchy and init nodes.
        """
        for prim in self._stage.Traverse():
            internal_node = self._init_internal_node(prim)
            self._add_path_node(internal_node)
            for attribute in prim.GetAttributes():
                internal_attribute = self._init_internal_node(attribute)
                if internal_attribute and internal_attribute not in self._path_node_list:
                    self._add_path_node(internal_attribute)

        
    def _init_internal_node(self, input_object: pusd.Prim | pusd.Attribute) -> Node | None:
        """
        Get appropriate node type and init.
        """
        prim_classes = {
            "Xform": XForm,
            "Mesh": Mesh,
            "DistantLight": Light,
            "DiskLight": Light,
            "RectLight": Light,
            "SphereLight": Light,
            "DomeLight": Light,
            "CylinderLight": Light,
            "GeometryLight": Light,
            "ShapingAPI": Light,
            "LightPortal": Light,
            "Camera": Camera,
            "Skeleton": Skeleton,
            "Material": Material,
            "BasisCurves": Curve,
            "NurbsCurves": Curve,
        }

        attribute_classes = {
            "float": Attribute,
            "double": Attribute,
            "int": Attribute,
            "bool": Attribute,
            "string": Attribute,
            "token": Attribute,
            "vector3d": Attribute,
            "vector4d": Attribute,
            "matrix3d": Attribute,
            "matrix4d": Attribute,
        }

        input_object_type = str(input_object.GetTypeName())
        if input_object_type in attribute_classes:
            return attribute_classes[input_object_type](input_object)
        if input_object_type in prim_classes:
            return prim_classes[input_object_type](input_object)
        return None

    def _init_internal_data(self, data_object: dict[str, str | pusd.Prim]) -> Data:
        """
        Get appropriate data type and init.
        """
        if isinstance(data_object["owner"], pskl.Skeleton):
            return Skeleton(data_object)
        if isinstance(data_object["owner"], pshd.Material):
            return Material(data_object)
        else:
            return None

    def _init_time_manager(self):
        """
        Initialize the time manager.
        """
        self._current_time = self._stage.GetStartTimeCode()
        self._start_time = self._stage.GetStartTimeCode()
        self._end_time = self._stage.GetEndTimeCode()

    def _add_path_node(self, node: Pathed):
        """
        Add a node to the scene manager.
        """
        if node not in self._path_node_list:
            self._path_node_list.append(node)

    def _add_data_node(self, node: Data):
        """
        Add a data node to the scene manager.
        """
        if node not in self._data_node_list:
            self._data_node_list.append(node)

    def init_path_node(self, data_object: pusd.Prim) -> Pathed:
        """
        Initialize a path node and add it to the scene manager.
        """
        for path_node in self._path_node_list:
            if path_node.get_data_object() == data_object:
                return path_node
        path_node = self._init_internal_node(data_object)
        if not path_node:
            raise TypeError("Unknown data object type.")
        self._add_path_node(path_node)
        return path_node

    def init_data_object(self, data_object: dict[str, str | pusd.Prim]) -> Data:
        """
        Initialize a data object and add it to the scene manager.
        """
        for data_node in self._data_node_list:
            if data_node.get_data_object() == data_object:
                return data_node
        data_node = self._init_internal_data(data_object)
        if not data_node:
            raise TypeError("Unknown data object type.")
        self._add_data_node(data_node)
        return data_node

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
    
    def get_path_node(self, input: psdf.Path | pusd.Prim | pusd.Attribute) -> Pathed:
        """
        Get the path node from psdf.Path | pusd.Prim | pusd.Attributes.
        """
        if isinstance(input, pusd.Prim):
            for node in self._path_node_list:
                if node.get_data_object() == input:
                    return node
        elif isinstance(input, pusd.Attribute):
            for node in self._path_node_list:
                if node.get_data_object() == input:
                    return node
        elif isinstance(input, psdf.Path):
            for node in self._path_node_list:
                if node.get_path() == input:
                    return node
    
    def get_data_node(self, input: str) -> Data:
        """
        Get the data node by its relative path.
        """
        for node in self._data_node_list:
            if node.get_relateive_path() == input:
                return node
            elif node.get_name() == input:
                return node
