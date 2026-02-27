"""Tests for UI framework components."""
import pytest
from unittest.mock import MagicMock, patch

class TestUIElement:
    """Tests for UIElement base class."""

    def test_uielement_initialization(self, mock_game_context):
        """Test UIElement can be initialized with pos and size."""
        from ui.base import UIElement

        element = UIElement(pos=(10, 20), size=(100, 50))

        assert element.base_pos == (10, 20)
        assert element.base_size == (100, 50)
        assert element.anchor == "topleft"
        assert element.resize_axis == "auto"

    def test_uielement_resize(self, mock_game_context):
        """Test UIElement resize method."""
        from ui.base import UIElement

        element = UIElement(pos=(10, 20), size=(100, 50))
        element.resize()

        assert element.image is not None

    def test_uielement_update_is_noop(self, mock_game_context):
        """Test UIElement update method is a noop."""
        from ui.base import UIElement

        element = UIElement(pos=(10, 20), size=(100, 50))
        element.update()

    def test_uielement_render_is_noop(self, mock_game_context):
        """Test UIElement render method is a noop."""
        from ui.base import UIElement

        element = UIElement(pos=(10, 20), size=(100, 50))
        element.render()


class TestUIManager:
    """Tests for UIManager class."""

    def test_uimanager_initialization(self, mock_game_context):
        """Test UIManager can be initialized with elements list."""
        from ui.manager import UIManager
        from ui.base import UIElement

        elements = [UIElement(), UIElement()]
        manager = UIManager(elements)

        assert len(manager.elements) == 2

    def test_uimanager_update_calls_element_updates(self, mock_game_context):
        """Test UIManager update propagates to elements."""
        from ui.manager import UIManager
        from ui.base import UIElement

        mock_element = MagicMock(spec=UIElement)
        manager = UIManager([mock_element])

        manager.update()

        mock_element.update.assert_called_once()

    def test_uimanager_draw_calls_element_draws(self, mock_game_context):
        """Test UIManager draw propagates to elements."""
        from ui.manager import UIManager
        from ui.base import UIElement

        mock_element = MagicMock(spec=UIElement)
        manager = UIManager([mock_element])

        manager.draw()

        mock_element.draw.assert_called_once()


class TestUIWidget:
    """Tests for UIWidget class."""

    def test_uiwidget_initialization(self, mock_game_context):
        """Test UIWidget can be initialized with base and child_factory."""
        from ui.widget import UIWidget
        from ui.rects.colored_rect import UIColoredRect

        base = UIColoredRect(
            pos=(0, 0),
            size=(100, 100),
            anchor="topleft",
            color="#FFFFFF"
        )

        def child_factory():
            return []

        widget = UIWidget(base=base, child_factory=child_factory)

        assert widget.base is not None
        assert widget.children is not None


class TestUIColoredRect:
    """Tests for UIColoredRect class."""

    def test_uicoloredrect_initialization(self, mock_game_context):
        """Test UIColoredRect can be initialized with color."""
        from ui.rects.colored_rect import UIColoredRect

        rect = UIColoredRect(
            pos=(0, 0),
            size=(100, 50),
            anchor="topleft",
            color="#FF0000"
        )

        assert rect.color == "#FF0000"
        assert rect.rounding == False

    def test_uicoloredrect_with_rounding(self, mock_game_context):
        """Test UIColoredRect with rounding parameter."""
        from ui.rects.colored_rect import UIColoredRect

        rect = UIColoredRect(
            pos=(0, 0),
            size=(100, 50),
            anchor="topleft",
            color="#FF0000",
            rounding=True
        )

        assert rect.rounding == True


class TestUIButton:
    """Tests for UIButton class."""

    def test_uibutton_initialization(self, mock_game_context):
        """Test UIButton can be initialized with click action."""
        from ui.buttons.base import UIButton

        def dummy_action():
            pass

        button = UIButton(
            pos=(0, 0),
            size=(100, 50),
            anchor="topleft",
            click_action=dummy_action
        )

        assert button.click_action is dummy_action
        assert button.click_action_args is None

    def test_uibutton_with_args(self, mock_game_context):
        """Test UIButton with click action arguments."""
        from ui.buttons.base import UIButton

        def dummy_action(x, y):
            pass

        button = UIButton(
            pos=(0, 0),
            size=(100, 50),
            anchor="topleft",
            click_action=dummy_action,
            click_action_args=(1, 2)
        )

        assert button.click_action_args == (1, 2)

    def test_uibutton_render_creates_highlight_none(self, mock_game_context):
        """Test UIButton render sets highlight to None initially."""
        from ui.buttons.base import UIButton

        def dummy_action():
            pass

        button = UIButton(
            pos=(0, 0),
            size=(100, 50),
            anchor="topleft",
            click_action=dummy_action
        )

        button.render()

        assert button.highlight is None
