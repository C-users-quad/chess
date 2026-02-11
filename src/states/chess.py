from core.settings import *
from states.base import GameState

class Chess(GameState):
    def __init__(self):
        self.draw_below = True

    def handle_events(self):
        events = pygame.event.get()
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.game.push_state('main-menu')

    def update(self):
        self.game.board.update()

    def draw(self):
        self.game.board.draw()
