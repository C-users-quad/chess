from core.enums import PieceColors
from core.settings import COLORS, TYPE_CHECKING
from ui.rects.colored_rect import UIColoredRect

if TYPE_CHECKING:
    from chess.board import Board


class UITurnColorRect(UIColoredRect):
    def __init__(self, board: Board, **kwargs):
        super().__init__(color=board.turn_color, **kwargs)
        self.board = board

    def change_color(self):
        self.color = (
            COLORS["white-square"]
            if self.board.turn_color == PieceColors.WHITE
            else COLORS["black-square"]
        )

    def update(self):
        self.change_color()
