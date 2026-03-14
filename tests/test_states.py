"""Tests for state machine components."""
import pytest
from unittest.mock import MagicMock, patch

class TestGameState:
    """Tests for GameState base class."""

    def test_gamestate_initialization(self, mock_game_context):
        """Test GameState initializes with default attributes."""
        from states.base import GameState

        state = GameState()

        assert state.draw_below == True
        assert state.ui is None
        assert state.dim == True

    def test_gamestate_has_name_property(self, mock_game_context):
        """Test GameState has name attribute."""
        from states.base import GameState

        state = GameState()

        assert state.name is None

    def test_gamestate_game_property_returns_game(self, mock_game_context, mock_game):
        """Test GameState.game property returns the game object."""
        from states.base import GameState

        state = GameState()

        assert state.game is mock_game

    def test_gamestate_make_ui_is_noop(self, mock_game_context):
        """Test GameState.make_ui is a noop by default."""
        from states.base import GameState

        state = GameState()
        result = state.make_ui()

        assert result is None

    def test_gamestate_handle_input_is_noop(self, mock_game_context):
        """Test GameState.handle_input is a noop by default."""
        from states.base import GameState

        state = GameState()
        state.handle_input()

    def test_gamestate_draw_dim_with_dim_enabled(self, mock_game_context):
        """Test GameState.draw_dim draws dim surface when dim is True."""
        from states.base import GameState

        state = GameState()
        state.dim = True

        state.draw_dim()

        mock_game_context.display.blit.assert_called()

    def test_gamestate_draw_dim_with_dim_disabled(self, mock_game_context):
        """Test GameState.draw_dim does nothing when dim is False."""
        from states.base import GameState

        state = GameState()
        state.dim = False

        state.draw_dim()

        mock_game_context.display.blit.assert_not_called()


class TestGameStateHandleEvents:
    """Tests for GameState.handle_events method."""

    def test_handle_quit_event(self, mock_game_context):
        """Test GameState handles pygame.QUIT event."""
        from states.base import GameState

        mock_event = MagicMock()
        mock_event.type = 1  # pygame.QUIT

        state = GameState()
        state.handle_events([mock_event])

        mock_game_context.power_off.assert_called_once()

    def test_handle_videoresize_event(self, mock_game_context):
        """Test GameState handles pygame.VIDEORESIZE event."""
        from states.base import GameState

        mock_event = MagicMock()
        mock_event.type = 2  # pygame.VIDEORESIZE

        state = GameState()
        state.handle_events([mock_event])

        mock_game_context.render_dim.assert_called_once()


class TestStateNames:
    """Tests for StateNames enum."""

    def test_state_names_has_base(self, mock_game_context):
        """Test StateNames has BASE state."""
        from core.enums import StateNames

        assert StateNames.BASE is not None

    def test_state_names_has_chess(self, mock_game_context):
        """Test StateNames has CHESS state."""
        from core.enums import StateNames

        assert StateNames.CHESS is not None

    def test_state_names_has_main_menu(self, mock_game_context):
        """Test StateNames has MAIN_MENU state."""
        from core.enums import StateNames

        assert StateNames.MAIN_MENU is not None

    def test_state_names_has_promotion(self, mock_game_context):
        """Test StateNames has PROMOTION state."""
        from core.enums import StateNames

        assert StateNames.PROMOTION is not None

    def test_state_names_has_settings(self, mock_game_context):
        """Test StateNames has SETTINGS state."""
        from core.enums import StateNames

        assert StateNames.SETTINGS is not None


class TestPieceColors:
    """Tests for PieceColors enum."""

    def test_piece_colors_has_white(self, mock_game_context):
        """Test PieceColors has WHITE."""
        from core.enums import PieceColors

        assert PieceColors.WHITE is not None

    def test_piece_colors_has_black(self, mock_game_context):
        """Test PieceColors has BLACK."""
        from core.enums import PieceColors

        assert PieceColors.BLACK is not None

    def test_piece_colors_white_value(self, mock_game_context):
        """Test PieceColors.WHITE has correct value."""
        from core.enums import PieceColors

        assert PieceColors.WHITE == "white"

    def test_piece_colors_black_value(self, mock_game_context):
        """Test PieceColors.BLACK has correct value."""
        from core.enums import PieceColors

        assert PieceColors.BLACK == "black"


class TestPieceNames:
    """Tests for PieceNames enum."""

    def test_piece_names_has_all_pieces(self, mock_game_context):
        """Test PieceNames has all piece types."""
        from core.enums import PieceNames

        assert PieceNames.KING is not None
        assert PieceNames.QUEEN is not None
        assert PieceNames.ROOK is not None
        assert PieceNames.BISHOP is not None
        assert PieceNames.KNIGHT is not None
        assert PieceNames.PAWN is not None
