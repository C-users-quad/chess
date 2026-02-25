from core.settings import *
from core.enums import StateNames
from states.base import GameState
from chess.board import Board

class Chess(GameState):
    """game state with chess board"""
    name = StateNames.CHESS
    def __init__(self, board):
        super().__init__()
        self.dim = False
        self.board= board

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.board.reset_square_flags()
            self.game.push_state('main-menu')

    def update(self):
        self.board.update()

    def render(self, force_rendering=False):
        if not force_rendering and not self.game.window_resized():
            return
        self.board.render()

    def draw(self):
        self.board.draw()
