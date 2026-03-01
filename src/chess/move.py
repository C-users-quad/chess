from core.sounds import PIECE_SOUNDS
from core.utils import get_all_pieces_of_color, opposite_color
from core.enums import PieceNames


class Move:
    """
    Stores info about a move

    precondition: move is legal
    """

    def __init__(self, piece, end_pos, board, real_move=True):
        self.piece = piece
        self.start = piece.pos
        self.end = end_pos
        self.capture_square = None
        self.promotion_piece = None
        self.captured_piece = None
        self.rook_start = None
        self.rook_end = None
        self.original_has_moved = None
        self.original_just_moved_forward_two = None

        # flags
        self.is_en_passant = False
        self.is_castle = False
        self.gives_check = False
        self.ends_game = False
        self.double_pawn_push = False
        self.is_promotion = False
        self.real_move = real_move
        self.board = board

    def check_flags_before_move(self):
        from chess.pieces import Pawn, King

        # has moved
        self.original_has_moved = self.piece.has_moved

        # capture
        end_sqr = self.board.get_square(self.end)
        if not end_sqr.empty():
            self.captured_piece = end_sqr.piece
            self.capture_square = end_sqr.piece.pos

        # en passant, double pawn push, promotion
        if isinstance(self.piece, Pawn):
            self.original_just_moved_forward_two = self.piece.just_moved_forward_two
            if self.end in self.piece.get_en_passant_moves():
                self.is_en_passant = True
                victim_sqr = self.board.get_square((self.start[0], self.end[1]))
                self.captured_piece = victim_sqr.piece
                self.capture_square = victim_sqr.piece.pos
            if self.end[0] == self.start[0] + self.piece.dir * 2:
                self.double_pawn_push = True
            if self.end[0] == self.piece.promotion_row:
                self.is_promotion = True

        # castle
        if isinstance(self.piece, King):
            castling_moves = self.piece.get_castling_moves()
            if castling_moves and self.end in castling_moves:
                self.is_castle = True

    def check_flags_after_move(self):
        if not self.real_move:
            return

        # deteremines if gives check/checkmate
        enemy_color = opposite_color(self.piece.color)
        enemy_king = getattr(self.board, f"{enemy_color.value}_king")
        if enemy_king.in_check():
            self.gives_check = True
        if all(
            not piece.get_legal_moves()
            for piece in get_all_pieces_of_color(enemy_color, self.board)
        ):
            self.ends_game = True

    def play_move_sound(self):
        if not self.real_move:
            return

        if self.ends_game:
            PIECE_SOUNDS["game-end"].play()
        elif self.gives_check:
            PIECE_SOUNDS["check"].play()
        elif self.is_castle:
            PIECE_SOUNDS["castle"].play()
        elif self.is_promotion:
            PIECE_SOUNDS["promote"].play()
        elif self.capture_square:
            PIECE_SOUNDS["capture"].play()
        else:
            PIECE_SOUNDS["move"].play()

    def set_promotion_piece(self, piece_name):
        from chess.pieces import Queen, Rook, Bishop, Knight

        piece_class = None
        match piece_name:
            case PieceNames.QUEEN:
                piece_class = Queen
            case PieceNames.ROOK:
                piece_class = Rook
            case PieceNames.BISHOP:
                piece_class = Bishop
            case PieceNames.KNIGHT:
                piece_class = Knight

        self.board.place_piece(
            piece=piece_class(self.end, self.piece.color, self.board), pos=self.end
        )
