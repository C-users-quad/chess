from core.settings import pygame


class Clickable:
    """class for clickable elements on screen"""

    def __init__(self, **kwargs):
        self.hover = False
        self.prev_hover = False
        super().__init__(**kwargs)

    def detect_hovering(self):
        """must be called before calling other methods here"""
        self.prev_hover = self.hover
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())

    def detect_press(self):
        if not self.hover:
            return False

        return pygame.mouse.get_just_pressed()[0]

    def detect_release(self):
        if not self.hover:
            return False

        return pygame.mouse.get_just_released()[0]

    def detect_held_down(self):
        if not self.hover:
            return False

        return pygame.mouse.get_pressed()[0]
