from chess.ui.captured_pieces import UICapturedPieces
from chess.ui.clock import UIClock
from chess.ui.turn_color_rect import UITurnColorRect
from core.settings import (
    BASE_HEIGHT,
    BASE_WIDTH,
    BOARD_RESIZE_AXIS,
    VariableSettings,
    pygame,
)
from core.enums import AnchorPoints, PieceColors, ResizeAxis, StateNames
from chess.board import Board
from core.utils import get_ui_elem
from states.base import GameState
from ui.composites.manager import UIManager
from ui.composites.widget import UIWidget
from ui.misc.text import UIText
from ui.rects.colored_rect import UIColoredRect


def game_info_widget_child_factory(base: UIColoredRect, state: Chess):
    children = []
    base_size = base.base_size
    resize_axis = base.resize_axis
    padding = get_ui_elem("padding")

    turn_color_indicator = UITurnColorRect(
        pos=(padding, base_size[1] / 2),
        anchor=AnchorPoints.MIDLEFT,
        size=(base_size[1] - padding * 2, base_size[1] - padding * 2),
        resize_axis=resize_axis,
        board=state.board,
        rounding=True,
    )
    children.append(turn_color_indicator)

    indicator_text = UIText(
        font_height=turn_color_indicator.base_size[1],
        text="to move",
        text_color="black",
        max_width=base_size[0] / 5,
        pos=(
            turn_color_indicator.get_base_rect().right + padding,
            base.base_size[1] / 2,
        ),
        anchor=AnchorPoints.MIDLEFT,
        resize_axis=resize_axis,
    )
    children.append(indicator_text)

    captured_pieces = UICapturedPieces(
        pos=(indicator_text.get_base_rect().right + padding, base_size[1] / 2),
        anchor=AnchorPoints.MIDLEFT,
        side_length=base_size[0] / 25,
        resize_axis=resize_axis,
        board=state.board,
    )
    children.append(captured_pieces)

    clock = UIClock(
        pos=(captured_pieces.get_base_rect().right + padding, base_size[1] / 2),
        size=(
            base_size[0] - captured_pieces.get_base_rect().right - 2 * padding,
            base_size[1] - 2 * padding,
        ),
        anchor=AnchorPoints.MIDLEFT,
        resize_axis=resize_axis,
        font_size=ResizeAxis.AUTO,
    )
    children.append(clock)

    return children


class Chess(GameState):
    """game state with chess board"""

    name = StateNames.CHESS

    def __init__(self):
        self.board = Board()
        super().__init__()
        self.dim = False
        self.white_time = VariableSettings.player_time
        """the current amount of time white has remaining"""
        self.black_time = VariableSettings.player_time
        """the current amount of time black has remaining"""
        self.time_accumulator: float = 0
        """should accumulate dt across frames. used for player clocks."""

    def reset_game(self):
        self.board.reset()
        self.white_time = VariableSettings.player_time
        self.black_time = VariableSettings.player_time

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.board.reset_square_flags()
            self.game.push_state(StateNames.MAIN_MENU)

    def update_game_time(self):
        """
        updates the time each player has remaining based on
        whose turn it is and the passing of time while the chess state is active.
        """
        # accumulate dt across frames
        self.time_accumulator += self.game.dt

        # updates player's clocks every second
        if self.time_accumulator >= 1:
            match self.board.turn_color:
                case PieceColors.WHITE:
                    self.white_time -= 1
                case PieceColors.BLACK:
                    self.black_time -= 1
            self.time_accumulator = 0

    def handle_loss_on_time(self):
        """
        detects and handles players running out of time.
        """
        if self.black_time <= 0 or self.white_time <= 0:
            self.board.timeout = True

    def update(self):
        self.ui.update()
        self.update_game_time()
        self.handle_loss_on_time()

    def render(self, force_rendering=False):
        self.ui.render(force_rendering)

    def draw(self):
        self.ui.draw()

    def make_ui(self):
        elements = []
        spacing = get_ui_elem("spacing")
        board_width = get_ui_elem("board") - 2 * spacing
        center = (BASE_WIDTH / 2, BASE_HEIGHT / 2)

        game_info_widget_base = UIColoredRect(
            pos=(center[0], center[1] + board_width / 2 + spacing),
            anchor=AnchorPoints.MIDTOP,
            size=(
                board_width,
                BASE_HEIGHT - center[1] - board_width / 2 - 2 * spacing,
            ),
            resize_axis=BOARD_RESIZE_AXIS,
            color="white",
            rounding=True,
            draw_below=False,
        )
        game_info_widget = UIWidget(
            base=game_info_widget_base,
            child_factory=lambda: game_info_widget_child_factory(
                game_info_widget_base, self
            ),
        )
        elements.append(game_info_widget)
        elements.append(self.board)

        self.ui.elements = elements
