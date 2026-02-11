from core.settings import *

class ChessPiece:
    def __init__(self, color: Literal['white', 'black'], pos: tuple[int, int]):
        self.color = color
        self.pos = pos
        self.possible_moves = []

    @property
    def board(self):
        return GameContext.game.board

    def get_possible_moves(self):
        pass
