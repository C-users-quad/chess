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

def get_all_pieces_of_color(color: Literal['white', 'black']):
    pieces = []
    board = GameContext.game.board.board
    for row in board:
        for square in row:
            if square.empty():
                continue
            if square.piece.color == color:
                pieces.append(square.piece)

    return pieces

# import piece images and make accessable with a dict, write the
# base piece class and write other piece classes.
class Piece:
    name = None
    def __init__(self, pos, color, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.color = color
        self.has_moved = False
        self.image = PIECE_IMAGES[(color, self.name)]

    @property
    def board(self):
        return GameContext.game.board

    def get_pseudo_moves(self):
        pass

    def get_valid_moves(self):
        return self.filter_illegal_moves(self.get_pseudo_moves())

    def update_pos(self, pos):
        self.pos = pos

    def filter_illegal_moves(self, moves):
        original_board = GameContext.game.board
        legal_moves = []

        for move in moves:
            temp_board = deepcopy(original_board)
            GameContext.game.board = temp_board

            temp_piece = temp_board.get_square(*self.pos).piece
            temp_king = temp_board.white_king if self.color == 'white' else temp_board.black_king

            temp_board.move_piece(temp_piece, move)
            if not temp_king.in_check():
                legal_moves.append(move)

        GameContext.game.board = original_board
        return legal_moves

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

    def get_pseudo_moves(self):
        pseudo_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            while self.board.pos_on_board(row, col):
                curr_square = self.board.get_square(row, col)
                if curr_square.empty():
                    pseudo_moves.append((row, col))
                    row += dr
                    col += dc
                    continue
                if curr_square.piece.color != self.color:
                    pseudo_moves.append((row, col))
                    break
                if curr_square.piece.color == self.color:
                    break

        return pseudo_moves

class Rook(SlidingPiece):
    name = 'rook'
    directions = [
                (0, 1),
        (-1, 0),         (1, 0),
                (0,-1),
    ]
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)

class Bishop(SlidingPiece):
    name = 'bishop'
    directions = [
        (-1, 1),        (1, 1),

        (-1,-1),        (1,-1)
    ]
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)

class Queen(SlidingPiece):
    name = 'queen'
    directions = Rook.directions.copy()
    directions.extend(Bishop.directions)
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)

class Knight(Piece):
    name = 'knight'
    directions = [
        (-2,-1), (-2,1), (2,-1), (2,1),
        (-1,-2), (1,-2), (-1,2), (1,2)
    ]
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)

    def get_pseudo_moves(self):
        pseudo_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board(row, col):
                continue

            curr_square = self.board.get_square(row, col)
            if curr_square.empty():
                pseudo_moves.append((row, col))
            elif curr_square.piece.color != self.color:
                pseudo_moves.append((row, col))

        return pseudo_moves

class Pawn(Piece):
    name = 'pawn'
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)
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

    def get_pseudo_moves(self):
        pseudo_moves = []
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
                pseudo_moves.append((row, col))

        # check en passant
        pseudo_moves.extend(self.get_en_passant_moves())

        # check moving directly infront
        row, col = self.pos
        pos_infront = (row + self.dir, col)
        if self.board.pos_on_board(*pos_infront):
            square_infront = self.board.get_square(*pos_infront)
            if square_infront.empty():
                pseudo_moves.append(pos_infront)

        # check moving 2 squares forward
        if not self.has_moved:
            pos_2_infront = (row + self.dir*2, col)
            square_infront = self.board.get_square(*pos_infront)
            square_2_infront = self.board.get_square(*pos_2_infront)
            if square_infront.empty() and square_2_infront.empty():
                pseudo_moves.append(pos_2_infront)

        return pseudo_moves

class King(Piece):
    name = 'king'
    directions = Queen.directions
    def __init__(self, pos, color, **kwargs):
        super().__init__(pos=pos, color=color, **kwargs)

    def in_check(self):
        enemy_color = 'white' if self.color == 'black' else 'black'
        enemy_pieces = get_all_pieces_of_color(enemy_color)
        enemy_moves = []
        for piece in enemy_pieces:
            enemy_moves.extend(piece.get_pseudo_moves())

        return self.pos in enemy_moves

    def get_pseudo_moves(self):
        pseudo_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board(row, col):
                continue

            curr_square = self.board.get_square(row, col)
            if curr_square.empty() or curr_square.piece.color != self.color:
                pseudo_moves.append((row, col))

        return pseudo_moves
