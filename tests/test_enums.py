from core.enums import (
    PieceColors,
    PieceNames,
    StateNames,
    SoundNames,
    AnchorPoints,
    ResizeAxis,
)


class TestPieceColors:
    def test_piece_colors_has_white(self):
        assert PieceColors.WHITE == "white"

    def test_piece_colors_has_black(self):
        assert PieceColors.BLACK == "black"

    def test_piece_colors_count(self):
        assert len(PieceColors) == 2


class TestPieceNames:
    def test_piece_names_has_king(self):
        assert PieceNames.KING == "king"

    def test_piece_names_has_queen(self):
        assert PieceNames.QUEEN == "queen"

    def test_piece_names_has_rook(self):
        assert PieceNames.ROOK == "rook"

    def test_piece_names_has_bishop(self):
        assert PieceNames.BISHOP == "bishop"

    def test_piece_names_has_knight(self):
        assert PieceNames.KNIGHT == "knight"

    def test_piece_names_has_pawn(self):
        assert PieceNames.PAWN == "pawn"

    def test_piece_names_count(self):
        assert len(PieceNames) == 6


class TestStateNames:
    def test_state_names_has_base(self):
        assert StateNames.BASE == "GameState"

    def test_state_names_has_chess(self):
        assert StateNames.CHESS == "Chess"

    def test_state_names_has_main_menu(self):
        assert StateNames.MAIN_MENU == "Main Menu"


class TestSoundNames:
    def test_sound_names_has_capture(self):
        assert SoundNames.CAPTURE == "capture"

    def test_sound_names_has_castle(self):
        assert SoundNames.CASTLE == "castle"

    def test_sound_names_has_check(self):
        assert SoundNames.CHECK == "check"


class TestAnchorPoints:
    def test_anchor_points_has_center(self):
        assert AnchorPoints.CENTER == "center"

    def test_anchor_points_has_topleft(self):
        assert AnchorPoints.TOPLEFT == "topleft"


class TestResizeAxis:
    def test_resize_axis_has_auto(self):
        assert ResizeAxis.AUTO == "auto"

    def test_resize_axis_has_min(self):
        assert ResizeAxis.MIN == "min"
