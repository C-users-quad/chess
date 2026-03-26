from core.utils import clamp, opposite_color, get_all_pieces_of_color
from core.enums import PieceColors


class TestClamp:
    def test_clamp_returns_value_when_in_range(self):
        assert clamp(5, 0, 10) == 5

    def test_clamp_returns_min_when_value_below(self):
        assert clamp(-5, 0, 10) == 0

    def test_clamp_returns_max_when_value_above(self):
        assert clamp(15, 0, 10) == 10

    def test_clamp_returns_min_when_equal_to_min(self):
        assert clamp(0, 0, 10) == 0

    def test_clamp_returns_max_when_equal_to_max(self):
        assert clamp(10, 0, 10) == 10

    def test_clamp_with_float_values(self):
        assert clamp(5.5, 0, 10) == 5.5

    def test_clamp_negative_range(self):
        assert clamp(0, -10, -5) == -5


class TestOppositeColor:
    def test_opposite_color_white_returns_black(self):
        assert opposite_color(PieceColors.WHITE) == PieceColors.BLACK

    def test_opposite_color_black_returns_white(self):
        assert opposite_color(PieceColors.BLACK) == PieceColors.WHITE


class TestGetAllPiecesOfColor:
    def test_get_all_pieces_of_color_returns_empty_when_no_pieces(self, empty_board):
        pieces = get_all_pieces_of_color(PieceColors.WHITE, empty_board)
        assert pieces == []

    def test_get_all_pieces_of_color_returns_white_pieces(self, full_board):
        pieces = get_all_pieces_of_color(PieceColors.WHITE, full_board)
        assert len(pieces) == 16
        for piece in pieces:
            assert piece.color == PieceColors.WHITE

    def test_get_all_pieces_of_color_returns_black_pieces(self, full_board):
        pieces = get_all_pieces_of_color(PieceColors.BLACK, full_board)
        assert len(pieces) == 16
        for piece in pieces:
            assert piece.color == PieceColors.BLACK

    def test_get_all_pieces_of_color_count(self, full_board):
        white_pieces = get_all_pieces_of_color(PieceColors.WHITE, full_board)
        black_pieces = get_all_pieces_of_color(PieceColors.BLACK, full_board)
        assert len(white_pieces) == 16
        assert len(black_pieces) == 16
