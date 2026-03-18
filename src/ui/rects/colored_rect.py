from core.settings import pygame, COLORS
from core.utils import get_ui_elem, scale
from ui.base import UIElement


class UIColoredRect(UIElement):
    """a colored rectangle"""

    def __init__(self, color: pygame.typing.ColorLike, rounding=False, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.rounding = rounding
        self.render()

    def render(self):
        self.resize()
        self.image.fill(COLORS["clear"])

        if self.rounding:
            rounding = scale(get_ui_elem("rounding"))
            pygame.draw.rect(
                surface=self.image,
                color=self.color,
                rect=self.image.get_rect(),
                border_radius=rounding,
            )
        else:
            self.image.fill(self.color)
