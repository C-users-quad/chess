from core.settings import BASE_HEIGHT, BASE_WIDTH, COLORS, pygame
from core.utils import get_ui_elem
from core.images import PIECE_IMAGES
from core.enums import AnchorPoints, PieceNames, ResizeAxis, StateNames
from ui.rects.colored_rect import UIColoredRect
from ui.buttons.image_button import UIImageButton
from ui.composites.widget import UIWidget
from states.base import GameState
from ui.composites.manager import UIManager


def promotion_widget_child_factory(base, move, state):
    children = []
    padding = get_ui_elem("padding")
    base_center = (base.base_size[0] / 2, base.base_size[1] / 2)

    option_btn_side_len = base.base_size[0] / 2 - (3 / 2) * padding
    option_btn_size = (option_btn_side_len, option_btn_side_len)
    buttons = {
        PieceNames.QUEEN: [
            (base_center[0] - padding / 2, base_center[1] - padding / 2),
            "bottomright",
        ],
        PieceNames.ROOK: [
            (base_center[0] + padding / 2, base_center[1] - padding / 2),
            "bottomleft",
        ],
        PieceNames.BISHOP: [
            (base_center[0] - padding / 2, base_center[1] + padding / 2),
            AnchorPoints.TOPRIGHT,
        ],
        PieceNames.KNIGHT: [
            (base_center[0] + padding / 2, base_center[1] + padding / 2),
            AnchorPoints.TOPLEFT,
        ],
    }
    for name, (pos, anchor) in buttons.items():
        btn_bg = UIColoredRect(
            pos=pos,
            size=option_btn_size,
            anchor=anchor,
            color=COLORS["promotion-ui-btn"],
            resize_axis=base.resize_axis,
            rounding=True,
        )
        button = UIImageButton(
            pos=pos,
            anchor=anchor,
            click_action=state.promote,
            click_action_args=(name,),
            image=PIECE_IMAGES[(move.piece.color, name)],
            size=option_btn_size,
            resize_axis=base.resize_axis,
        )
        children.append(btn_bg)
        children.append(button)

    return children


class Promotion(GameState):
    """menu for pawn promotion"""

    names = StateNames.PROMOTION

    def __init__(self, move):
        self.move = move
        self.default_promotion = PieceNames.QUEEN
        """the piece you default to during promotion"""
        super().__init__()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.promote(self.default_promotion)

    def promote(self, piece_name):
        self.move.set_promotion_piece(piece_name)
        self.game.pop_state()

    def update(self):
        self.ui.update()

    def render(self, force_rendering=False):
        self.ui.render(force_rendering)

    def draw(self):
        self.ui.draw()

    def make_ui(self):
        # get needed info
        elements = []
        resize_axis = ResizeAxis.MAX

        # create bounding box for the promotion ui
        base_side_length = BASE_HEIGHT / 5
        base_center = (BASE_WIDTH / 2, BASE_HEIGHT / 2)
        promotion_ui_base = UIColoredRect(
            pos=base_center,
            size=(base_side_length, base_side_length),
            anchor=AnchorPoints.CENTER,
            color=COLORS["promotion-ui-bg"],
            resize_axis=resize_axis,
            rounding=True,
        )

        promotion_ui = UIWidget(
            base=promotion_ui_base,
            child_factory=lambda: promotion_widget_child_factory(
                promotion_ui_base, self.move, self
            ),
        )
        elements.append(promotion_ui)

        self.ui.elements = elements
