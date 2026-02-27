import pytest
import sys
from unittest.mock import MagicMock, patch

@pytest.fixture(autouse=True)
def mock_pygame():
    """Mock pygame modules to allow testing without display."""
    mock_pygame = MagicMock()
    mock_pygame.SRCALPHA = 32
    mock_pygame.QUIT = 1
    mock_pygame.VIDEORESIZE = 2
    mock_pygame.BLEND_RGBA_MULT = 2

    mock_surface = MagicMock()
    mock_surface.get_size.return_value = (800, 600)
    mock_surface.get_rect.return_value = MagicMock()
    mock_pygame.Surface = MagicMock(return_value=mock_surface)

    mock_rect = MagicMock()
    mock_rect.size = (100, 100)
    mock_rect.topleft = (0, 0)
    mock_rect.center = (50, 50)
    mock_rect.bottomright = (100, 100)
    mock_rect.collidepoint.return_value = False
    mock_rect.width = 100
    mock_rect.height = 100
    mock_pygame.Rect = MagicMock(return_value=mock_rect)

    mock_display = MagicMock()
    mock_display.get_size.return_value = (800, 600)
    mock_pygame.display = mock_display

    mock_mouse = MagicMock()
    mock_mouse.get_pos.return_value = (0, 0)
    mock_mouse.get_just_released.return_value = (False,)
    mock_pygame.mouse = mock_mouse

    mock_draw = MagicMock()
    mock_pygame.draw = mock_draw

    mock_transform = MagicMock()
    mock_pygame.transform = mock_transform

    sys.modules['pygame'] = mock_pygame

    return mock_pygame

@pytest.fixture
def mock_game():
    """Create a mock game object for testing."""
    game = MagicMock()
    game.display = MagicMock()
    game.display.get_size.return_value = (800, 600)
    game.window_resized.return_value = False
    game.debug = False
    game.dim_surf = MagicMock()
    game.dim_rect = MagicMock()
    game.state_stack = []
    game.push_state = MagicMock()
    game.power_off = MagicMock()

    return game

@pytest.fixture
def mock_game_context(mock_game):
    """Set up GameContext with mock game."""
    from core.settings import GameContext
    GameContext.game = mock_game
    yield mock_game
    GameContext.game = None
