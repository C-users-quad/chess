from chess.pieces import Rook, King
from chess.move import Move
from core.enums import PieceColors, PieceNames


class TestBoardInitialization:
    def test_board_has_8_rows(self, empty_board):
        assert len(empty_board.board) == 8

    def test_board_has_8_cols(self, empty_board):
        assert len(empty_board.board[0]) == 8

    def test_board_initial_turn_is_white(self, full_board):
        assert full_board.turn_color == PieceColors.WHITE

    def test_board_initial_state(self, empty_board):
        assert empty_board.checkmate is False
        assert empty_board.stalemate is False
        assert empty_board.game_end is False


class TestBoardPositionChecks:
    def test_pos_on_board_valid_center(self, empty_board):
        assert empty_board.pos_on_board((4, 4)) is True

    def test_pos_on_board_valid_corner(self, empty_board):
        assert empty_board.pos_on_board((0, 0)) is True
        assert empty_board.pos_on_board((7, 7)) is True

    def test_pos_on_board_invalid_row_negative(self, empty_board):
        assert empty_board.pos_on_board((-1, 4)) is False

    def test_pos_on_board_invalid_row_too_large(self, empty_board):
        assert empty_board.pos_on_board((8, 4)) is False

    def test_pos_on_board_invalid_col_negative(self, empty_board):
        assert empty_board.pos_on_board((4, -1)) is False

    def test_pos_on_board_invalid_col_too_large(self, empty_board):
        assert empty_board.pos_on_board((4, 8)) is False


class TestBoardGetSquare:
    def test_get_square_returns_square(self, empty_board):
        square = empty_board.get_square((0, 0))
        assert square is not None
        assert square.pos == (0, 0)

    def test_get_square_different_positions(self, empty_board):
        assert empty_board.get_square((0, 0)).pos == (0, 0)
        assert empty_board.get_square((7, 7)).pos == (7, 7)
        assert empty_board.get_square((3, 5)).pos == (3, 5)


class TestBoardPlaceAndRemovePieces:
    def test_place_piece(self, empty_board):
        rook = Rook((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (0, 0))
        assert empty_board.get_square((0, 0)).piece == rook

    def test_remove_piece(self, empty_board):
        rook = Rook((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (0, 0))
        empty_board.remove_piece((0, 0))
        assert empty_board.get_square((0, 0)).empty() is True

    def test_place_and_remove_preserves_piece_pos(self, empty_board):
        rook = Rook((5, 5), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (3, 3))
        assert rook.pos == (3, 3)


class TestBoardPopulation:
    def test_populate_board_creates_kings(self, full_board):
        assert full_board.white_king is not None
        assert full_board.black_king is not None

    def test_populate_board_creates_queens(self, full_board):
        white_queen = full_board.get_square((7, 3)).piece
        black_queen = full_board.get_square((0, 3)).piece
        assert white_queen.name == PieceNames.QUEEN
        assert black_queen.name == PieceNames.QUEEN

    def test_populate_board_creates_rooks(self, full_board):
        rooks = [
            full_board.get_square((7, 0)).piece,
            full_board.get_square((7, 7)).piece,
            full_board.get_square((0, 0)).piece,
            full_board.get_square((0, 7)).piece,
        ]
        assert all(r.name == PieceNames.ROOK for r in rooks)

    def test_populate_board_creates_knights(self, full_board):
        knights = [
            full_board.get_square((7, 1)).piece,
            full_board.get_square((7, 6)).piece,
            full_board.get_square((0, 1)).piece,
            full_board.get_square((0, 6)).piece,
        ]
        assert all(k.name == PieceNames.KNIGHT for k in knights)

    def test_populate_board_creates_bishops(self, full_board):
        bishops = [
            full_board.get_square((7, 2)).piece,
            full_board.get_square((7, 5)).piece,
            full_board.get_square((0, 2)).piece,
            full_board.get_square((0, 5)).piece,
        ]
        assert all(b.name == PieceNames.BISHOP for b in bishops)

    def test_populate_board_creates_pawns(self, full_board):
        white_pawns = [full_board.get_square((6, i)).piece for i in range(8)]
        black_pawns = [full_board.get_square((1, i)).piece for i in range(8)]
        assert all(p.name == PieceNames.PAWN for p in white_pawns)
        assert all(p.name == PieceNames.PAWN for p in black_pawns)


class TestBoardTurnManagement:
    def test_change_turn_white_to_black(self, full_board):
        assert full_board.turn_color == PieceColors.WHITE
        full_board.change_turn()
        assert full_board.turn_color == PieceColors.BLACK

    def test_change_turn_black_to_white(self, full_board):
        full_board.change_turn()
        assert full_board.turn_color == PieceColors.BLACK
        full_board.change_turn()
        assert full_board.turn_color == PieceColors.WHITE


class TestBoardMakeMove:
    def test_make_move_changes_piece_position(self, full_board):
        pawn = full_board.get_square((6, 4)).piece
        move = Move(pawn, (4, 4), full_board)
        full_board.make_move(move)
        assert pawn.pos == (4, 4)

    def test_make_move_captures_piece(self, empty_board):
        white_king = King((7, 3), PieceColors.WHITE, empty_board)
        black_king = King((0, 3), PieceColors.BLACK, empty_board)
        white_rook = Rook((7, 7), PieceColors.WHITE, empty_board)
        black_rook = Rook((7, 5), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_king, (7, 3))
        empty_board.place_piece(black_king, (0, 3))
        empty_board.place_piece(white_rook, (7, 7))
        empty_board.place_piece(black_rook, (7, 5))
        empty_board.white_king = white_king
        empty_board.black_king = black_king
        move = Move(white_rook, (7, 5), empty_board)
        empty_board.make_move(move)
        assert empty_board.get_square((7, 7)).empty()
        assert empty_board.get_square((7, 5)).piece == white_rook

    def test_make_move_updates_has_moved(self, empty_board):
        white_king = King((7, 3), PieceColors.WHITE, empty_board)
        black_king = King((0, 3), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_king, (7, 3))
        empty_board.place_piece(black_king, (0, 3))
        empty_board.white_king = white_king
        empty_board.black_king = black_king
        rook = Rook((7, 7), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (7, 7))
        assert rook.has_moved is False
        move = Move(rook, (7, 6), empty_board)
        empty_board.make_move(move)
        assert rook.has_moved is True


class TestBoardUnmakeMove:
    def test_unmake_move_restores_position(self, empty_board):
        white_king = King((7, 3), PieceColors.WHITE, empty_board)
        black_king = King((0, 3), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_king, (7, 3))
        empty_board.place_piece(black_king, (0, 3))
        empty_board.white_king = white_king
        empty_board.black_king = black_king
        rook = Rook((7, 7), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (7, 7))
        move = Move(rook, (7, 6), empty_board)
        empty_board.make_move(move)
        empty_board.unmake_move(move)
        assert rook.pos == (7, 7)

    def test_unmake_move_restores_captured_piece(self, empty_board):
        white_king = King((7, 3), PieceColors.WHITE, empty_board)
        black_king = King((0, 3), PieceColors.BLACK, empty_board)
        white_rook = Rook((7, 7), PieceColors.WHITE, empty_board)
        black_rook = Rook((7, 5), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_king, (7, 3))
        empty_board.place_piece(black_king, (0, 3))
        empty_board.place_piece(white_rook, (7, 7))
        empty_board.place_piece(black_rook, (7, 5))
        empty_board.white_king = white_king
        empty_board.black_king = black_king
        move = Move(white_rook, (7, 5), empty_board)
        empty_board.make_move(move)
        empty_board.unmake_move(move)
        assert empty_board.get_square((7, 5)).piece == black_rook

    def test_unmake_move_restores_has_moved(self, empty_board):
        white_king = King((7, 3), PieceColors.WHITE, empty_board)
        black_king = King((0, 3), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_king, (7, 3))
        empty_board.place_piece(black_king, (0, 3))
        empty_board.white_king = white_king
        empty_board.black_king = black_king
        rook = Rook((7, 7), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (7, 7))
        move = Move(rook, (7, 6), empty_board)
        empty_board.make_move(move)
        empty_board.unmake_move(move)
        assert rook.has_moved is False


class TestBoardReset:
    def test_reset_clears_checkmate(self, full_board):
        full_board.checkmate = True
        full_board.reset()
        assert full_board.checkmate is False

    def test_reset_clears_stalemate(self, full_board):
        full_board.stalemate = True
        full_board.reset()
        assert full_board.stalemate is False

    def test_reset_clears_game_end(self, full_board):
        full_board.game_end = True
        full_board.reset()
        assert full_board.game_end is False
