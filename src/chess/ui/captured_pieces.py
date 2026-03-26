from core.enums import PieceColors, StateNames
from core.images import PIECE_IMAGES
from core.settings import COLORS, GameContext, TYPE_CHECKING, pygame
from core.utils import get_ui_elem, scale
from ui.base import UIElement

if TYPE_CHECKING:
    from chess.pieces import Piece
    from chess.board import Board


class UICapturedPieces(UIElement):
    def __init__(self, side_length, board: Board, **kwargs):
        """
        ui element that displays the current pieces captured by both black and white
        Args:
            side_length (float | int) :
                the side length in base-space of each individual captured piece's
                image
        """
        padding = get_ui_elem("padding")
        self.side_length = side_length
        size = (
            15 * side_length / 1.5,  # 15 = max captureable pieces
            2 * side_length + padding,
        )
        super().__init__(size=size, **kwargs)
        self.prev_captured_pieces = board.captured_pieces

    @property
    def captured_pieces(self) -> list[Piece]:
        """the current list of captured pieces"""
        return self.game.get_state(StateNames.CHESS).board.captured_pieces

    @property
    def image_side_length(self):
        """the screen-space image side length"""
        return scale(self.side_length, self.resize_axis)

    def check_capture(self):
        """if a piece has been captured, make sprite dirty for re-rendering"""
        if self.prev_captured_pieces != self.captured_pieces:
            self.dirty = True

    def update(self):
        self.check_capture()
        self.prev_captured_pieces = self.captured_pieces

    def render(self):
        self.resize()
        self.image.fill(COLORS["clear"])
        padding = scale(get_ui_elem("padding"), axis=self.resize_axis)

        # create lists of captured pieces
        white_captured = [
            piece for piece in self.captured_pieces if piece.color == PieceColors.WHITE
        ]
        white_captured.sort(key=lambda x: x.value, reverse=True)
        black_captured = [
            piece for piece in self.captured_pieces if piece.color == PieceColors.BLACK
        ]
        black_captured.sort(key=lambda x: x.value, reverse=True)

        # draw captured pieces
        for i, piece in enumerate(white_captured):
            piece_image = PIECE_IMAGES.get((piece.color, piece.name))
            piece_image = pygame.transform.smoothscale(
                surface=piece_image,
                size=(self.image_side_length, self.image_side_length),
            )
            self.image.blit(source=piece_image, dest=(i * (self.image.width / 15), 0))

        for i, piece in enumerate(black_captured):
            piece_image = PIECE_IMAGES.get((piece.color, piece.name))
            piece_image = pygame.transform.smoothscale(
                surface=piece_image,
                size=(self.image_side_length, self.image_side_length),
            )
            self.image.blit(
                source=piece_image,
                dest=(i * (self.image.width / 15), self.image_side_length + padding),
            )

        # draw partition between 2 rows of captured pieces
        pygame.draw.line(
            surface=self.image,
            color="gray",
            start_pos=(0, self.image.get_height() / 2),
            end_pos=(self.image.get_width(), self.image.get_height() / 2),
            width=self.image.get_height() // 15,
        )
