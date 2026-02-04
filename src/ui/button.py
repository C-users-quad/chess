from core.settings import *
from core.utils import get_tui_text_box
from ui.text_box import UITextBox

class UIButton(UITextBox):
    """button that when clicked executes click_action"""
    def __init__(self, pos, anchor, text, font_size,
            click_action, auto_size=False, size=(0,0)):
        super().__init__(pos, anchor, text, font_size, auto_size, size)
        self.click_action = click_action
        self.hover = False
        self.prev_hover = False

    def detect_hovering(self):
        self.prev_hover = self.hover
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())

    def highlight_button(self):
        if self.hover == self.prev_hover:
            return
        if not self.hover:
            # re-render without highlight
            self.render_element()
        else:
            # re-render with highlight
            self.render_element(bg_color=COLORS['button-highlight'])

    def do_click_action(self):
        if self.hover and pygame.mouse.get_just_released()[0]:
            self.click_action()

    def update(self):
        self.detect_hovering()
        self.highlight_button()
        self.do_click_action()

    def __str__(self):
        text = (
            f"Button {hex(id(self))}\n"
            f"Size: {self.rect.size}\n"
            f"Topleft: {self.rect.topleft}\n"
            f"Center: {self.rect.center}\n"
            f"Bottomright: {self.rect.bottomright}\n"
            f"Text: {self.text}\n"
            f"Font size: {self.font_size}\n"
            f"Mouse hovering: {self.hover}"
        )
        return get_tui_text_box(text)
