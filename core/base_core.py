#####################################################################################################################################
# USD Asset Viewer | Core | Base
# TODO:
#
#####################################################################################################################################
# PYTHON
from typing import Any
import os
import ctypes
import sys

# ADDONS
from attr import has
from imgui_bundle import imgui
import pxr.Usd as pusd
import pxr.Gf as pgf
import pxr.Sdf as psdf
import pxr.UsdGeom as pgeo
import pxr.UsdShade as pshd
import pxr.UsdLux as plux
import pxr.UsdSkel as pskl
import pxr.UsdUtils as putils
import glfw
import OpenGL.GL as gl

# PROJECT
import core.static_core as cstat
import core.utils_core as cutils

#####################################################################################################################################


class Node:
    """
    Class representing a node.
    """
    _node_color = (0.5, 0.5, 0.5, 1.0)
    _node_icon = cstat.Icon.UNKNOWN_ICON
    _name = None
    def __init__(self, data_object):
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

    def get_icon(self) -> cstat.Icon:
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
    _parent_node = None    
    _path = None
    def __init__(self, data_object):
        super().__init__(data_object)
        
    def _init_node_data(self):
        self._set_name()
        self._data_object: pusd.Prim | pusd.Attribute
        self._path = self._data_object.GetPath()
        parent_path = self._path.GetParentPath()
        self._parent_node = self._scene_manager.get_stage().GetPrimAtPath(parent_path)

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
    _attribute_list: list['Attribute'] = []   
    _child_list: list['Pathed'] = []
    def __init__(self, data_object: pusd.Prim):
        super().__init__(data_object)

    def _init_node_data(self):
        super()._init_node_data()
        self._init_node_attributes()
        self._init_node_children()

    def _init_node_attributes(self):
        """
        Load the attributes of the node.
        """
        for attribute in self._data_object.GetAttributes():
            node_attribute = self._scene_manager.init_path_node(attribute)
            self._add_attribute(node_attribute)

    def _add_attribute(self, attribute: 'Attribute'):
        """
        Add an attribute to the node.
        """
        if attribute and attribute not in self._attribute_list:
            self._attribute_list.append(attribute)

    def _init_node_children(self):
        """
        Load the children of the node.
        """
        for child in self._data_object.GetChildren():
            node_child = self._scene_manager.init_path_node(child)
            self._add_child(node_child)

    def _add_child(self, child: 'Node'):
        """
        Add a child node to the node.
        """
        if child and child not in self._child_list:
            self._child_list.append(child)

    def get_child_nodes(self) -> list['Node']:
        """
        Get the child nodes.
        """
        return self._child_list   


class Attribute(Pathed):
    """
    Class representing an attribute of a node.
    """
    _connection_path_list: list['Attribute'] = []
    _connected = False
    def __init__(self, data_object):
        super().__init__(data_object)
        self._data_object: pusd.Attribute

    def _init_node_data(self):
        super()._init_node_data()
        self._init_connections()

    def _init_connections(self) -> list[psdf.Path]:
        """
        Get any connections.
        """
        connection_paths = self._data_object.GetConnections()
        for path in connection_paths:
            if path.IsPropertyPath():
                pass
                #self._add_connection(path)
        if self._connection_path_list:
            self._connected = True

    def _add_connection(self, path: psdf.Path):
        """
        Add an input node to the node.
        """
        attribute = self._scene_manager.get_stage().GetPrimAtPath(path)
        attribute_node = self._scene_manager.init_path_node(attribute)
        if attribute_node and attribute_node not in self._connection_path_list:
            self._connection_path_list.append(attribute_node)

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
        self._data_object: pgeo.Xform

    def _init_node_data(self):
        super()._init_node_data()
        self._node_color = (0.4, 0.8, 0.4, 1.0)
        self._node_icon = cstat.Icon.NULL_ICON


class Mesh(Primative):
    """
    Class representing a mesh node.
    """
    _display_color = None
    def __init__(self, data_object):
        super().__init__(data_object)
        self._data_object: pgeo.Mesh

    def _init_node_data(self):
        super()._init_node_data()
        self._data_object = pgeo.Mesh(self._data_object)  
        self._node_color = (0.8, 0.4, 0.4, 1.0)
        self._node_icon = cstat.Icon.MESH_ICON
        self._display_color = self._data_object.GetDisplayColorAttr()
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
        self._node_icon = cstat.Icon.LIGHT_ICON


class Camera(Primative):
    """
    Class representing a camera node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()    
        self._node_color = (0.4, 0.4, 0.8, 1.0)
        self._node_icon = cstat.Icon.CAMERA_ICON


class Skeleton(Primative):
    """
    Class representing a skeleton node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()
        self._data_object = pskl.Skeleton(self._data_object)
        self._node_color = (0.6, 0.4, 0.8, 1.0)
        self._node_icon = cstat.Icon.SKELETON_ICON
        self._init_skeleton_bones()

    def _init_skeleton_bones(self):
        """
        Load the skeleton of the node.
        """
        bone_attribute = self._data_object.GetJointsAttr()
        bone_token_list = bone_attribute.Get()


class Material(Primative):
    """
    Class representing a material node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()    
        self._node_color = (0.8, 0.4, 0.6, 1.0)
        self._node_icon = cstat.Icon.MATERIAL_ICON

    def _init_textures(self):
        """
        Load the textures of the material node.
        """


class Curve(Primative):
    """
    Class representing a curve node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)

    def _init_node_data(self):
        super()._init_node_data()
        self._node_color = (0.8, 0.8, 0.4, 1.0)
        self._node_icon = cstat.Icon.CURVE_ICON


class Data(Node):
    """
    Class representing a data node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)

    def _init_node_data(self):
        self._set_name(self._data_object["name"])
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
    def __init__(self, data_object):
        super().__init__(data_object)

    def _init_node_data(self):
        super()._init_node_data()
        self._node_color = (0.4, 0.8, 0.8, 1.0)
        self._node_icon = cstat.Icon.TEXTURE_ICON


class Bone(Data):
    """
    Class representing a bone node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)

    def _init_node_data(self):
        super()._init_node_data()
        self._node_color = (0.8, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icon.BONE_ICON


#####################################################################################################################################


class Pencil:
    """
    Class representing an draw pencil.
    """
    _node_name = None
    _node_icon = None
    _node_color = None
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

    def _internal_draw(self):
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
        self._internal_draw()



#####################################################################################################################################


class Frame:
    """
    Class representing the tool frame.
    """
    _config = None
    _render_context_manager = None
    _display_size = None
    def __init__(self):
        self._init_config()
        self._init_render_context_manager()
        self._init_default_font()
        self._init_panels()
        self._init_pre_rendering()
        
    def _init_config(self):
        """
        Initialize the configuration file.
        """
        self._cfg = cutils.get_core_config()

    def _init_scene_manager(self):
        """
        Initialize the scene manager.
        """
        self._default_usd_path = os.path.join(cutils.get_usd_default_path(), self._cfg['settings']['default_usd'])   
        self._scene_manager = SceneManager()

    def _init_render_context_manager(self):
        """
        Initialize the render manager.
        """
        self._render_context_manager = RenderContextManager(self.update_draw)
        self._window = self._render_context_manager.get_window()
        self._context = self._render_context_manager.context_list[-1]
        self._display_size = self._render_context_manager.get_frame_size()
        glfw.set_window_close_callback(self._window, self._shutdown)

    def _init_panels(self):
        """
        Initialize the frame panels.
        """
        raise NotImplementedError("The '_init_panels' method must be implemented by Frame subclasses.")

    def _init_pre_rendering(self):
        """
        Initialize the frame panels.
        """
        raise NotImplementedError("The '_init_pre_rendering' method must be implemented by Frame subclasses.")        

    def _init_rendering(self):
        """
        Initialize the rendering context.
        """
        imgui.backends.opengl3_new_frame()
        self._render_context_manager.get_glfw().begin_render_loop()

    def _push_default_style(self):
        """
        Set the default style for the frame.
        """
        imgui.get_io().font_global_scale = self._cfg['window']['font_scale']

        cutils.push_style_var(self._cfg['window']['style_var'], 'item_spacing')
        cutils.push_style_var(self._cfg['window']['style_var'], 'window_padding')
        cutils.push_style_var(self._cfg['window']['style_var'], 'window_border_size')
        cutils.push_style_var(self._cfg['window']['style_var'], 'window_rounding')
        cutils.push_style_var(self._cfg['menu_bar']['style_var'], 'popup_rounding')
        cutils.push_style_var(self._cfg['menu_bar']['style_var'], 'popup_border_size')

        cutils.push_style_color(self._cfg['window']['style_color'], 'window_bg')
        cutils.push_style_color(self._cfg['window']['style_color'], 'border')
        cutils.push_style_color(self._cfg['window']['style_color'], 'text')
        cutils.push_style_color(self._cfg['header']['style_color'], 'header')
        cutils.push_style_color(self._cfg['header']['style_color'], 'header_hovered')
        cutils.push_style_color(self._cfg['header']['style_color'], 'header_active')
        cutils.push_style_color(self._cfg['title']['style_color'], 'title_bg')
        cutils.push_style_color(self._cfg['title']['style_color'], 'title_bg_active')
        cutils.push_style_color(self._cfg['menu_bar']['style_color'], 'menu_bar_bg')

    def _pop_default_style(self):
        """
        Pop the default style for the frame.
        """
        imgui.pop_style_var(6)
        imgui.pop_style_color(9)

    def _set_config_flags(self):
        """
        Set the flags for the frame.
        """
        cutils.set_flag(imgui.ConfigFlags_.docking_enable, self._cfg['config']['docking'])

    def _init_default_font(self):
        """
        Create the default font for the frame.
        """
        font_path = os.path.join(cutils.get_font_path(), "arial.ttf")
        self._font_tiny = imgui.get_io().fonts.add_font_from_file_ttf(font_path, self._cfg['window']['font_size_tiny'])
        self._font_small = imgui.get_io().fonts.add_font_from_file_ttf(font_path, self._cfg['window']['font_size_small'])
        self._font_medium = imgui.get_io().fonts.add_font_from_file_ttf(font_path, self._cfg['window']['font_size_medium'])
        self._font_large = imgui.get_io().fonts.add_font_from_file_ttf(font_path, self._cfg['window']['font_size_large'])

    def _set_window_flags(self):
        self._window_flags = 0
        for flag in self._cfg['window']['flags']:
            self._window_flags = cutils.set_window_flag(self._window_flags, self._cfg['window']['flags'], flag)

    def _internal_draw(self):
        """
        Draw the frame and its panels.
        """
        imgui.set_current_context(self._context)
        self._set_config_flags()
        self._set_window_flags()
        self._push_default_style()
        imgui.new_frame()
        imgui.push_font(self._font_small)
        self.draw()
        imgui.pop_font()
        self._pop_default_style()
        imgui.render()
        self._render_context_manager.render(imgui.get_draw_data(), self._context)

    def draw(self):
        """
        Draw the frame.
        """
        raise NotImplementedError("The 'draw' method must be implemented by subclasses.")
        
    def update_draw(self):
        """
        Update the frame.
        """
        self._internal_draw()

    def get_window(self):
        """
        Get the window of the frame.
        """
        return self._window

    def get_usable_space(self) -> tuple[int, int]:
        """
        Get the usable space for the panels.
        """
        display_size = imgui.get_io().display_size
        return display_size

    def _stop_rendering(self):
        """
        Stop the rendering loop.
        """
        if self._render_context_manager is not None:
            self._render_context_manager

    def _shutdown(self, *args):
        """
        Shutdown the frame and its panels.
        """
        self._render_context_manager.remove_context(self._context)


#####################################################################################################################################

class Panel:
    """
    Class representing a panel.
    """
    def __init__(self, name: str, frame: Frame):
        self._name = name
        self._frame = frame
        self._init_config()
        self._init_scene_manager()

    def _init_config(self):
        """
        Initialize the configuration file.
        """
        self._cfg = cutils.get_core_config()

    def _init_scene_manager(self):
        """
        Initialize the scene manager.
        """
        self._scene_manager = SceneManager()
        self._stage = self._scene_manager.get_stage()

    def _init_stage_data(self):
        """
        Initialize the stage data.
        """

    def _update_stage_data(self):
        """
        Update the stage data.
        """

    def _set_window_flags(self):
        self._window_flags = 0
        for flag in self._cfg[self._name]['flags']:
            self._window_flags = cutils.set_window_flag(self._window_flags, self._cfg[self._name]['flags'], flag)

    def _push_panel_style(self):
        for style in self._cfg[self._name]['style_color']:
            cutils.push_style_color(self._cfg[self._name]['style_color'], style)
        for style in self._cfg[self._name]['style_var']:
            cutils.push_style_var(self._cfg[self._name]['style_var'], style)

    def _pop_panel_style(self):
        imgui.pop_style_color(len(self._cfg[self._name]['style_color']))
        imgui.pop_style_var(len(self._cfg[self._name]['style_var']))

    def _calc_panel_rect(self):
        """
        Calculate the panel rectangle.
        """
        window_position = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        rect = (window_position.x, window_position.y, window_position.x + window_size.x, window_position.y + window_size.y)
        return rect

    def _internal_draw(self):
        """
        Draw the panel.
        """
        rect = self.draw()
        return rect

    def draw(self):
        """
        Draw the panel.
        """
        raise NotImplementedError("The 'draw' method must be implemented by subclasses.")

    def update_draw(self, position: tuple[int, int], size: tuple[int, int]) -> tuple[int, int, int, int]:
        """
        Update the frame.
        """
        self._panel_width = size[0]
        self._panel_height = size[1]
        self._panel_position = position
        self._update_stage_data()
        self._set_window_flags()
        self._push_panel_style()
        self._internal_draw()
        rect = self._calc_panel_rect()
        self._pop_panel_style()
        imgui.end()
        return rect

    def update_usd(self):
        """
        Update the USD stage.
        """
        self._init_scene_manager()

    def shutdown(self):
        """
        Shutdown the panel.
        """

#####################################################################################################################################

class Viewport(Panel):
    """
    Class representing the viewport panel.
    """
    def __init__(self, name: str, frame: Frame):
        super().__init__(name, frame)
        self._viewport_size = (0, 0)
        self._viewport_position = (0, 0)

    def draw(self):
        """
        Draw the viewport panel.
        """
        imgui.begin(self._name, True, self._frame._window_flags)
        imgui.text("Viewport")
        imgui.end()

#####################################################################################################################################

class SceneManager:
    """
    Class for managing scene nodes.
    """
    _instance = None
    _usd_path = None
    _root = None
    def __new__(cls, usd_path: str=None):
        if cls._instance is None:
            cls._initialized = False
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
        if usd_path:
            self.set_usd_file(usd_path)
    
    def _init_usd_scene(self):
        """
        Initialize USD scene.
        """
        self._stage: pusd.Stage = pusd.Stage.Open(self._usd_path)
        self._root = self._stage.GetPseudoRoot()
        self._traverse_hierarchy()

    def _traverse_hierarchy(self):
        """
        Traverse the hierarchy and init nodes.
        """
        for self._temp_prim in self._stage.Traverse():
            internal_node = self._init_internal_node(self._temp_prim)
            self._add_path_node(internal_node)
            for self._temp_attribute in self._temp_prim.GetAttributes():
                internal_attribute = self._init_internal_node(self._temp_attribute)
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

        
        if isinstance(input_object, pusd.Attribute):
            return Attribute(input_object)
        input_object_type = str(input_object.GetTypeName())
        if input_object_type in prim_classes:
            return prim_classes[input_object_type](input_object)
        return None

    def _init_internal_data(self, data_object: dict[str, str | pusd.Prim]) -> Data:
        """
        Get appropriate data type and init.
        """
        if isinstance(data_object["owner"], pskl.Skeleton):
            return Skeleton(data_object)
        elif isinstance(data_object["owner"], pshd.Material):
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
        if node and node not in self._path_node_list:
            self._path_node_list.append(node)

    def _add_data_node(self, node: Data):
        """
        Add a data node to the scene manager.
        """
        if node and node not in self._data_node_list:
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
            print(f"Unknown data object type: {data_object.GetTypeName()}")
            return None
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
            print(f"Unknown data object type: {data_object['owner'].GetTypeName()}")
        self._add_data_node(data_node)
        return data_node

    def get_stage(self) -> pusd.Stage:
        """
        Get the USD stage.
        """
        if hasattr(self, "_stage"):
            return self._stage

    def set_usd_file(self, usd_path: str):
        """
        Set the USD file for the scene manager.
        """
        self._usd_path = usd_path
        self._path_node_list = []
        self._data_node_list = []        
        self._init_usd_scene()

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
            self._glfw.stop_render_loop()
            self.context_list.remove(context)
            imgui.set_current_context(context)
            imgui.backends.glfw_shutdown()
            imgui.backends.opengl3_shutdown()
            imgui.destroy_context(context)
            imgui.destroy_platform_windows()


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

    def get_window(self):
        """
        Get the GLFW window.
        """
        return self._glfw_window

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
    _should_render = True
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
        while not glfw.window_should_close(self._window) and self._should_render:
            self._set_imgui_window_size()
            glfw.poll_events()
            gl.glClearColor(*self._cfg_gl_color)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            self._render_loop_function()
            glfw.swap_buffers(self._window)
        self._shutdown()

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

    def stop_render_loop(self):
        """
        Stop the render loop.
        """
        self._should_render = False

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
    
    def _shutdown(self):
        """
        Shutdown the GLFW window.
        """
        glfw.terminate()
        sys.exit()      