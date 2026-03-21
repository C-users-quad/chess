from chess.ui.turn_color_rect import UITurnColorRect
from core.settings import BASE_HEIGHT, BASE_WIDTH, BOARD_RESIZE_AXIS, pygame
from core.enums import AnchorPoints, ResizeAxis, StateNames
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
        size=(
            base_size[1] - padding * 2,
            base_size[1] - padding * 2
        ),
        resize_axis=resize_axis,
        board=state.board,
        rounding=True,
    )
    print(turn_color_indicator.base_pos)
    children.append(turn_color_indicator)

    indicator_text = UIText(
        font_height = turn_color_indicator.base_size[1],
        text="to move",
        text_color="black",
        max_width=base_size[0] / 5,
        pos=(
            turn_color_indicator.get_base_rect().right + padding,
            turn_color_indicator.get_base_rect().centery
        ),
        anchor=AnchorPoints.MIDLEFT,
        resize_axis=resize_axis,
    )
    children.append(indicator_text)

    return children


class Chess(GameState):
    """game state with chess board"""

    name = StateNames.CHESS

    def __init__(self):
        self.board = Board()
        super().__init__()
        self.dim = False

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.board.reset_square_flags()
            self.game.push_state(StateNames.MAIN_MENU)

    def update(self):
        self.ui.update()

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

        self.ui = UIManager(elements, self)
