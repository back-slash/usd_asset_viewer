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
import pprint as pp
import math

# USD

# ADDONS
from imgui_bundle import imgui
import numpy as np
import pxr.Usd as pusd
import pxr.Gf as pgf
import pxr.Sdf as psdf
import pxr.UsdGeom as pgeo
import pxr.UsdShade as pshd
import pxr.UsdLux as plux
import pxr.UsdSkel as pskl
import pxr.UsdUtils as putils
import pxr.UsdImagingGL as pimg
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
    def __init__(self, data_object):
        self._visible = True
        self._selected = False
        self._hovered = False
        self._active = True
        self._node_color = (0.5, 0.5, 0.5, 1.0)
        self._node_icon = cstat.Icon.ICON_UNKNOWN
        self._name = None
        self._data_object: pusd.Prim | dict = data_object
        self._init_scene_manager()
        self._init_node_data()

    def _init_scene_manager(self):
        """
        Initialize the scene manager.
        """
        self._sm = SceneManager()

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
    
    def get_sm(self) -> 'SceneManager':
        """
        Get the scene manager.
        """
        return self._sm

    def is_visible(self) -> bool:
        """
        Check if the node is visible.
        """
        return self._visible
    
    def is_selected(self) -> bool:
        """
        Check if the node is selected.
        """
        return self._selected
    
    def is_hovered(self) -> bool:
        """
        Check if the node is hovered.
        """
        return self._hovered

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

    def __init__(self, data_object):
        self._parent_node = None    
        self._path = None
        self._prim_object = None        
        super().__init__(data_object)

    def _init_node_data(self):
        self._set_name()
        self._data_object: pusd.Prim | pusd.Attribute
        self._path = self._data_object.GetPath()
        parent_path = self._path.GetParentPath()
        self._parent_node = self._sm.get_stage().GetPrimAtPath(parent_path)
        self._prim_object = self._sm.get_stage().GetPrimAtPath(self._path)

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

    def get_prim(self) -> pusd.Prim:
        """
        Get the prim of the node.
        """
        return self._prim_object

class Primative(Pathed):
    """
    Class representing a primitive node.
    """

    def __init__(self, data_object: pusd.Prim):
        self._attribute_list: list['Attribute'] = []   
        self._child_list: list['Pathed'] = []
        super().__init__(data_object)


    def _init_node_data(self):
        super()._init_node_data()
        self._init_node_attributes()
        self._init_node_children()

    def _init_node_attributes(self):
        """
        Load the attributes of the node.
        """
        self._attribute_list = []
        for attribute in self._data_object.GetAttributes():
            node_attribute = self._sm.init_path_node(attribute)
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
        self._child_list = []
        for child in self._data_object.GetChildren():
            node_child = self._sm.init_path_node(child)
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


class Root(Primative):
    """
    Class representing the root node.
    """
    def __init__(self, data_object: pusd.Prim):
        super().__init__(data_object)
        self._data_object: pusd.Prim

    def _init_node_data(self):
        super()._init_node_data()
        self._node_color = (0.5, 0.5, 0.5, 1.0)
        self._node_icon = cstat.Icon.ICON_ROOT


class Attribute(Pathed):
    """
    Class representing an attribute of a node.
    """

    def __init__(self, data_object):
        self._connection_path_list: list['Attribute'] = []
        super().__init__(data_object)
        self._data_object: pusd.Attribute
        self._connected = False

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
                self._add_connection(path)
        if self._connection_path_list:
            self._connected = True

    def _add_connection(self, path: psdf.Path):
        """
        Add an input node to the node.
        """
        attribute = self._sm.get_stage().GetPrimAtPath(path)
        attribute_node = self._sm.init_path_node(attribute)
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
        self._node_icon = cstat.Icon.ICON_NULL


class Mesh(Primative):
    """
    Class representing a mesh node.
    """

    def __init__(self, data_object):
        self._display_color = None  
        super().__init__(data_object)      
        self._data_object: pgeo.Mesh

    def _init_node_data(self):
        super()._init_node_data()
        self._data_object = pgeo.Mesh(self._data_object)  
        self._node_color = (0.8, 0.4, 0.4, 1.0)
        self._node_icon = cstat.Icon.ICON_MESH
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
        self._node_icon = cstat.Icon.ICON_LIGHT


class Camera(Primative):
    """
    Class representing a camera node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()    
        self._node_color = (0.4, 0.4, 0.8, 1.0)
        self._node_icon = cstat.Icon.ICON_CAMERA


class Skeleton(Primative):
    """
    Class representing a skeleton node.
    """
    def __init__(self, data_object):
        self._is_animating = False
        super().__init__(data_object)
          
    def _init_node_data(self):
        super()._init_node_data()
        self._data_object = pskl.Skeleton(self._data_object)
        self._node_color = (0.6, 0.4, 0.8, 1.0)
        self._node_icon = cstat.Icon.ICON_SKELETON
        self.check_animation()
        self._init_skeleton_bones()

    def _init_skeleton_bones(self):
        """
        Load the skeleton of the node.
        """
        self._bone_dict: dict[Bone, Any] = {}
        self._data_object: pskl.Skeleton
        bone_attribute = self._data_object.GetJointsAttr()
        bone_matrix_list = self._data_object.GetBindTransformsAttr().Get()
        bone_path_list = bone_attribute.Get(self._sm.get_current_time())
        for index, path in enumerate(bone_path_list):
            sdf_path = psdf.Path(path)
            path_split = str(path).split("/")
            bone_matrix: pgf.Matrix4d = bone_matrix_list[index]
            bone_entry_dict = {
                "index": index,
                "owner": self._data_object,
                "path": sdf_path,
                "name": path_split[-1],
                "matrix": bone_matrix,
                "anim_matrix": bone_matrix,
            }
            bone_object = self._sm.init_data_object(bone_entry_dict)
            self._bone_dict[bone_object] = bone_entry_dict
        for bone in self._bone_dict:
            parent_path = bone.get_relative_path().GetParentPath()
            if parent_path == psdf.Path("."):
                self._add_child(bone)
            else:
                parent_bone = self._get_bone_from_path(parent_path)
                if parent_bone:
                    parent_bone.add_child(bone)

    def _get_bone_from_path(self, path: psdf.Path) -> 'Bone':
        """
        Get a bone from the path.
        """
        for bone in self._bone_dict:
            if bone.get_relative_path() == path:
                return bone
        return None

    def check_animation(self):
        """
        Check if the skeleton has an animation.
        """
        for child in self._child_list:
            if isinstance(child, Animation):
                self._animation = child.get_data_object()
                return True
        self._animation = False
        self._is_animating = False

    def enable_animation(self):
        """
        Enable animation.
        """
        if self._animation:
            self._is_animating = True

    def disable_animation(self):
        """
        Disable animation.
        """
        if self._animation:
            self._is_animating = False

    def update_animation(self):
        """
        Update animation.
        """
        if self._animation and self._is_animating:
            for index, bone in enumerate(self._bone_dict):
                self._sm.get_current_time()
                parent_bone_path = bone.get_relative_path().GetParentPath()
                if parent_bone_path == psdf.Path("."):
                    parent_bone_matrix = pgeo.Xformable(self._data_object.GetPrim()).ComputeLocalToWorldTransform(self._sm.get_current_time())
                else:
                    parent_bone_matrix = pgf.Matrix4d()
                for parent_bone in self._bone_dict:
                    if parent_bone.get_relative_path() == parent_bone_path:
                        parent_bone_matrix = self._bone_dict[parent_bone]["anim_matrix"]
                translation_list = self._animation.GetPrim().GetAttribute("translations").Get(self._sm.get_current_time())
                rotation_list = self._animation.GetPrim().GetAttribute("rotations").Get(self._sm.get_current_time())
                scale_list = self._animation.GetPrim().GetAttribute("scales").Get(self._sm.get_current_time())
                matrix = pgf.Matrix4d().SetScale(pgf.Vec3d(scale_list[index])).SetTranslate(pgf.Vec3d(translation_list[index])).SetRotateOnly(rotation_list[index])
                anim_matrix = matrix * parent_bone_matrix
                self._bone_dict[bone]["anim_matrix"] = anim_matrix
        else:
            for index, bone in enumerate(self._bone_dict):
                self._bone_dict[bone]["anim_matrix"] = self._bone_dict[bone]["matrix"]

class SkeletonRoot(Primative):
    """
    Class representing a skeleton root node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)
        self._init_zero_root()
        self.zero_root()

    def _init_node_data(self):
        super()._init_node_data()
        self._data_object = pskl.Root(self._data_object)
        self._node_color = (0.6, 0.4, 0.8, 1.0)
        self._node_icon = cstat.Icon.ICON_SKELETON_ROOT

    def _init_zero_root(self):
        """
        Initialize the zero of the skeleton root.
        """
        skel_root_prim = self._data_object.GetPrim()
        xformable = pgeo.Xformable(skel_root_prim)
        self._zero_transform_op = xformable.AddTransformOp()
        self._zero_transform_op.Set(pgf.Matrix4d())

    def zero_root(self):
        """
        zero the skeleton root.
        """
        if self._zero_transform_op:
            for time in range(self._sm.get_time_range()[1]):
                current_translate = self._data_object.GetPrim().GetAttribute("xformOp:translate").Get(time)
                current_rotate = self._data_object.GetPrim().GetAttribute("xformOp:rotateXYZ").Get(time)
                current_scale = self._data_object.GetPrim().GetAttribute("xformOp:scale").Get(time)
                rotation = pgf.Rotation(pgf.Vec3d(1, 0, 0), current_rotate[0])
                rotation = rotation * pgf.Rotation(pgf.Vec3d(0, 1, 0), current_rotate[1])
                rotation = rotation * pgf.Rotation(pgf.Vec3d(0, 0, 1), current_rotate[2])
                current_matrix = pgf.Matrix4d().SetScale(pgf.Vec3d(current_scale)).SetTranslateOnly(pgf.Vec3d(current_translate)).SetRotateOnly(rotation)
                self._zero_transform_op.Set(current_matrix.GetInverse(), time)
        
    def remove_root_zero(self):
        """
        Remove the zero on the skeleton root.
        """
        if self._zero_transform_op:
            for time in range(self._sm.get_time_range()[1]):
                self._zero_transform_op.Set(pgf.Matrix4d().SetIdentity(), time)

class Animation(Primative):
    """
    Class representing a skeleton node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()
        self._data_object = pskl.Animation(self._data_object)
        self._node_color = (0.2, 0.3, 0.7, 1.0)
        self._node_icon = cstat.Icon.ICON_ANIMATION
        

class Material(Primative):
    """
    Class representing a material node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)
        
    def _init_node_data(self):
        super()._init_node_data()    
        self._node_color = (0.8, 0.4, 0.6, 1.0)
        self._node_icon = cstat.Icon.ICON_MATERIAL

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
        self._node_icon = cstat.Icon.ICON_CURVE


class Data(Node):
    """
    Class representing a data node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)

    def _init_node_data(self):
        self._set_name(self._data_object["name"])
        self._parent_node: pusd.Prim = self._data_object["owner"]
        self._relative_path = self._data_object["path"]

    def get_relative_path(self) -> psdf.Path:
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
        self._node_icon = cstat.Icon.ICON_TEXTURE


class Bone(Data):
    """
    Class representing a bone node.
    """
    def __init__(self, data_object):
        super().__init__(data_object)
        self._child_list: list['Bone'] = []

    def _init_node_data(self):
        super()._init_node_data()
        self._node_color = (0.8, 0.6, 0.4, 1.0)
        self._node_icon = cstat.Icon.ICON_BONE
    
    def add_child(self, child: 'Bone'):
        """
        Add a child node to the bone.
        """
        if child and child not in self._child_list and child != self:
            self._child_list.append(child)
    
    def get_child_nodes(self) -> list['Bone']:
        """
        Get the child nodes.
        """
        return self._child_list


#####################################################################################################################################


class NodePencil:
    """
    Class representing an draw pencil.
    """

    def __init__(self, node: Node):
        self._node_name = None
        self._node_icon = None
        self._node_color = None
        self._node_display_color = None        
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

    def __init__(self):
        self._config = None
        self._render_context_manager = None
        self._display_size = None        
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
        self._sm = SceneManager()

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
        glfw.set_window_should_close(self._window, True)
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
        self._sm = SceneManager()
        self._stage = self._sm.get_stage()

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
        self._panel_width = int(size[0])
        self._panel_height = int(size[1])
        self._panel_position = (int(position[0]), int(position[1]))
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
    _fps = 30
    _current_time = 0
    _start_time = 0
    _end_time = 1
    _instance = None
    def __new__(cls, usd_path: str=None):
        if cls._instance is None:
            cls._initialized = False
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, usd_path: str=None):
        self._init_config()
        if usd_path and not self._initialized:
            self._root = None
            self._animation = None
            self._usd_path = usd_path
            self._init_usd_scene()
            self._initialized = True      
        elif usd_path:
            self.set_usd_file(usd_path)

    def _init_config(self):
        """
        Initialize the configuration file.
        """
        self._cfg = cutils.get_core_config()
        self._up_axis = self._cfg['scene']['up_axis']

    def _init_usd_scene(self, force_path: str=None):
        """
        Initialize USD scene.
        """
        print(f"Loading USD file: {self._usd_path}")        
        self._path_node_list: list[Pathed] = []
        self._data_node_list: list[Data] = []
        self._stage: pusd.Stage = pusd.Stage.Open(self._usd_path)
        self._root = self._stage.GetPseudoRoot()
        self._init_time_manager()
        internal_root = self._init_internal_node(self._root)
        self._add_path_node(internal_root)
        self._calc_up_axis()
        self._scene_bbox_center, self._scene_bbox_size = self.create_scene_bounding_box()
        self.init_scene_default_objects()
        if not self._animation:
            self.disable_animation()

    def _init_time_manager(self):
        """
        Initialize the time manager.
        """
        self._fps = self._stage.GetTimeCodesPerSecond()
        self._current_time = self._stage.GetStartTimeCode()
        self._start_time = self._stage.GetStartTimeCode()
        self._end_time = self._stage.GetEndTimeCode()
    
    def _init_internal_node(self, input_object: pusd.Prim | pusd.Attribute) -> Node | None:
        """
        Get appropriate node type and init.
        """
        prim_classes = {
            "": Root,
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
            "SkelRoot": SkeletonRoot,
            "SkelAnimation": Animation,
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
        else:
            print(f"Unknown node type: {input_object_type}")
        return None

    def _init_internal_data(self, data_object: dict[str, str | pusd.Prim]) -> Data:
        """
        Get appropriate data type and init.
        """
        if isinstance(data_object["owner"], pskl.Skeleton):
            return Bone(data_object)
        elif isinstance(data_object["owner"], pshd.Material):
            return Texture(data_object)
        else:
            return None

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

    def _calc_up_axis(self):
        """
        Initialize up axis matrix.
        """
        if self._up_axis == "Y":
            self._up_axis_matrix = pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(1, 0, 0), 0))
        elif self._up_axis == "Z":
            self._up_axis_matrix = pgf.Matrix4d().SetRotate(pgf.Rotation(pgf.Vec3d(1, 0, 0), -90))
        else:
            raise ValueError("Invalid up axis specified")

    def _create_camera(self):
        """
        Create a camera with default attributes and a transformation matrix.
        """
        clipping_range = self._cfg["viewport"]["clipping_range"]
        focal_length = self._cfg["viewport"]["focal_length"]
        camera = pgeo.Camera.Define(self._stage, "/OrbitCamera")
        camera.CreateFocalLengthAttr(focal_length)
        camera.CreateHorizontalApertureAttr(24.0)
        camera.CreateVerticalApertureAttr(18.0)
        camera.CreateHorizontalApertureOffsetAttr(0.0)
        camera.CreateVerticalApertureOffsetAttr(0.0)
        camera.CreateClippingRangeAttr(pgf.Vec2f(clipping_range))
        xform_attr = camera.GetPrim().CreateAttribute("xformOp:transform", psdf.ValueTypeNames.Matrix4d)
        xform_attr.Set(pgf.Matrix4d().SetIdentity())
        xform_op_order = camera.GetPrim().GetAttribute("xformOpOrder")
        if not xform_op_order:
           xform_op_order = camera.GetPrim().CreateAttribute("xformOpOrder", psdf.ValueTypeNames.TokenArray)
        xform_op_order.Set(["xformOp:transform"])
        return camera.GetPrim()

    def _create_lighting(self):
        """
        Create default 3-point lighting.
        """
        light_xform = pgeo.Xform.Define(self._stage, "/LightNull")
        light_xform.GetPrim().CreateAttribute("xformOp:transform", psdf.ValueTypeNames.Matrix4d)
        light_xform.GetPrim().GetAttribute("xformOp:transform").Set(pgf.Matrix4d().SetIdentity())
        lights_xform_op_order = light_xform.GetPrim().CreateAttribute("xformOpOrder", psdf.ValueTypeNames.TokenArray)
        lights_xform_op_order.Set(["xformOp:transform"])
        self._light_xform = light_xform.GetPrim()
        
        zero_position = pgf.Vec3d(0.0, 0.0, 0.0)
        distance = 100
        key_position = pgf.Vec3d(5.0, 5.0, 5.0).GetNormalized() * distance
        fill_position = pgf.Vec3d(-5.0, 3.0, 5.0).GetNormalized() * distance
        back_position = pgf.Vec3d(0.0, 5.0, -5.0).GetNormalized() * distance

        key_transform = self._calc_light_transform(key_position, zero_position)
        fill_transform = self._calc_light_transform(fill_position, zero_position)
        back_transform = self._calc_light_transform(back_position, zero_position)

        self._light_key = self._create_light("/LightNull/KeyLight", (1.0, 0.95, 0.9), 15.0, key_transform)
        self._light_fill = self._create_light("/LightNull/FillLight", (0.9, 0.9, 1.0), 8.0, fill_transform)
        self._light_back = self._create_light("/LightNull/BackLight", (1.0, 1.0, 1.0), 10.0, back_transform)
        return self._light_xform

    def _create_light(self, path: str, color: tuple, intensity: float, transform: pgf.Matrix4d) -> pusd.Prim:
        """
        Create a light for the scene with a specified intensity.
        """
        light = plux.DistantLight.Define(self._stage, path)
        light.CreateIntensityAttr(intensity)
        light.CreateColorAttr(pgf.Vec3f(*color))
        light.CreateAngleAttr(35.0)
        light.GetPrim().CreateAttribute("xformOp:transform", psdf.ValueTypeNames.Matrix4d)
        light.GetPrim().GetAttribute("xformOp:transform").Set(transform)
        light_xform_op_order = light.GetPrim().CreateAttribute("xformOpOrder", psdf.ValueTypeNames.TokenArray)
        light_xform_op_order.Set(["xformOp:transform"])
        light.GetPrim().GetAttribute("visibility").Set(pgeo.Tokens.inherited)
        return light.GetPrim()

    def _calc_light_transform(self, light_position, target_position):
        """
        Calculate the light transform matrix.
        """
        world_up = pgf.Vec3d(0, 1, 0)
        light_matrix = cutils.calc_look_at_neg_z(light_position, target_position, world_up, flip_forward=True)
        return light_matrix

    def calc_light_xform_default(self) -> None:
        """
        Scale the default light.
        """
        bbox_size_factor = self._scene_bbox_size.GetLength()
        if bbox_size_factor <= 0:
            bbox_size_factor = 1.0
        distance_factor = 2.0
        distance = bbox_size_factor * distance_factor
        target_scale = distance / 200
        light_scale = pgf.Vec3d(target_scale, target_scale, target_scale)
        self._light_xform.GetAttribute("xformOp:transform").Set(pgf.Matrix4d().SetScale(light_scale) * self._up_axis_matrix.GetInverse())


    def get_camera_dict(self):
        """
        Create a list of lights in the scene.
        """
        if not self._stage:
            return []
        camera_dict: dict = {}
        prim_list = self._stage.Traverse()
        for prim in prim_list:
            if prim.IsA(pgeo.Camera):
                if prim.GetAttribute("visibility").Get() != pgeo.Tokens.invisible:
                    xformable = pgeo.Xformable(prim)
                    world_transform = xformable.ComputeLocalToWorldTransform(pusd.TimeCode.Default())
                    world_transform_orthonormalized = pgf.Matrix4d(world_transform).GetOrthonormalized()
                    world_rotation = world_transform_orthonormalized.ExtractRotation()
                    world_translate = world_transform.ExtractTranslation()
                    world_transform = pgf.Matrix4d().SetTranslateOnly(world_translate).SetRotateOnly(world_rotation)
                    camera_dict[str(prim.GetName())] = {
                        "prim": prim,
                        "matrix": world_transform,
                        "visibility": True if prim.GetAttribute("visibility").Get() == pgeo.Tokens.inherited else False,
                    }
        return camera_dict

    def get_light_dict(self):
        """
        Create a list of lights in the scene.
        """
        if not self._stage:
            return {}
        light_dict: dict = {}
        prim_list = self._stage.Traverse()
        for prim in prim_list:
            if prim.HasAPI(plux.LightAPI):
                xformable = pgeo.Xformable(prim)
                world_transform = xformable.ComputeLocalToWorldTransform(pusd.TimeCode.Default())
                world_transform_orthonormalized = pgf.Matrix4d(world_transform).GetOrthonormalized()
                world_rotation = world_transform_orthonormalized.ExtractRotation()
                world_translate = world_transform.ExtractTranslation()
                world_transform = pgf.Matrix4d().SetTranslateOnly(world_translate).SetRotateOnly(world_rotation)
                light_dict[str(prim.GetName())] = {
                    "prim": prim,
                    "matrix": world_transform,
                    "color": prim.GetAttribute("inputs:color").Get(),
                    "visibility": True if prim.GetAttribute("visibility").Get() == pgeo.Tokens.inherited else False,
                }
        return light_dict

    def create_scene_bounding_box(self):
        """
        Create a bounding box for the scene.
        """
        prim_inactive_list: list[pusd.Prim] = []
        for node in self.get_path_node_list():
            if node.get_prim():
                if not node.get_prim().IsActive():
                    node.get_prim().SetActive(True)
                    prim_inactive_list.append(node.get_data_object().GetPrim())
        bbox_cache = pgeo.BBoxCache(pusd.TimeCode.Default(), includedPurposes=[pgeo.Tokens.default_], useExtentsHint=True)
        bbox = bbox_cache.ComputeWorldBound(self._stage.GetPseudoRoot())
        bbox_min = bbox.GetRange().GetMin()
        bbox_max = bbox.GetRange().GetMax()
        bbox_center: pgf.Vec3d = (bbox_min + bbox_max) * 0.5
        bbox_size: pgf.Vec3d = bbox_max - bbox_min
        for prim in prim_inactive_list:
                prim.SetActive(False)   
        return bbox_center, bbox_size

    def get_camera(self) -> pusd.Prim:
        """
        Get the camera of the scene.
        """
        return self._camera

    def get_up_axis_matrix(self) -> pgf.Matrix4d:
        """
        Get the up axis matrix.
        """
        return self._up_axis_matrix

    def get_up_axis(self) -> str:
        """
        Get the up axis of the scene.
        """
        return self._up_axis
    
    def get_up_vector(self) -> pgf.Vec3d:
        """
        Get the up vector of the scene.
        """
        if self._up_axis == "Y":
            return pgf.Vec3d(0, 1, 0)
        if self._up_axis == "Z":
            return pgf.Vec3d(0, 0, 1)
    
    def set_up_axis(self, up_axis: str) -> None:
        """
        Set the up axis of the scene.
        """
        self._up_axis = up_axis
        self._calc_up_axis()

    def get_light_xform(self) -> pusd.Prim:
        """
        Get the light transform of the scene.
        """
        return self._light_xform

    def disable_scene_lights(self):
        """
        Disable all lights in the scene.
        """
        self._light_disable_list: list[pusd.Prim] = []
        prim_list = self._stage.Traverse()
        for prim in prim_list:
            if prim.HasAPI(plux.LightAPI) and prim not in [self._light_key, self._light_fill, self._light_back]:
                if prim.GetAttribute("visibility").Get() != pgeo.Tokens.invisible:
                    self._light_disable_list.append(prim)
                    prim.GetAttribute("visibility").Set(pgeo.Tokens.invisible)
        return False

    def enable_scene_lights(self):
        """
        Enable all lights in the scene.
        """
        for light in self._light_disable_list:
            light.GetAttribute("visibility").Set(pgeo.Tokens.inherited)
        self._light_disable_list = []
        return True

    def disable_default_lights(self):
        """
        Disable all default lights in the scene.
        """
        for light in [self._light_key, self._light_fill, self._light_back]:
            light.GetAttribute("visibility").Set(pgeo.Tokens.invisible)
        return False

    def enable_default_lights(self):
        """
        Enable all default lights in the scene.
        """
        for light in [self._light_key, self._light_fill, self._light_back]:
            light.GetAttribute("visibility").Set(pgeo.Tokens.inherited)
        return True

    def init_scene_default_objects(self):
        """
        Initialize the scene.
        """
        self._light_xform = self._create_lighting()
        self.calc_light_xform_default()
        self._camera = self._create_camera()


    def enable_animation(self):
        """
        Enable animation.
        """
        self._animation = True
        current_camera_matrix = self._camera.GetAttribute("xformOp:transform").Get()
        for path_node in self.get_path_node_list_by_type(Skeleton):
            path_node: Skeleton
            path_node.get_prim().SetActive(True)
        self._stage.Reload()
        self._init_usd_scene()
        for path_node in self.get_path_node_list_by_type(Skeleton):
            path_node: Skeleton
            path_node.enable_animation()
        self._camera.GetAttribute("xformOp:transform").Set(current_camera_matrix)
        self.update_skeletal_animation()

    def disable_animation(self):
        """
        Disable animation.
        """
        self._animation = False
        print("asjkdhaskjd")
        for path_node in self.get_path_node_list_by_type(Skeleton):
            path_node: Skeleton
            if path_node.check_animation():
                path_node.get_prim().SetActive(False)
                path_node.disable_animation()
                path_node.update_animation()
        print("asjkdhaskjd")

    def get_path_node_list(self) -> list[Pathed]:
        """
        Get the list of path nodes.
        """
        return self._path_node_list
    
    def get_path_node_list_by_type(self, node_type: 'Pathed') -> list[Pathed]:
        """
        Get the list of path nodes by type.
        """
        node_list = []
        for node in self._path_node_list:
            if isinstance(node, node_type):
                node_list.append(node)
        return node_list

    def get_data_node_list(self) -> list[Data]:
        """
        Get the list of data nodes.
        """
        return self._data_node_list
    
    def get_data_node_list_by_type(self, node_type: 'Data') -> list[Data]:
        """
        Get the list of data nodes by type.
        """
        node_list = []
        for node in self._data_node_list:
            if isinstance(node, node_type):
                node_list.append(node)
        return node_list

    def init_path_node(self, data_object: pusd.Prim) -> Pathed:
        """
        Initialize a path node and add it to the scene manager.
        """
        for path_node in self._path_node_list:
            if path_node.get_data_object() == data_object:
                return path_node
        path_node = self._init_internal_node(data_object)
        if not path_node:
            print(f"Unknown path object type: {data_object.GetTypeName()}")
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
        self._init_usd_scene()

    def get_root(self) -> pusd.Prim:
        """
        Get the root of the stage.
        """
        return self._root

    def zero_skeletal_root(self) -> None:
        """
        Zero the skeletal root motion of the scene.
        """
        for path_node in self.get_path_node_list():
            if isinstance(path_node, SkeletonRoot):
                path_node.zero_root()

    def remove_skeletal_root_zero(self) -> None:
        """
        Remove the skeletal root motion of the scene.
        """
        for path_node in self.get_path_node_list():
            if isinstance(path_node, SkeletonRoot):
                path_node.remove_root_zero()

    def get_fps(self) -> int:
        """
        Get the frames per second.
        """
        return self._fps

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
        return int(self._start_time), int(self._end_time)
    
    def get_path_node(self, input: psdf.Path | pusd.Prim | pusd.Attribute) -> Pathed:
        """
        Get the path node from psdf.Path | pusd.Prim | pusd.Attributes.
        """
        if isinstance(input, pusd.Prim) and not isinstance(input, pusd.Attribute):
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
            if node.get_relative_path() == input:
                return node
            elif node.get_name() == input:
                return node

    def check_animation(self) -> bool:
        """
        Check if the animation is present in the scene.
        """
        skeleton_list = self.get_path_node_list_by_type(Skeleton)
        for skeleton in skeleton_list:
            skeleton: Skeleton
            if skeleton.check_animation():
                return True

    def disable_skeletal_animation(self) -> None:
        """
        Disable the skeletal animation.
        """
        for node in self._path_node_list:
            if isinstance(node, Skeleton):
                node.disable_animation()
                node.update_animation()

    def enable_skeletal_animation(self) -> None:
        """
        Enable the skeletal animation.
        """
        for node in self._path_node_list:
            if isinstance(node, Skeleton):
                node.enable_animation()
                node.update_animation()

    def update_skeletal_animation(self, skeleton: Skeleton = None) -> None:
        """
        Update the animation.
        """
        if not skeleton:
            for node in self._path_node_list:
                if isinstance(node, Skeleton):
                    node.update_animation()
        else:
            skeleton.update_animation()

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
            self.context_list.remove(context)
            imgui.set_current_context(context)
            imgui.backends.glfw_shutdown()
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

#####################################################################################################################################

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
        self._cfg_msaa = self._cfg["glfw"]["msaa"]

    def _init_frame(self):
        """
        Initialize the GLFW window with 4x MSAA.
        """
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        
        if self._cfg_msaa > 0:
            glfw.window_hint(glfw.SAMPLES, self._cfg_msaa)
        
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
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
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
        glfw.destroy_window(self._window)
        glfw.terminate()
        sys.exit()      

#####################################################################################################################################


