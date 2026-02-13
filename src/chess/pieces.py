from core.settings import *
from core.utils import asset_path, get_tui_text_box

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
    def __init__(self, pos, color, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.color = color
        self.has_moved = False

    @property
    def board(self):
        return GameContext.game.board

    def get_valid_moves(self):
        pass

    def update_pos(self, pos):
        self.pos = pos

    def __str__(self):
        lines = (
            f"{self.name} {hex(id(self))}\n"
            f"Pos: {self.pos}\n"
            f"Color: {self.color}\n"
            f"Valid Moves: {self.get_valid_moves()}"
        )

        return get_tui_text_box(lines)

class SlidingPiece(Piece):
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)

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
    name = 'rook'
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)
        self.image = PIECE_IMAGES[(color, self.name)]
        self.directions = [
                     (0, 1),
            (-1, 0),         (1, 0),
                     (0,-1),
        ]

class Bishop(SlidingPiece):
    name = 'bishop'
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)
        self.image = PIECE_IMAGES[(color, self.name)]
        self.directions = [
            (-1, 1),        (1, 1),

            (-1,-1),        (1,-1)
        ]

class Queen(SlidingPiece):
    name = 'queen'
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)
        self.image = PIECE_IMAGES[(color, self.name)]
        self.directions = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),         (1, 0),
            (-1,-1), (0,-1), (1,-1)
        ]

class Knight(Piece):
    name = 'knight'
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)
        self.image = PIECE_IMAGES[(color, self.name)]
        self.directions = [
            (-2,-1), (-2,1), (2,-1), (2,1),
            (-1,-2), (1,-2), (-1,2), (1,2)
        ]

    def get_valid_moves(self):
        valid_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board(row, col):
                continue

            curr_square = self.board.get_square(row, col)
            if curr_square.empty():
                valid_moves.append((row, col))
            elif curr_square.piece.color != self.color:
                valid_moves.append((row, col))

        return valid_moves

class Pawn(Piece):
    name = 'pawn'
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)
        self.image = PIECE_IMAGES[(color, self.name)]
        # determines if the pawn moves up or down the board depending on its color
        self.dir = -1 if color == 'white' else 1
        self.attack_moves = [
            (self.dir,-1),(self.dir,1)
        ]
        self.just_moved_forward_two = False

    def update_pos(self, pos):
        # pawn-specific check used for en passant
        if pos[0] == self.pos[0] + self.dir*2:
            self.just_moved_forward_two = True
        # the actual updating of the position
        self.pos = pos

    def get_en_passant_moves(self):
        en_passant_moves = []
        for dr, dc in self.attack_moves:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board(row, col):
                continue

            curr_square = self.board.get_square(row, col)
            if curr_square.empty():
                square_adjacent = self.board.get_square(row-self.dir, col)
                if square_adjacent.empty():
                    continue
                # adjacent square must have a pawn
                if not square_adjacent.piece.name == self.name:
                    continue
                # target squares pawn must have just double moved
                if not square_adjacent.piece.just_moved_forward_two:
                    continue
                # en passant
                en_passant_moves.append((row, col))
                continue

        return en_passant_moves

    def get_valid_moves(self):
        valid_moves = []
        # check attacking squares
        for dr, dc in self.attack_moves:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board(row, col):
                continue

            curr_square = self.board.get_square(row, col)
            if curr_square.empty():
                continue

            if curr_square.piece.color != self.color:
                valid_moves.append((row, col))

        # check en passant
        valid_moves.extend(self.get_en_passant_moves())

        # check moving directly infront
        row, col = self.pos
        pos_infront = (row + self.dir, col)
        if self.board.pos_on_board(*pos_infront):
            square_infront = self.board.get_square(*pos_infront)
            if square_infront.empty():
                valid_moves.append(pos_infront)

        # check moving 2 squares forward
        if not self.has_moved:
            valid_moves.append((row + 2*self.dir, col))

        return valid_moves
