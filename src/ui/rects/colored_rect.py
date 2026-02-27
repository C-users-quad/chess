from core.settings import *
from core.utils import get_ui_elem, scale
from ui.base import UIElement

class UIColoredRect(UIElement):
    """a colored rectangle"""
    def __init__(self, pos, size, anchor, color,
                 resize_axis='auto', rounding=False, **kwargs):
        super().__init__(
            pos=pos,
            size=size,
            anchor=anchor,
            resize_axis=resize_axis,
            **kwargs
        )
        self.color = color
        self.rounding = rounding
        self.render()

    def render(self):
        self.resize()
        if self.rounding:
            rounding = scale(get_ui_elem('rounding'))
            pygame.draw.rect(
                surface=self.image,
                color=self.color,
                rect=self.image.get_rect(),
                border_radius=rounding
            )
        else:
            self.image.fill(self.color)
