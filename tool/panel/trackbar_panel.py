#####################################################################################################################################
# USD Asset Viewer | Tool | Panel | Trackbar
# TODO:
# -
#####################################################################################################################################

# PYTHON
from typing import Any

# ADDONS
from imgui_bundle import imgui
from pxr import Usd as pusd
from pxr import UsdSkel as pskl
import threading
import time

# PROJECT
import core.static_core as cstat
import core.utils_core as cutils
import core.base_core as cbase
#####################################################################################################################################
      
class TrackbarPanel(cbase.Panel):
    """
    Trackbar for scrubbing usd scene time.
    """
    def __init__(self, frame: cbase.Frame):
        super().__init__("trackbar", frame)
        self._init_time()
        self._thread = None

    def _init_time(self) -> None:
        """
        Initialize time.
        """
        self._is_playing = None
        self._start_time, self._end_time = self._scene_manager.get_time_range()

    def play(self, loop=True) -> None:
        """
        Play the animation.
        """
        if self._is_playing == None:
            self._scene_manager.enable_animation()
            self._is_playing = True
            if loop:
                self._thread = threading.Thread(target=self._time_play, daemon=True)
                self._thread.start()
        else:
            self._is_playing = True

    def pause(self) -> None:
        """
        Pause the animation.
        """
        if self._thread:
            self._is_playing = False
    
    def stop(self) -> None:
        """
        Stop the animation.
        """
        self._scene_manager.disable_animation()
        if self._thread:
            self._thread.join()
        self._is_playing = None

    def _time_play(self) -> None:
        """
        Play the animation.
        """
        while self._is_playing:
            time.sleep(1.0 / self._scene_manager.get_fps())
            current_time = self._scene_manager.get_current_time()
            if current_time >= self._end_time:
                self._scene_manager.set_current_time(self._start_time)
            else:
                self._scene_manager.set_current_time(current_time + 1.0)
            self._scene_manager.update_animation()

    def _draw_horizonal_line(self) -> None:
        window_pos = imgui.get_window_pos()
        window_size = imgui.get_window_size()
        vertical_line_min  = imgui.ImVec2(window_pos[0], window_pos[1])
        vertical_line_max  = imgui.ImVec2(window_size[0], window_pos[1])
        self._draw_list.add_line(vertical_line_min, vertical_line_max, imgui.get_color_u32((0, 0, 0, 1)), thickness=1.0)

    def _draw_trackbar(self) -> None:
        """
        Draw the trackbar.
        """
        imgui.push_style_color(imgui.Col_.slider_grab, imgui.get_color_u32((0.15, 0.15, 0.15, 1)))
        imgui.push_style_color(imgui.Col_.slider_grab_active, imgui.get_color_u32((0.25, 0.25, 0.25, 1)))
        imgui.push_style_color(imgui.Col_.frame_bg, imgui.get_color_u32((0, 0, 0, 0)))
        imgui.push_style_color(imgui.Col_.frame_bg_active, imgui.get_color_u32((0, 0, 0, 0)))
        imgui.push_style_color(imgui.Col_.frame_bg_hovered, imgui.get_color_u32((0, 0, 0, 0)))

        imgui.push_style_var(imgui.StyleVar_.grab_rounding, 2.0)

        track_bg_width = self._cfg['detail']['width']
        window_pos = imgui.get_window_pos()
        trackbar_bg_min = imgui.get_cursor_pos() + window_pos + imgui.ImVec2(5, 5)
        trackbar_bg_max = imgui.get_content_region_avail() + window_pos - imgui.ImVec2(track_bg_width, 5)
        self._draw_list.add_rect_filled(trackbar_bg_min, trackbar_bg_max, imgui.get_color_u32((0.3, 0.3, 0.3, 1)), rounding=2.0, flags=0)
        self._draw_list.add_rect(trackbar_bg_min, trackbar_bg_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0, flags=0)
        imgui.push_item_width((trackbar_bg_max - trackbar_bg_min)[0] - 10)
        imgui.set_cursor_pos((imgui.get_cursor_pos_x() + 10, imgui.get_cursor_pos_y() + 10))
        changed, value = imgui.slider_int("##trackbar", int(self._scene_manager.get_current_time()), int(self._start_time), int(self._end_time))
        if changed:
            if not self._is_playing:
                self.play(loop=False)
            self._scene_manager.set_current_time(value)
            self._scene_manager.update_animation()
        imgui.pop_item_width()
        imgui.pop_style_color(5)
        imgui.pop_style_var(1)

    def _draw_control_buttons(self) -> None:
        """
        Draw the control buttons.
        """
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (2, 2))
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 2.0)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 1.0)

        imgui.push_style_color(imgui.Col_.button, imgui.get_color_u32((0.3, 0.3, 0.3, 1)))
        imgui.push_style_color(imgui.Col_.button_active, imgui.get_color_u32((0.15, 0.15, 0.15, 1)))
        imgui.push_style_color(imgui.Col_.button_hovered, imgui.get_color_u32((0.4, 0.4, 0.4, 1)))

        start_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_START, (20,20))
        imgui.same_line()
        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + 10)
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        if imgui.image_button("##start", start_icon_id, (20,20)):
            self._scene_manager.set_current_time(self._start_time)
            self._scene_manager.update_animation()
        play_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_PLAY, (20,20))
        pause_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_PAUSE, (20,20))
        imgui.same_line()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        if self._is_playing: playpause_icon_id = pause_icon_id
        else: playpause_icon_id = play_icon_id
        if imgui.image_button("##playpause", playpause_icon_id, (20,20)):
            if not self._is_playing:
                self.play()
            else:
                self.pause()
        imgui.same_line()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        stop_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_STOP, (20,20))
        if imgui.image_button("##stop", stop_icon_id, (20,20)):
            self._is_playing = False
            self.stop()
            self._scene_manager.set_current_time(self._start_time)
            self._scene_manager.update_animation()
        end_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_END, (20,20))
        imgui.same_line()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 2)
        if imgui.image_button("##end", end_icon_id, (20,20)):
            self._scene_manager.set_current_time(self._end_time)
            self._scene_manager.update_animation()
        
        imgui.pop_style_color(3)
        imgui.pop_style_var(3)

    def draw(self) -> None:
        """
        Draw the outliner panel.
        """
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        self._draw_list = imgui.get_window_draw_list()
        self._draw_trackbar()
        self._draw_control_buttons()
        self._draw_horizonal_line()

    def update_usd(self):
        super().update_usd()
        self._init_time()

        