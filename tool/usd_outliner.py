import imgui
from imgui.integrations.glfw import GlfwRenderer

import glfw
import OpenGL.GL as gl

import prototypeStatics as pstatic
import outliner.outlinerCore as ocore
import prototypeCore as pcore
import prototypeUSD as pusd


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