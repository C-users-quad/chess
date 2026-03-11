from core.settings import BASE_WIDTH, pygame
from core.utils import get_ui_elem
from core.enums import StateNames
from states.base import GameState
from ui.rects.text_box import UITextBox
from ui.composites.manager import UIManager


class SettingsMenu(GameState):
    """menu for game settings"""

    name = StateNames.SETTINGS

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
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

        title = UITextBox(
            pos=(BASE_WIDTH / 2, spacing),
            anchor="midtop",
            text="Settings",
            font_size="title",
            do_auto_size=True,
        )
        elements.append(title)

        self.ui = UIManager(elements)
