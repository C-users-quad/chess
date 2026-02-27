from core.settings import *
from core.utils import get_tui_text_box
from ui.base import UIElement

class UIManager(UIElement):
    def __init__(self, elements: list[UIElement]):
        """
        manages a collection of ui elements
        """
        self.elements = elements

    def render(self, force_rendering=False):
        if not force_rendering and not self.game.window_resized():
            return
        for element in self.elements:
            element.render()

    def draw(self):
        for element in self.elements:
            element.draw()

    def update(self):
        for element in self.elements:
            element.update()

    def __str__(self):
        lines = (
            f"UIManager {hex(id(self))}\n"
            f"Elements: {self.elements}"
        )

        return get_tui_text_box(lines)
