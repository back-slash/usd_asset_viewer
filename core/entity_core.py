import imgui

import static.static as stat




class PanelEntity():
    """
    Class representing a panel in the prototype window.
    """
    

class NodeEntity:
    """
    Class representing a prototype entity.
    """
    def __init__(self, source_object: dict, parent_object):
        self.source_object = source_object
        self.parent_object = parent_object
        self.child_list: list[dict] = []
        self.property_list: list[dict] = []
        self.input_list: list['NodeEntity'] = []
        self.output_list: list['NodeEntity'] = []
        self.item_type = source_object['type']
        self.item_name = source_object['name']
        self.item_path = source_object['path']
        self.floating = False
        self.drop_target = False

    def add_child(self, child):
        if child not in self.child_list:
            self.child_list.append(child)

    def remove_child(self, child):
        if child in self.child_list:
            self.child_list.remove(child)

    def add_property(self, property_object: 'NodeEntity'):
        """
        Add a property to the outliner object.
        """
        if property_object not in self.property_list:
            self.property_list.append(property_object)
    
    def remove_property(self, property_object: 'NodeEntity'):
        """
        Remove a property from the outliner object.
        """
        if property_object in self.property_list:
            self.property_list.remove(property_object)

    def add_input(self, input_object: 'NodeEntity'):
        """
        Add an input to the outliner object.
        """
        if input_object not in self.input_list:
            self.input_list.append(input_object)

    def add_output(self, output_object: 'NodeEntity'):
        """
        Add an output to the outliner object.
        """
        if output_object not in self.output_list:
            self.output_list.append(output_object)
