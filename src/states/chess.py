from core.settings import pygame
from core.enums import StateNames
from chess.board import Board
from states.base import GameState


class Chess(GameState):
    """game state with chess board"""

    name = StateNames.CHESS

    def __init__(self):
        super().__init__()
        self.dim = False
        self.board = Board()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.board.reset_square_flags()
            self.game.push_state(StateNames.MAIN_MENU)

    def update(self):
        self.board.update()

    def render(self, force_rendering=False):
        if not force_rendering and not self.game.window_resized():
            return
        self.board.render()

    def draw(self):
        self.board.draw()
