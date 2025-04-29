#####################################################################################################################################
# USD Outliner | Tool | Main
# TODO:
# - Add animation trackbars to the outliner to scrub time
#####################################################################################################################################

# PYTHON


# ADDONS
from imgui_bundle import imgui
import glfw
import OpenGL.GL as gl
import pxr.Usd as pusd

# PROJECT
import core.static.static_core as cstat
import core.utils_core as cutils
import core.base_core as base_core

#####################################################################################################################################



class OutlinerPanel(base_core.Panel):
    """
    Outliner class for managing and displaying a list of items in a prototype window.
    """
    def __init__(self, parent=None, source: cusd.USDPrototypeObject = None):
        super().__init__(parent, source)
        self.parent = parent
        if source:
            self.source_data_object = source
            self.source_item_list = self.source_data_object.usd_skeleton
        self.outliner_item_list: list[base_core.Node] = []
        self.hierarchy_dict = {}

    def _set_usd_file(self, file_path: str):
        """
        Set the USD file path.
        """
        self.source_data_object = pusd.Stage.Open(file_path)
        self.source_item_list = self.source_data_object.usd_skeleton


    def create_invisible_root_item(self):
        """
        Create a new item in the outliner.
        """
        fake_data = {
            "name": "InvisibleRoot",
            "type": "InvisibleRoot",
            "path": "/"
        }
        new_item = base_core.Node(fake_data, None)
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













def build_prototype(window, renderer: GlfwRenderer):
    file_path = pstatic.USD_FILE_PATH
    source_data_object = pusd.USDPrototypeObject(file_path)
    prototypeWindow = pcore.PrototypeWindow()
    if source_data_object:
        invisible_root = None
        outliner = ocore.OutlinerPanel(invisible_root, source_data_object)
        item_list = [
            outliner,
        ]
        while not glfw.window_should_close(window):
            render_tick(window, renderer, item_list)


def render_tick(window, renderer: GlfwRenderer, item_list: list[pcore.PrototypePanel]):
    """
    Function to be called every frame to render.
    """
    glfw_render_prep(renderer)

    imgui.new_frame()
    for item in item_list:
        item.draw()
    imgui.render()

    glfw_render(window, renderer)


def init_glfw_window(window_name: str, width: int, height: int):
    """
    Initialize GLFW and create a window.
    """
    if not glfw.init():
        return None

    window = glfw.create_window(width, height, window_name, None, None)
    if not window:
        glfw.terminate()
        return None

    glfw.make_context_current(window)
    glfw.swap_interval(1)  # Enable vsync

    return window


def glfw_render_prep(renderer: GlfwRenderer):
    """
    Prepare the window for rendering.
    """
    glfw.poll_events()
    renderer.process_inputs()


def glfw_render(window, renderer: GlfwRenderer):
    """
    Render the window.
    """
    gl.glClearColor(0, 0, 0, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    renderer.render(imgui.get_draw_data())
    glfw.swap_buffers(window)


def main():
    prototype_window = init_glfw_window("Prototype Editor", 1280, 720)
    imgui.create_context()
    renderer = GlfwRenderer(prototype_window)
    build_prototype(prototype_window, renderer)
    renderer.shutdown()
    glfw.terminate()



if __name__ == "__main__":
    main()