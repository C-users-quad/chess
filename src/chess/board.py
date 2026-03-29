from core.utils import opposite_color
from core.enums import PieceColors
from ui.base import UIElement
from chess.square import BoardSquare
from chess.move import Move
from chess.pieces import (
    Piece,
    King,
    Knight,
    Pawn,
    Queen,
    Rook,
    Bishop,
    get_all_pieces_of_color,
)


class Board:
    """
    logical chess board.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.squares = [[BoardSquare((r, c), self) for c in range(8)] for r in range(8)]
        self.turn_color = PieceColors.WHITE  # whos turn it is
        self.white_king = None
        self.black_king = None
        self.checkmate = False
        self.stalemate = False
        self.timeout = False
        self.game_end = False
        self.winning_color = None
        self.captured_pieces: list[Piece] = []
        self.current_move: Move = None
        self.populate_board()  # give board initial pieces

    def detect_game_end(self):
        """
        detects game end and if it has ended also
        adjusts the values of related flags like checkmate or stalemate
        """

        pieces = get_all_pieces_of_color(self.turn_color, self)
        player_can_move = False
        for piece in pieces:
            if piece.get_legal_moves():
                player_can_move = True
                break

        if not player_can_move or self.timeout:
            self.game_end = True
        else:
            return  # if the game hasnt ended, further checks arent necessary.

        king = getattr(self, f"{self.turn_color}_king")
        if king.in_check():
            self.checkmate = True
        elif not king.in_check() and not player_can_move:
            self.stalemate = True

        white_king_sqr = self.get_square(self.white_king.pos)
        black_king_sqr = self.get_square(self.black_king.pos)
        king = getattr(self, f"{self.turn_color}_king")

        if self.timeout or king.in_check():
            self.winning_color = opposite_color(self.turn_color)
            winning_sqr = (
                white_king_sqr
                if self.winning_color == PieceColors.WHITE
                else black_king_sqr
            )
            losing_sqr = (
                white_king_sqr
                if self.winning_color != PieceColors.WHITE
                else black_king_sqr
            )
            winning_sqr.winning_square = True
            losing_sqr.losing_square = True

    def get_square(self, pos):
        row, col = pos
        return self.squares[row][col]

    def pos_on_board(self, pos):
        row, col = pos
        return 0 <= row <= 7 and 0 <= col <= 7

    def make_move(self, move: Move):
        """
        makes the move.

        precondition: move is legal.
        """
        if move.real_move:
            self.current_move = move
        move.check_flags_before_move()
        self._apply_move(move)
        move.check_flags_after_move()

    def unmake_move(self, move: Move):
        # reset squares
        self.place_piece(move.piece, move.start)
        self.remove_piece(move.end)
        if move.capture_square:
            self.place_piece(move.captured_piece, move.capture_square)

        # reset board
        self.reset_pawn_flags()
        self.change_turn()

        # reset piece
        move.piece.has_moved = move.original_has_moved
        if move.original_just_moved_forward_two:
            move.piece.just_moved_forward_two = move.original_just_moved_forward_two
        if move.is_castle:
            rook = self.get_square(move.rook_end).piece
            self.remove_piece(move.rook_end)
            self.place_piece(rook, move.rook_start)
            rook.has_moved = False

    def _apply_move(self, move: Move):
        self.remove_piece(move.start)
        self.place_piece(move.piece, move.end)
        self._capture_pawn_if_en_passant(move)
        self._move_rook_if_castling(move)
        self.reset_pawn_flags()
        self.change_turn()

    def place_piece(self, piece, pos):
        """
        place a piece on a square at pos.
        used during piece creation.
        """
        square = self.get_square(pos)
        square.place(piece)
        piece.update_pos(pos)

    def remove_piece(self, pos):
        square = self.get_square(pos)
        square.remove_piece()

    def change_turn(self):
        self.turn_color = opposite_color(self.turn_color)

    def populate_board(self):
        """adds the initial arrangement of chess pieces to the board"""
        # make back rows
        for color in PieceColors:
            row = 0 if color == PieceColors.BLACK else 7
            col = 0
            for piece_class in [
                Rook,
                Knight,
                Bishop,
                Queen,
                King,
                Bishop,
                Knight,
                Rook,
            ]:
                pos = (row, col)
                piece = piece_class(pos, color, self)
                self.place_piece(piece, pos)
                if isinstance(piece, King):
                    setattr(self, f"{color}_king", piece)
                col += 1

        # make pawns
        for color in PieceColors:
            row = 1 if color == PieceColors.BLACK else 6
            col = 0
            for _ in range(8):
                pos = (row, col)
                self.place_piece(Pawn(pos, color, self), pos)
                col += 1

    def _capture_pawn_if_en_passant(self, move: Move):
        # the piece thats moving must be a pawn
        if not isinstance(move.piece, Pawn):
            return

        # the position the piece is moving to must be an en passant move
        if not move.is_en_passant:
            return

        # capture the piece
        row, col = move.end
        victim_pos = (row - move.piece.dir, col)
        victim_square = self.get_square(victim_pos)
        victim_square.remove_piece()

    def _move_rook_if_castling(self, move: Move):
        if not move.is_castle:
            return

        # determine rooks initial and final positions
        kingside_castle_col = 6
        queenside_castle_col = 2

        if move.end[1] == kingside_castle_col:
            # kingside
            rook_initial_pos = (move.end[0], move.end[1] + 1)
            rook_final_pos = (move.end[0], move.end[1] - 1)
        elif move.end[1] == queenside_castle_col:
            # queenside
            rook_initial_pos = (move.end[0], move.end[1] - 2)
            rook_final_pos = (move.end[0], move.end[1] + 1)

        # move rook
        piece = self.get_square(rook_initial_pos).piece
        self.remove_piece(rook_initial_pos)
        self.place_piece(piece, rook_final_pos)

        # update move info
        move.rook_start = rook_initial_pos
        move.rook_end = rook_final_pos

    def reset_pawn_flags(self):
        """
        once the turn changes,
        make the previous mover's pawns' reset their en passant flags
        """
        previous_move_color = opposite_color(self.turn_color)
        for row in self.squares:
            for square in row:
                if square.is_empty():
                    continue
                if not isinstance(square.piece, Pawn):
                    continue
                if square.piece.color != previous_move_color:
                    continue
                square.piece.just_moved_forward_two = False
