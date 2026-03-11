from core.settings import BASE_HEIGHT, BASE_WIDTH, pygame
from core.enums import StateNames
from core.utils import get_ui_elem
from states.base import GameState
from ui.buttons.text_button import UITextButton
from ui.rects.colored_rect import UIColoredRect
from ui.composites.widget import UIWidget
from ui.composites.manager import UIManager
from chess.board import Board
from ui.text import UIText


def new_game_widget_child_factory(base, state: NewGame):
    children = []
    padding = get_ui_elem("padding")

    # new game button
    new_game_button = UITextButton(
        pos=(base.base_size[0] / 2, base.base_size[1] - padding),
        anchor="midbottom",
        text="New Game",
        font_size="text",
        click_action=state.reset_board,
        size=(base.base_size[0] - padding * 2, base.base_size[1] / 5),
        resize_axis=base.resize_axis,
    )
    children.append(new_game_button)

    # game results info
    game_results_text_base = UIColoredRect(
        pos=(base.base_size[0] / 2, padding),
        size=(base.base_size[0] - padding * 2, base.base_size[1] / 4),
        anchor="midtop",
        color="#57585e",
        resize_axis=base.resize_axis,
        rounding=True,
    )
    children.append(game_results_text_base)
    if state.chess_state.board.winning_color:
        game_result = f"{state.chess_state.board.winning_color.value} wins!!"
    else:
        game_result = "draw!"

    game_results_text = UIText(
        pos=(game_results_text_base.get_base_rect().center),
        font_height=game_results_text_base.base_size[1] - padding * 2,
        anchor="center",
        resize_axis=base.resize_axis,
        text=game_result,
        text_color="white",
        max_width=game_results_text_base.base_size[0] - padding * 2,
    )
    children.append(game_results_text)

    return children


class NewGame(GameState):
    name = StateNames.NEW_GAME

    def __init__(self):
        # the chess state is always at the bottom
        self.chess_state = self.game.state_stack[0]
        super().__init__()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        match key:
            case pygame.K_ESCAPE:
                self.reset_board()

    def reset_board(self):
        self.chess_state.board = Board()
        self.game.pop_state()

    def update(self):
        self.ui.update()

    def render(self, force_rendering=False):
        self.ui.render(force_rendering)

    def draw(self):
        self.ui.draw()

    def make_ui(self):
        elements = []
        resize_axis = "height"

        # make new game widget
        new_game_widget_base = UIColoredRect(
            pos=(BASE_WIDTH / 2, BASE_HEIGHT / 2),
            size=(BASE_WIDTH / 5, BASE_HEIGHT / 3),
            anchor="center",
            rounding=True,
            color="white",
            resize_axis=resize_axis,
        )

        new_game_widget = UIWidget(
            base=new_game_widget_base,
            child_factory=lambda: new_game_widget_child_factory(
                new_game_widget_base, self
            ),
        )
        elements.append(new_game_widget)

        self.ui = UIManager(elements)
