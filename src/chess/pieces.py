from core.settings import *
from core.utils import asset_path

# create piece images dict
PIECE_IMAGES = {}
"""(color, piecename) : Surface"""
for piece in ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']:
    for color in ['black', 'white']:
        key = (color, piece)
        filename = f'{piece}-{color}.png'
        path = join('assets', 'images', 'pieces', filename)
        PIECE_IMAGES[key] = pygame.image.load(asset_path(path))

# import piece images and make accessable with a dict, write the
# base piece class and write other piece classes.
class Piece:
    def __init__(self, pos, board, color, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.board = board
        self.color = color

    def get_valid_moves(self):
        pass

    def update_pos(self, pos):
        self.pos = pos

class SlidingPiece(Piece):
    def __init__(self, pos, board, color, **kwargs):
        super().__init__(pos=pos, board=board, color=color, **kwargs)

    def get_valid_moves(self):
        valid_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            while self.board.pos_on_board(row, col):
                curr_square = self.board.get_square(row, col)
                if curr_square.empty():
                    valid_moves.append((row, col))
                    row += dr
                    col += dc
                    continue
                if curr_square.piece.color != self.color:
                    valid_moves.append((row, col))
                    break
                if curr_square.piece.color == self.color:
                    break

        return valid_moves

class Rook(SlidingPiece):
    def __init__(self, pos, board, color, **kwargs):
        super().__init__(pos=pos, board=board, color=color, **kwargs)
        self.image = PIECE_IMAGES[(color, 'rook')]
        self.directions = [
                     (0, 1),
            (-1, 0),         (1, 0),
                     (0,-1),
        ]

class Bishop(SlidingPiece):
    def __init__(self, pos, board, color, **kwargs):
        super().__init__(pos=pos, board=board, color=color, **kwargs)
        self.image = PIECE_IMAGES[(color, 'bishop')]
        self.directions = [
            (-1, 1),        (1, 1),

            (-1,-1),        (1,-1)
        ]

class Queen(SlidingPiece):
    def __init__(self, pos, board, color, **kwargs):
        super().__init__(pos=pos, board=board, color=color, **kwargs)
        self.image = PIECE_IMAGES[(color, 'queen')]
        self.directions = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),         (1, 0),
            (-1,-1), (0,-1), (1,-1)
        ]
