from core.settings import *
from states.base import GameState
from chess.board import Board

class Chess(GameState):
    def __init__(self):
        super().__init__()
        self.dim = False

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.game.board.reset_flags()
            self.game.push_state('main-menu')

    def update(self):
        self.game.board.update()

    def render(self, force):
        if not force and not self.game.window_resized():
            return
        self.game.board.render()

    def draw(self, force_rendering=False):
        self.render(force_rendering)
        self.game.board.draw()
