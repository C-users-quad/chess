from core.settings import *
from ui.base import UIElement

class UIColoredRect(UIElement):
    def __init__(self, pos, size, anchor, color, **kwargs):
        super().__init__(pos=pos, size=size, anchor=anchor, **kwargs)
        self.color = color
        self.render()

    def render(self):
        self.resize()
        self.image.fill(self.color)
