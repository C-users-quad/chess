from core.settings import COLORS, pygame
from core.utils import get_tui_text_box
from core.sounds import playsound
from core.enums import SoundNames
from ui.base import UIElement
from ui.buttons.clickable import Clickable


class UIButton(UIElement, Clickable):
    """ui button class that is clickable and has a sprite"""

    def __init__(
        self,
        pos,
        size,
        anchor,
        click_action,
        click_action_args=None,
        resize_axis="auto",
        **kwargs,
    ):
        super().__init__(
            pos=pos, size=size, anchor=anchor, resize_axis=resize_axis, **kwargs
        )
        self.click_action = click_action
        self.click_action_args = click_action_args
        self.highlight = None

    def render_highlight(self):
        overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        overlay.fill(COLORS["button-highlight"])

        # multiply overlay by the button image
        overlay.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.highlight = overlay

    def render(self):
        super().render()
        self.highlight = None

    def draw(self):
        super().draw()
        self.draw_highlight()

    def draw_highlight(self):
        if self.highlight:
            self.game.display.blit(self.highlight, self.rect)

    def highlight_button(self):
        if self.hover == self.prev_hover:
            return
        if not self.hover:
            # remove highlight
            self.highlight = None
        else:
            # render highlight
            self.render_highlight()

    def do_click_action(self):
        if not self.detect_release():
            return

        if self.click_action_args:
            self.click_action(*self.click_action_args)
        else:
            self.click_action()

    def play_button_sounds(self):
        if self.detect_press():
            playsound(SoundNames.BUTTON_DOWN)
        elif self.detect_release():
            playsound(SoundNames.BUTTON_UP)

    def debug(self):
        if self.hover and self.game.debug:
            print(self)

    def update(self):
        self.play_button_sounds()
        self.detect_hovering()
        self.highlight_button()
        self.do_click_action()
        self.debug()

    def __str__(self):
        text = (
            f"Button {hex(id(self))}\n"
            f"Size: {self.rect.size}\n"
            f"Topleft: {self.rect.topleft}\n"
            f"Center: {self.rect.center}\n"
            f"Bottomright: {self.rect.bottomright}\n"
            f"Mouse hovering: {self.hover}\n"
            f"Click action: {self.click_action.__name__}\n"
            f"Click action args: {self.click_action_args}"
        )
        return get_tui_text_box(text)
