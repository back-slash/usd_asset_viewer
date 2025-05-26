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
        self._animation = False
        self._motion_mode = "In Place"

    def _init_time(self) -> None:
        """
        Initialize time.
        """
        self._is_playing = None
        self._start_time, self._end_time = self._sm.get_time_range()

    def _init_animation(self) -> None:
        """
        Initialize animation.
        """
        if self._sm.get_stage():
            self._scene_skeletal_animation = self._sm.check_animation()
            if self._scene_skeletal_animation:
                self._animation = True
                self._sm.enable_animation()
                self._thread = threading.Thread(target=self._iterate_frame, daemon=True)
                self._thread.start()

    def _terminate_animation(self) -> None:
        """
        Terminate animation.
        """
        if self._thread:
            self._sm.set_current_time(self._start_time)
            self._animation = False
            self._thread.join()
            self._is_playing = None
            self._sm.disable_animation()

    def _play(self) -> None:
        """
        Play the animation.
        """
        self._is_playing = True

    def _pause(self) -> None:
        """
        Pause the animation.
        """
        self._is_playing = False
    
    def _stop(self) -> None:
        """
        Stop the animation.
        """
        self._is_playing = False

    def _iterate_frame(self) -> None:
        """
        Iterate the frame.
        """
        while self._animation:
            current_time = time.time()
            if hasattr(self, "_last_frame_time"):
                expected_frame_time = self._last_frame_time + (1.0 / self._sm.get_playback_speed())
            else:
                expected_frame_time = current_time
            if current_time < expected_frame_time:
                time.sleep(expected_frame_time - current_time)
            if self._is_playing:
                current_time = self._sm.get_current_time()
                if current_time >= self._end_time:
                    self._sm.set_current_time(self._start_time)
                else:
                    self._sm.set_current_time(current_time + 1.0)
                self._sm.update_skeletal_animation()
            self._last_frame_time = time.time()

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
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (5, 3))
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (0, 0))

        detail_panel_width = self._cfg['detail']['width']
        imgui.same_line()
        window_pos = imgui.get_window_pos()
        cursor_pos = imgui.get_cursor_pos()
        trackbar_bg_min = imgui.get_cursor_pos() + window_pos + imgui.ImVec2(3, 0)
        trackbar_bg_max = imgui.get_content_region_avail() + window_pos - imgui.ImVec2(detail_panel_width - cursor_pos[0], -1)
        self._draw_list.add_rect_filled(trackbar_bg_min, trackbar_bg_max, imgui.get_color_u32((0.3, 0.3, 0.3, 1)), rounding=2.0, flags=0)
        self._draw_list.add_rect(trackbar_bg_min, trackbar_bg_max, imgui.get_color_u32((0, 0, 0, 1)), rounding=2.0, flags=0)
        trackbar_inner_width = (trackbar_bg_max - trackbar_bg_min)[0] - 10
        trackbar_height = (trackbar_bg_max - trackbar_bg_min)[1]
        self._time_range = self._end_time - self._start_time
        frame_width = (trackbar_inner_width - 2.5) / (self._time_range + 1)
        imgui.set_cursor_pos((imgui.get_cursor_pos_x() + 10, imgui.get_cursor_pos_y() + 10))
        original_cursor_pos = imgui.get_cursor_pos()
        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() - (frame_width * 0.5))
        for index in range(1, int(self._time_range) + 2):
            cursor_pos_x = imgui.get_cursor_pos_x()
            line_color = imgui.get_color_u32((0.1, 0.1, 0.1, 1))
            line_width = 1.0
            if index == int(self._sm.get_current_time()):
                line_color = imgui.get_color_u32((0.75, 0.25, 0.25, 1))
                line_width = 3.0
            frame_pos = imgui.ImVec2(cursor_pos_x + frame_width + window_pos[0], trackbar_bg_min[1])
            frame_line_start = imgui.ImVec2(int(frame_pos[0]), int(frame_pos[1]))
            frame_line_end = frame_line_start + imgui.ImVec2(0, trackbar_height * 0.333)
            imgui.set_cursor_pos_x(frame_pos[0])
            self._draw_list.add_line(frame_line_start, frame_line_end, line_color, thickness=line_width)
        imgui.set_cursor_pos(original_cursor_pos - (5, 0))
        imgui.push_item_width(trackbar_inner_width + 5)
        if self._animation:
            flags = 0
        else:
            flags = imgui.SliderFlags_.no_input
        changed, value = imgui.slider_int("##trackbar", int(self._sm.get_current_time()), int(self._start_time), int(self._end_time), flags=flags)
        if self._animation and changed:
            self._sm.set_current_time(value)
            self._sm.update_skeletal_animation()
        imgui.pop_item_width()
        imgui.pop_style_color(5)
        imgui.pop_style_var(3)

    def _draw_animation_button(self) -> None:
        """
        Draw the enable/disable animation button toggle.
        """
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (2, 2))
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 2.0)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 1.0)

        if self._animation:
            imgui.push_style_color(imgui.Col_.button, imgui.get_color_u32((0.175, 0.4, 0.175, 1)))
            imgui.push_style_color(imgui.Col_.button_active, imgui.get_color_u32((0.15, 0.15, 0.15, 1)))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.get_color_u32((0.175, 0.6, 0.175, 1)))
            tint_color = (0.0, 0.0, 0.0, 1)
        else:    
            imgui.push_style_color(imgui.Col_.button, imgui.get_color_u32((0.4, 0.175, 0.175, 1)))
            imgui.push_style_color(imgui.Col_.button_active, imgui.get_color_u32((0.1, 0.1, 0.1, 1)))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.get_color_u32((0.6, 0.175, 0.175, 1)))
            tint_color = (0.0, 0.0, 0.0, 1)

        icon_size = (31, 31)
        enable_animation_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_ANIMATION, icon_size)
        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + 3)
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 3) 
        if imgui.image_button("##enable_animation", enable_animation_id, icon_size, tint_col=tint_color):
            if not self._animation:
                self._init_animation()
            else:
                self._terminate_animation()
        imgui.pop_style_color(3)
        imgui.pop_style_var(3)     

    def _draw_control_buttons(self) -> None:
        """
        Draw the control buttons.
        """
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (2, 2))
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 2.0)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 1.0)

        if self._animation:
            imgui.push_style_color(imgui.Col_.button, imgui.get_color_u32((0.3, 0.3, 0.3, 1)))
            imgui.push_style_color(imgui.Col_.button_active, imgui.get_color_u32((0.15, 0.15, 0.15, 1)))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.get_color_u32((0.4, 0.4, 0.4, 1)))
        else:
            imgui.push_style_color(imgui.Col_.button, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
            imgui.push_style_color(imgui.Col_.button_active, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))            

        button_size = imgui.ImVec2(20, 20)

        start_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_START, button_size)
        imgui.same_line()
        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + 10)
        cursor_y = imgui.get_cursor_pos_y() + 5
        imgui.set_cursor_pos_y(cursor_y)
        if imgui.image_button("##start", start_icon_id, button_size):
            if self._animation:
                self._sm.set_current_time(self._start_time)
                self._sm.update_skeletal_animation()
        play_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_PLAY, button_size)
        pause_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_PAUSE, button_size)
        imgui.same_line()
        imgui.set_cursor_pos_y(cursor_y)
        if self._is_playing: playpause_icon_id = pause_icon_id
        else: playpause_icon_id = play_icon_id
        if imgui.image_button("##playpause", playpause_icon_id, button_size, tint_col=(1, 1, 1, 1)):
            if self._animation:
                if not self._is_playing:
                    self._play()
                else:
                    self._pause()
        imgui.same_line()
        imgui.set_cursor_pos_y(cursor_y)
        stop_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_STOP, button_size)
        if imgui.image_button("##stop", stop_icon_id, button_size):
            if self._animation:
                self._stop()
                self._sm.set_current_time(self._start_time)
                self._sm.update_skeletal_animation()
        end_icon_id = cutils.FileHelper.read(cstat.Filetype.ICON, cstat.Icon.ICON_TRACKBAR_END, button_size)
        imgui.same_line()
        imgui.set_cursor_pos_y(cursor_y)
        if imgui.image_button("##end", end_icon_id, button_size):
            if self._animation:
                self._sm.set_current_time(self._end_time)
                self._sm.update_skeletal_animation()
        imgui.pop_style_color(3)
        imgui.pop_style_var(3)

    def _draw_motion_mode(self) -> None:
        """
        Draw the root motion combo box.
        """
        imgui.push_style_var(imgui.StyleVar_.frame_padding, (5, 5))
        imgui.push_style_var(imgui.StyleVar_.frame_rounding, 2.0)
        imgui.push_style_var(imgui.StyleVar_.frame_border_size, 1.0)
        imgui.push_style_var(imgui.StyleVar_.item_spacing, (5, 5))
        imgui.push_style_var(imgui.StyleVar_.window_padding, (5, 5))

        if self._animation:
            imgui.push_style_color(imgui.Col_.button, imgui.get_color_u32((0.3, 0.3, 0.3, 1)))
            imgui.push_style_color(imgui.Col_.button_active, imgui.get_color_u32((0.15, 0.15, 0.15, 1)))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.get_color_u32((0.4, 0.4, 0.4, 1)))
            imgui.push_style_color(imgui.Col_.frame_bg, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
            imgui.push_style_color(imgui.Col_.frame_bg_active, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
            imgui.push_style_color(imgui.Col_.frame_bg_hovered, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
        else:
            imgui.push_style_color(imgui.Col_.button, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
            imgui.push_style_color(imgui.Col_.button_active, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
            imgui.push_style_color(imgui.Col_.button_hovered, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))            
            imgui.push_style_color(imgui.Col_.frame_bg, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
            imgui.push_style_color(imgui.Col_.frame_bg_active, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))
            imgui.push_style_color(imgui.Col_.frame_bg_hovered, imgui.get_color_u32((0.2, 0.2, 0.2, 1)))

        if self._animation:
            motion_list = ["In Place", "Root Motion"]
            current_index = motion_list.index(self._motion_mode)
        else:
            motion_list = [""]
            current_index = 0
        imgui.same_line()
        imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() + 6)
        region_avail = imgui.get_content_region_avail()
        imgui.push_item_width(region_avail[0] - 7)  
        imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + 2)
        if imgui.begin_combo("##root_motion", motion_list[current_index]):
            for index, mode in enumerate(motion_list):
                imgui.push_id(index)
                changed, value = imgui.selectable(mode, False)
                if changed:
                    self._motion_mode = motion_list[index]
                    if self._animation:
                        if motion_list[index] == "In Place":
                            self._sm.zero_skeletal_root()
                            self._sm.enable_skeletal_animation()
                            self._sm.update_skeletal_animation()
                        elif motion_list[index] == "Root Motion":
                            self._sm.remove_skeletal_root_zero()
                            self._sm.update_skeletal_animation()
                            self._sm.enable_skeletal_animation()
                    imgui.set_item_default_focus()
                imgui.pop_id()
            imgui.end_combo()
        imgui.pop_item_width()
        imgui.pop_style_color(6)
        imgui.pop_style_var(5)

    def draw(self) -> None:
        """
        Draw the outliner panel.
        """
        imgui.set_next_window_size((self._panel_width, self._panel_height))
        imgui.set_next_window_pos(self._panel_position)
        imgui.begin(self._name, True, self._window_flags)
        self._draw_list = imgui.get_window_draw_list()
        self._draw_animation_button()
        self._draw_trackbar()
        self._draw_control_buttons()
        self._draw_motion_mode()
        self._draw_horizonal_line()

    def update_usd(self):
        super().update_usd()
        self._init_time()

        