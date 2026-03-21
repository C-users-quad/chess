from core.enums import SoundNames
from core.settings import CHECKBOX_RATIOS, COLORS, pygame
from core.sounds import playsound
from core.utils import get_ui_elem
from ui.base import UIElement
from ui.buttons.clickable import Clickable


class UICheckbox(UIElement, Clickable):
    """changes the value of a boolean based on input"""

    def __init__(
        self,
        value: bool,
        change_value: callable,
        side_length,
        **kwargs,
    ):
        super().__init__(
            size=(side_length, side_length),
            **kwargs,
        )
        self.value = value
        self.change_value = change_value

    def on_click(self):
        if not self.detect_release():
            return

        self.value = not self.value
        self.change_value(self.value)
        self.dirty = True

    def play_clicking_sound(self):
        if self.detect_press():
            playsound(SoundNames.BUTTON_DOWN)
        elif self.detect_release():
            playsound(SoundNames.BUTTON_UP)

    def update(self):
        self.detect_hovering()
        self.play_clicking_sound()
        self.on_click()

    def render(self):
        self.resize()
        self.image.fill(COLORS["clear"])

        # get necessary info
        rounding = get_ui_elem("rounding")
        image_rect = self.image.get_rect()

        # draw base followed by border
        base_color = (
            COLORS["checkbox-ticked"] if self.value else COLORS["checkbox-unticked"]
        )
        pygame.draw.rect(
            surface=self.image,
            color=base_color,
            rect=image_rect,
            border_radius=rounding,
        )
        pygame.draw.rect(
            surface=self.image,
            color=COLORS["checkbox-border"],
            rect=image_rect,
            width=int(self.rect.width * CHECKBOX_RATIOS["border"]),
            border_radius=rounding,
        )
