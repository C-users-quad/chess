from core.settings import pygame


class Clickable:
    """class for clickable elements on screen"""

    def __init__(self, **kwargs):
        self.hover = False
        self.prev_hover = False
        self.dragging = False
        super().__init__(**kwargs)

    @property
    def screen_rect(self):
        """
        the current objects rect positioned in coordinates relative to window space
        """
        return self.rect

    def detect_hovering(self):
        """must be called before calling other methods here"""
        self.prev_hover = self.hover
        self.hover = self.screen_rect.collidepoint(pygame.mouse.get_pos())

    def detect_press(self):
        if not self.hover:
            return False

        pressed = pygame.mouse.get_just_pressed()[0]
        if pressed:
            self.dragging = True

        return pressed

    def detect_release(self):
        released = pygame.mouse.get_just_released()[0]
        if released:
            self.dragging = False

        if not self.hover:
            return False

        return released

    def detect_held_down(self):
        if not self.dragging:
            return False

        return pygame.mouse.get_pressed()[0]
