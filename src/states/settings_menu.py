import pygame
from core.settings import BASE_WIDTH
from core.utils import get_ui_elem
from core.images import PIECE_IMAGES
from core.enums import PieceColors, PieceNames, StateNames
from states.base import GameState
from ui.rects.text_box import UITextBox
from ui.buttons.image_button import UIImageButton
from ui.manager import UIManager


class SettingsMenu(GameState):
    """menu for game settings"""

    name = StateNames.SETTINGS

    def __init__(self):
        super().__init__()
        self.ui = UIManager(elements=self.make_ui())

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event)

    def handle_input(self, keyevent):
        if keyevent.key == pygame.K_ESCAPE:
            self.game.pop_state()

    def update(self):
        self.ui.update()

    def render(self, force_rendering=False):
        self.ui.render(force_rendering)

    def draw(self):
        self.ui.draw()

    def make_ui(self):
        elements = []

        spacing = get_ui_elem("spacing")
        padding = get_ui_elem("padding")
        rounding = get_ui_elem("rounding")

        title = UITextBox(
            pos=(BASE_WIDTH / 2, spacing),
            anchor="midtop",
            text="Settings",
            font_size="title",
            do_auto_size=True,
        )
        elements.append(title)

        return elements
