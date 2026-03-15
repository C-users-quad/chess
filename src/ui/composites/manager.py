from core.settings import GameContext
from core.utils import get_tui_text_box
from ui.base import UIElement


class UIManager:
    def __init__(self, elements: list[UIElement]):
        """
        manages a collection of ui elements
        """
        self.elements = elements

    @property
    def game(self):
        return GameContext.game

    def render(self, force_rendering=False):
        for element in self.elements:
            if not force_rendering \
                and not self.game.window_resized() \
                    and not element.dirty:
                        continue
            element.render()

    def draw(self):
        for element in self.elements:
            element.draw()

    def update(self):
        for element in self.elements:
            element.update()

    def __str__(self):
        lines = f"UIManager {hex(id(self))}\nElements: {self.elements}"

        return get_tui_text_box(lines)
