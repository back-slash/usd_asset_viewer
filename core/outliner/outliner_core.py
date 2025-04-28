import imgui

import static.static as stat
import core.entity_core as cent
import core.usd_core as cusd





class OutlinerEntity(pcore.PrototypeEntity):
    """
    Class representing an entity in the outliner.
    """
    def __init__(self, source_object: dict, parent_object):
        super().__init__(source_object, parent_object)


    def calculate_drop_target_position(self):
        """
        Calculate the drop target position for the outliner object.
        """
        x = imgui.get_cursor_screen_pos().x
        y = imgui.get_cursor_screen_pos().y
        return x, y

    def draw(self, x: float, y: float):
        """
        Draw the outliner object in the prototype window.
        """
        self.draw_list = imgui.get_window_draw_list()
        imgui.push_id(self.item_name)
       
        if self.parent_object:
            imgui.push_style_var(imgui.STYLE_ITEM_SPACING, pstatic.OUTLINER_ITEM_SPACING)
            imgui.new_line()
            imgui.pop_style_var(1)

        x, y = imgui.get_cursor_screen_pos()

        if not self.floating or self.drop_target:
            if self.drop_target:
                x, y = self.calculate_drop_target_position()
            self.draw_background_line(x, y)

        imgui.pop_id()



class OutlinerRelationship:
    """
    Class representing a relationship between two outliner objects.
    """
    def __init__(self, source_object: pcore.PrototypeEntity, target_object: pcore.PrototypeEntity):
        super().__init__()
        self.source_object = source_object
        self.target_object = target_object



class OutlinerPanel(pcore.PrototypePanel):
    """
    Outliner class for managing and displaying a list of items in a prototype window.
    """
    def __init__(self, parent=None, source: pusd.USDPrototypeObject = None):
        super().__init__(parent, source)
        self.parent = parent
        if source:
            self.source_data_object = source
            self.source_item_list = self.source_data_object.usd_skeleton
        self.outliner_item_list: list[OutlinerEntity] = []
        self.hierarchy_dict = {}



    def draw_background_line(self, x: float, y: float):
        """
        Draw the background line for the outliner object.
        """
        
        backdrop_rect_min_x = x
        backdrop_rect_min_y = y
        backdrop_rect_max_x = x + 400
        backdrop_rect_max_y = backdrop_rect_min_y + 20.0

        line_color = (0.3, 0.3, 0.3, 1.0)

        self.draw_list.add_rect_filled(backdrop_rect_min_x, backdrop_rect_min_y, backdrop_rect_max_x, backdrop_rect_max_y, imgui.get_color_u32_rgba(*line_color), rounding=4.0)



    def create_invisible_root_item(self):
        """
        Create a new item in the outliner.
        """
        fake_data = {
            "name": "InvisibleRoot",
            "type": "InvisibleRoot",
            "path": "/"
        }
        new_item = OutlinerEntity(fake_data, None)
        return new_item


    def create_outliner_item(self, item_data_dict, parent_item_object):
        """
        Create a new item in the outliner.
        """
        new_item = OutlinerEntity(item_data_dict, parent_item_object)
        return new_item

    def find_item_by_path(self, path):
        """
        Find an item in the outliner by its path.
        """
        for item in self.outliner_item_list:
            if item.item_path == path:
                return item
        return None
    
    def build_item_hierarchy(self, item_list: list[OutlinerEntity], hierarchy_dict: dict):
        for item in item_list:
            if item.parent_object and item not in self.hierarchy_dict:
                hierarchy_dict[item] = {}
            else:
                self.build_item_hierarchy(item_list, hierarchy_dict[item.parent_object])
    
    def recursively_draw_hierarchy_dict(self, hierarchy_dict: dict[OutlinerEntity, dict]):
        for item in hierarchy_dict:
            item.draw(0, 0)
            if hierarchy_dict[item]:
                self.recursively_draw_hierarchy_dict(hierarchy_dict[item])

    def update(self):
        self.outliner_item_list.clear()
        invisible_root = self.create_invisible_root_item()
        for source_data_dict in self.source_item_list:
            if not source_data_dict['parent']:
                parent_item_object = invisible_root
            else:
                parent_item_name = source_data_dict['parent']
                for item in self.outliner_item_list:
                    if item.item_name == parent_item_name:
                        parent_item_object = item
                        break
            new_item = self.create_outliner_item(source_data_dict, parent_item_object)
            self.outliner_item_list.append(new_item)

    def draw(self):
        """
        Draw the outliner in the prototype window.
        """
        super().draw()
        self.update()

        # Apply window styling
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, pstatic.OUTLINER_WINDOW_PADDING)
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, pstatic.OUTLINER_WINDOW_ROUNDING)
        imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING, 4.0)
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, pstatic.OUTLINER_ITEM_SPACING)

        # Apply color styling
        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *pstatic.OUTLINER_BG_COLOUR)
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, *pstatic.OUTLINER_TITLE_BG_COLOUR)
        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *pstatic.OUTLINER_TITLE_ACTIVE_BG_COLOUR)

        self.hierarchy_dict.clear()
        self.build_item_hierarchy(self.outliner_item_list, self.hierarchy_dict)
        
        # Begin the outliner window
        flags = 0
        imgui.begin("Prototype Outliner", True, flags)

        self.recursively_draw_hierarchy_dict(self.hierarchy_dict)
        
        imgui.pop_style_color(3)
        imgui.pop_style_var(4)



        imgui.end()


