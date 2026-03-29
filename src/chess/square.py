from core.settings import TYPE_CHECKING
from core.utils import get_tui_text_box

if TYPE_CHECKING:
    from chess.board import Board


class BoardSquare:
    """
    contains a piece at a position in board.
    """

    def __init__(self, pos: tuple[int, int], board: Board):
        self.piece = None
        self.pos = pos
        self.board = board

    def place(self, piece):
        self.piece = piece

    def remove_piece(self):
        self.piece = None

    def is_empty(self):
        return self.piece is None

    def __str__(self):
        lines = (
            f"BoardSquare {hex(id(self))}\nPos: {self.pos}\nPiece: {type(self.piece)}"
        )

        return get_tui_text_box(lines)
