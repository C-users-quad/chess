from core.settings import *
from ui.base import UIElement

class Button(UIElement):
    """button that when clicked executes click_action"""
    def __init__(self, size, pos, text, click_action, anchor="topleft"):
        super().__init__(size, pos, text, anchor)
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
            self.render_element()
        else:
            self.render_element(bg_color=COLORS['button-highlight'])

    def do_click_action(self):
        if self.hover and pygame.mouse.get_just_released()[0]:
            self.click_action()

    def update(self):
        self.detect_hovering()
        self.highlight_button()
        self.do_click_action()
