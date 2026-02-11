from core.settings import *

class Clickable:
    def __init__(self, **kwargs):
        self.hover = False
        self.prev_hover = False
        super().__init__(**kwargs)

    def detect_hovering(self):
        self.prev_hover = self.hover
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())

    def detect_click(self):
        if not self.hover:
            return
        return pygame.mouse.get_just_released()[0]
