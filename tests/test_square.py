from chess.square import BoardSquare
from chess.pieces import Rook
from core.enums import PieceColors


class TestBoardSquare:
    def test_square_stores_position(self):
        board = type("MockBoard", (), {"image": None, "rect": None})()
        square = BoardSquare((3, 5), "white-square", board)
        assert square.pos == (3, 5)

    def test_square_is_empty_initially(self):
        board = type("MockBoard", (), {"image": None, "rect": None})()
        square = BoardSquare((0, 0), "white-square", board)
        assert square.is_empty() is True

    def test_square_place_piece(self):
        board = type("MockBoard", (), {"image": None, "rect": None})()
        square = BoardSquare((0, 0), "white-square", board)
        rook = Rook((0, 0), PieceColors.WHITE, board)
        square.place(rook)
        assert square.is_empty() is False
        assert square.piece == rook

    def test_square_remove_piece(self):
        board = type("MockBoard", (), {"image": None, "rect": None})()
        square = BoardSquare((0, 0), "white-square", board)
        rook = Rook((0, 0), PieceColors.WHITE, board)
        square.place(rook)
        square.remove_piece()
        assert square.is_empty() is True
        assert square.piece is None

    def test_square_selected_flag(self):
        board = type("MockBoard", (), {"image": None, "rect": None})()
        square = BoardSquare((0, 0), "white-square", board)
        assert square.selected is False
        square.selected = True
        assert square.selected is True

    def test_square_valid_square_flag(self):
        board = type("MockBoard", (), {"image": None, "rect": None})()
        square = BoardSquare((0, 0), "white-square", board)
        assert square.valid_square is False
        square.valid_square = True
        assert square.valid_square is True

    def test_square_game_end_flags_initially_false(self):
        board = type("MockBoard", (), {"image": None, "rect": None})()
        square = BoardSquare((0, 0), "white-square", board)
        assert square.winning_square is False
        assert square.losing_square is False
        assert square.stalemate_square is False
