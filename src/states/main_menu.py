from core.settings import *
from states.base import GameState
from core.utils import get_tui_text_box
from ui.button import Button

class MainMenu(GameState):
    def __init__(self):
        super().__init__()
        self.draw_below = True
        thing = Button((250,100), (SPACING, SPACING), "quit",
            lambda: self.game.power_off())
        self.ui.append(thing)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.power_off()

    def update(self):
        for element in self.ui:
            element.update()

    def draw(self):
        for element in self.ui:
            element.draw()
