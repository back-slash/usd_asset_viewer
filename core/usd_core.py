
import pxr.Gf as pxgf
from pxr import Usd as pxusd
import pprint as pp
import os
import json


from utils import utils
import statics.statics as cstat



def get_usd_file_dict(directory: str):
    """
    List all .usd files in the given directory.
    """
    usd_file_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".usd"):
                usd_file_dict[file] = os.path.join(root, file)
    return usd_file_dict


def get_usd_object_list(usd_stage: pxusd.Stage) -> list[pxusd.Prim]:
    usd_object_list = []
    for scene_object in usd_stage.Traverse():
        scene_object: pxusd.Prim
        usd_object_list.append(scene_object)
    return usd_object_list


def get_usd_root(usd_stage: pxusd.Stage):
    """
    Get the root of the USD stage.
    """
    return usd_stage.GetPseudoRoot()


def get_usd_skeleton(usd_stage: pxusd.Stage) -> list[dict]:
    """
    Get the skeleton of the USD stage.
    """
    usd_skeleton = []
    primative_list = get_usd_object_list(usd_stage)
    for primative in primative_list:
        if primative.GetTypeName() == "Skeleton":
            attribute_list = primative.GetAttributes()
            for attribute in attribute_list:
                if attribute.GetName() == "joints":
                    joint_list: list[str] = attribute.Get()
                    for joint_path in joint_list:
                        hierarchyList = joint_path.split("/")
                        joint_name = hierarchyList[-1]
                        joint_parent = hierarchyList[-2] if len(hierarchyList) > 1 else None
                        usd_skeleton.append({
                            "name": joint_name,
                            "path": joint_path,
                            "type": "joint",
                            "parent": joint_parent
                        })
            for attribute in attribute_list:
                if attribute.GetName() == "bindTransforms":
                    bind_transform_list: list[pxgf.Matrix4dArray] = attribute.Get()
                    for joint_index in range(len(usd_skeleton)):
                        usd_skeleton[joint_index]["index"] = joint_index
                        joint_bind_transform_list = bind_transform_list[joint_index]
                        usd_skeleton[joint_index]["bindTransforms"] = joint_bind_transform_list
            for attribute in attribute_list:
                if attribute.GetName() == "restTransforms":
                    rest_transform_list: list[pxgf.Matrix4dArray] = attribute.Get()
                    for joint_index in range(len(usd_skeleton)):
                        joint_rest_transform_list = rest_transform_list[joint_index]
                        usd_skeleton[joint_index]["restTransform"] = joint_rest_transform_list
    return usd_skeleton





def get_usd_meshes(usd_stage: pxusd.Stage) -> dict[str, dict]:
    pass

def get_usd_information_dict(usd_stage: pxusd.Stage):
    """
    Get the information of USD objects in the stage.
    """
    usd_information_dict = {}
    usd_object_list = get_usd_object_list(usd_stage)
    for usd_object in usd_object_list:
        object_name = usd_object.GetName()
        object_path = usd_object.GetPath()
        object_type = usd_object.GetTypeName()
        object_attributes = usd_object.GetAttributes()
        usd_information_dict[str(object_name)] = {
            "path": str(object_path),
            "type": str(object_type),
            "attributes": {}
        }
        for attribute in object_attributes:
            attribute_name = str(attribute.GetName())
            attribute_path = str(attribute.GetPath())
            attribute_type = str(attribute.GetTypeName())
            attribute_value = attribute.Get()

            if "array" in str(type(attribute_value)).lower():
                attribute_value = [str(value) for value in attribute_value]
            else:
                attribute_value = str(attribute_value)
            usd_information_dict[object_name]["attributes"][attribute_name] = {
                "attribute_path": attribute_path,
                "attribute_type": attribute_type,
                "attribute_value": attribute_value
            }
    return usd_information_dict


class USDPrototypeObject:
    """
    Class representing a USD object in the prototype.
    """
    def __init__(self, usd_file_path):
        self.usd_file_path = usd_file_path
        self.usd_stage = pxusd.Stage.Open(usd_file_path)
        self.prepare_usd_data(self.usd_file_path)

        
    def prepare_usd_data(self, file_path: str):
        """
        Prepare the USD data for use in the prototype.
        """
        usd_stage = pxusd.Stage.Open(file_path)
        if not usd_stage:
            print(f"Failed to open USD file: {file_path}")
            return

        self.usd_object_list = get_usd_object_list(usd_stage)
        self.usd_root = get_usd_root(usd_stage)
        self.usd_information_dict = get_usd_information_dict(usd_stage)
        self.usd_skeleton = get_usd_skeleton(usd_stage)       




if __name__ == "__main__":
    usd_file_path = pstatic.USD_FILE_PATH
    usd_directory = pstatic.USD_DIRECTORY

    file_name = os.path.split(usd_file_path)[0]
    extension = os.path.splitext(usd_file_path)[1]
    json_file_path = usd_file_path.replace(extension, ".json")

    usd_prototype_object = USDPrototypeObject(usd_file_path)
    putils.write_to_file(json_file_path, usd_prototype_object.usd_information_dict, pstatic.PrototypeFiletype.JSON)




