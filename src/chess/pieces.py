from core.utils import get_all_pieces_of_color, get_tui_text_box, opposite_color
from core.images import PIECE_IMAGES
from core.enums import PieceColors, PieceNames
from chess.move import Move


class Piece:
    """base piece class for logical chess pieces"""

    name = None
    value = 0

    def __init__(self, pos, color, board, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.color = color
        self.has_moved = False
        self.image = PIECE_IMAGES[(color, self.name)]
        self.board = board

    def get_attack_moves(self):
        """
        gets a list of positions corresponding to attack moves.
        does not consider move legality.
        """
        pass

    def get_pseudo_moves(self):
        """
        gets a list of positions corresponding to possible moves.
        does not consider move legality.
        """
        pass

    def get_legal_moves(self):
        """
        gets a list of legal moves the piece can make.
        """
        return self.filter_illegal_moves(self.get_pseudo_moves())

    def update_pos(self, pos):
        """
        precondition: this is a legal move.
        sets the pieces position to one passed in by pos argument.
        """
        self.pos = pos

    def filter_illegal_moves(self, moves):
        """
        takes in pseudo moves and returns a list of move objects
        that are all legal moves.
        """
        legal_moves = []
        king = getattr(self.board, f"{self.color}_king")

        for end_pos in moves:
            move = Move(self, end_pos, self.board, real_move=False)
            self.board.make_move(move)
            if not king.in_check():
                legal_moves.append(end_pos)
            self.board.unmake_move(move)

        return legal_moves

    def __str__(self):
        lines = (
            f"{self.name} {hex(id(self))}\n"
            f"Pos: {self.pos}\n"
            f"Color: {self.color}\n"
            f"Has moved: {self.has_moved}\n"
            f"Legal Moves: {self.get_legal_moves()[:2]}..."
        )

        return get_tui_text_box(lines)


class SlidingPiece(Piece):
    def __init__(self, pos, color, board, **kwargs):
        super().__init__(pos=pos, color=color, board=board, **kwargs)

    def get_attack_moves(self):
        return self.get_pseudo_moves()

    def get_pseudo_moves(self):
        pseudo_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            while self.board.pos_on_board((row, col)):
                curr_square = self.board.get_square((row, col))
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
    name = PieceNames.ROOK
    value = 5
    directions = [
        (0, 1),
        (-1, 0),
        (1, 0),
        (0, -1),
    ]

    def __init__(self, pos, color, board, **kwargs):
        super().__init__(pos=pos, color=color, board=board, **kwargs)


class Bishop(SlidingPiece):
    name = PieceNames.BISHOP
    value = 3
    directions = [(-1, 1), (1, 1), (-1, -1), (1, -1)]

    def __init__(self, pos, color, board, **kwargs):
        super().__init__(pos=pos, color=color, board=board, **kwargs)


class Queen(SlidingPiece):
    name = PieceNames.QUEEN
    value = 9
    directions = Rook.directions.copy()
    directions.extend(Bishop.directions)

    def __init__(self, pos, color, board, **kwargs):
        super().__init__(pos=pos, color=color, board=board, **kwargs)


class Knight(Piece):
    name = PieceNames.KNIGHT
    value = 3
    directions = [
        (-2, -1),
        (-2, 1),
        (2, -1),
        (2, 1),
        (-1, -2),
        (1, -2),
        (-1, 2),
        (1, 2),
    ]

    def __init__(self, pos, color, board, **kwargs):
        super().__init__(pos=pos, color=color, board=board, **kwargs)

    def get_attack_moves(self):
        return self.get_pseudo_moves()

    def get_pseudo_moves(self):
        pseudo_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board((row, col)):
                continue

            curr_square = self.board.get_square((row, col))
            if curr_square.empty():
                pseudo_moves.append((row, col))
            elif curr_square.piece.color != self.color:
                pseudo_moves.append((row, col))

        return pseudo_moves


class Pawn(Piece):
    name = PieceNames.PAWN
    value = 1

    def __init__(self, pos, color, board, **kwargs):
        super().__init__(pos=pos, color=color, board=board, **kwargs)
        # determines if the pawn moves up or down the board depending on its color
        self.dir = -1 if color == PieceColors.WHITE else 1
        self.attack_moves = [(self.dir, -1), (self.dir, 1)]
        self.just_moved_forward_two = False
        self.promotion_row = 0 if self.color == PieceColors.WHITE else 7

    def update_pos(self, pos):
        # pawn-specific check used for en passant
        if pos[0] == self.pos[0] + self.dir * 2:
            self.just_moved_forward_two = True
        # the actual updating of the position
        self.pos = pos

    def get_attack_moves(self):
        attack_moves = []
        for dr, dc in self.attack_moves:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board((row, col)):
                continue

            attack_moves.append((row, col))

        return attack_moves

    def get_en_passant_moves(self):
        en_passant_moves = []
        for dr, dc in self.attack_moves:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board((row, col)):
                continue

            curr_square = self.board.get_square((row, col))
            if curr_square.empty():
                square_adjacent = self.board.get_square((row - self.dir, col))
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

        return en_passant_moves

    def get_pseudo_moves(self):
        pseudo_moves = []
        # check attacking squares
        for dr, dc in self.attack_moves:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board((row, col)):
                continue

            curr_square = self.board.get_square((row, col))
            if curr_square.empty():
                continue

            if curr_square.piece.color != self.color:
                pseudo_moves.append((row, col))

        # check en passant
        pseudo_moves.extend(self.get_en_passant_moves())

        # check moving directly infront
        row, col = self.pos
        pos_infront = (row + self.dir, col)
        if self.board.pos_on_board(pos_infront):
            square_infront = self.board.get_square(pos_infront)
            if square_infront.empty():
                pseudo_moves.append(pos_infront)

        # check moving 2 squares forward
        if not self.has_moved:
            pos_2_infront = (row + self.dir * 2, col)
            square_infront = self.board.get_square(pos_infront)
            square_2_infront = self.board.get_square(pos_2_infront)
            if square_infront.empty() and square_2_infront.empty():
                pseudo_moves.append(pos_2_infront)

        return pseudo_moves


class King(Piece):
    name = PieceNames.KING
    directions = Queen.directions

    def __init__(self, pos, color, board, **kwargs):
        super().__init__(pos=pos, color=color, board=board, **kwargs)

    def in_check(self):
        enemy_color = opposite_color(self.color)
        enemy_pieces = get_all_pieces_of_color(enemy_color, self.board)
        enemy_moves = []
        for piece in enemy_pieces:
            enemy_moves.extend(piece.get_attack_moves())

        return self.pos in enemy_moves

    def get_castling_moves(self):
        castling_moves = []
        if self.has_moved:
            return

        if self.in_check():
            return

        row, col = self.pos
        castle_sides = {
            "kingside": [(row, col + 1), (row, col + 2)],
            "queenside": [(row, col - 1), (row, col - 2), (row, col - 3)],
        }

        for side, squares in castle_sides.items():
            # check if rook has moved
            rook_col = 7 if side == "kingside" else 0
            rook_square = self.board.get_square((row, rook_col))
            if rook_square.empty() or rook_square.piece.has_moved:
                continue

            # check if no pieces in the way
            if any(not self.board.get_square(sqr).empty() for sqr in squares):
                continue

            # check if castling side is under attack
            path_squares = squares[:-1]
            enemy_color = opposite_color(self.color)
            if any(
                sq in piece.get_attack_moves()
                for piece in get_all_pieces_of_color(enemy_color, self.board)
                for sq in path_squares
            ):
                continue

            # pass all checks, allow castling move.
            castling_moves.append(squares[1])

        return castling_moves

    def get_attack_moves(self):
        attack_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board((row, col)):
                continue
            attack_moves.append((row, col))

        return attack_moves

    def get_pseudo_moves(self):
        pseudo_moves = []
        for dr, dc in self.directions:
            row, col = self.pos
            row, col = row + dr, col + dc
            if not self.board.pos_on_board((row, col)):
                continue

            curr_square = self.board.get_square((row, col))
            if curr_square.empty() or curr_square.piece.color != self.color:
                pseudo_moves.append((row, col))

        castling_moves = self.get_castling_moves()
        if castling_moves:
            pseudo_moves.extend(castling_moves)

        return pseudo_moves
