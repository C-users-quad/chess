import sys
from unittest.mock import MagicMock, patch
import pytest

sys.path.insert(0, "src")


@pytest.fixture(autouse=True)
def mock_pygame():
    with patch.dict("sys.modules", {"pygame": MagicMock(), "pygame.ce": MagicMock()}):
        yield


@pytest.fixture(autouse=True)
def mock_game_context():
    mock_game = MagicMock()
    mock_game.display.get_size.return_value = (800, 800)
    mock_game.debug = False

    with patch("core.settings.GameContext") as mock_context:
        mock_context.game = mock_game
        yield mock_game


@pytest.fixture
def empty_board():
    from chess.board import Board

    with patch.object(Board, "populate_board"):
        board = Board()
        for row in board.squares:
            for square in row:
                square.piece = None
        return board


@pytest.fixture
def full_board():
    from chess.board import Board

    board = Board()
    return board
