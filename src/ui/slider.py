from core.settings import pygame, COLORS
from core.utils import clamp
from core.sounds import playsound, stopsound, is_playing
from core.enums import SoundNames
from ui.base import UIElement
from ui.buttons.clickable import Clickable


class SliderMarker(UIElement, Clickable):
    """draggable marker thats used with uislider."""

    def __init__(self, slider: UISlider, **kwargs):
        self.slider = slider
        self.base_radius = slider.base_size[1] / 2
        self.current_x = None
        super().__init__(
            pos=(self.base_radius, self.base_radius),
            size=(self.base_radius * 2, self.base_radius * 2),
            anchor="center",
            resize_axis=slider.resize_axis,
            **kwargs,
        )
        self.render()

    @property
    def screen_rect(self):
        """
        override clickables screen rect property so that it
        avoids using this class's self.rect which is positioned relative
        to self.widget and not to the screen
        """
        return self.rect.move(self.slider.rect.topleft)

    def set_current_x(self):
        value_range = self.slider.max_value - self.slider.min_value
        print(self.slider.curr_value, self.slider.min_value)
        percent_range = (self.slider.curr_value - self.slider.min_value) / \
            value_range
        marker_radius = self.slider.image.height / 2
        self.current_x = clamp(
            value=self.slider.image.width * percent_range,
            min_value=marker_radius,
            max_value=self.slider.image.width - marker_radius,
        )

    def update_value(self):
        """
        updates the sliders current value based
        on the current position of the marker
        """
        marker_radius = self.slider.rect.height / 2
        min_x, max_x = marker_radius, self.slider.rect.width - marker_radius
        x_range = max_x - min_x
        percent_x_range = (self.current_x - marker_radius) / x_range
        value_range = self.slider.max_value - self.slider.min_value
        self.slider.curr_value = percent_x_range * value_range + self.slider.min_value
        if self.slider.on_change:
            self.slider.on_change(self.slider.curr_value)

    def handle_sound(self):
        if not self.detect_held_down():
            stopsound(SoundNames.SLIDER)
            return

        if is_playing(SoundNames.SLIDER):
            return

        if not self.game.mouse_moved():
            return

        playsound(SoundNames.SLIDER)

    def on_drag(self):
        # if not being dragged, return.
        if not self.detect_held_down():
            return

        new_x = pygame.mouse.get_pos()[0] - self.slider.rect.left

        marker_radius = self.slider.image.height / 2
        new_x = clamp(
            value=new_x,
            min_value=marker_radius,
            max_value=self.slider.image.width - marker_radius,
        )

        # reposition rect at new x and rerender to display results
        self.current_x = new_x
        self.update_value()
        self.slider.dirty = True

    def update(self):
        self.detect_hovering()
        self.detect_press()
        self.handle_sound()
        self.on_drag()

    def resize(self):
        """overrides resize with relative positioning"""
        screen_radius = self.slider.image.height / 2
        self.image = pygame.transform.smoothscale(
            surface=self.image, size=(screen_radius * 2, screen_radius * 2)
        )

        self.set_current_x()
        self.rect = self.image.get_rect(center=(self.current_x, screen_radius))

    def render(self):
        self.resize()
        self.image.fill(COLORS["clear"])

        screen_radius = self.slider.image.height / 2
        pygame.draw.circle(
            surface=self.image,
            color=COLORS["text"],
            center=(screen_radius, screen_radius),
            radius=screen_radius,
        )

        self.slider.image.blit(self.image, self.rect)


class UISlider(UIElement):
    """slider that updates a value based on the position of its marker"""

    def __init__(
        self,
        pos,
        size,
        anchor,
        resize_axis,
        value,
        min_value,
        max_value,
        on_change: callable = None,
        **kwargs,
    ):
        """
        Note: the argument on_change should be passed in as:

        ```
        slider = UISlider(
            ...,
            on_change=lambda value: setattr(
                value_parent_object, "value_variable_name", value
            ),
            ...
        )
        ```
        """
        super().__init__(
            pos=pos, size=size, anchor=anchor, resize_axis=resize_axis, **kwargs
        )
        self.min_value = min_value
        self.max_value = max_value
        self.curr_value = value
        self.marker = SliderMarker(self)
        self.on_change = on_change
        self.render()

    def update(self):
        self.marker.update()

    def render(self):
        self.resize()
        self.marker.resize()
        self.image.fill(COLORS["clear"])

        # get necessary values
        marker_center_x = int(self.marker.current_x)
        marker_radius = self.marker.image.width // 2
        image_rect = self.image.get_rect()

        # construct light and dark rects
        dark_rect = image_rect.copy()
        dark_rect.width = marker_center_x + marker_radius

        light_rect = image_rect.copy()
        light_rect.left = marker_center_x - marker_radius
        light_rect.width -= marker_center_x - marker_radius

        # render the dark and light half, separated by the marker
        pygame.draw.rect(
            surface=self.image,
            color=COLORS["slider-base-dark"],
            rect=dark_rect,
            border_radius=marker_radius,
        )
        pygame.draw.rect(
            surface=self.image,
            color=COLORS["slider-base-light"],
            rect=light_rect,
            border_radius=marker_radius,
        )

        # draw slider marker
        self.marker.render()
        self.image.blit(self.marker.image, self.marker.rect)
