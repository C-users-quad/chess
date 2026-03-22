from core.settings import (
    BOARD_RATIOS,
    BOARD_SQUARE_RATIOS,
    COLORS,
    GameContext,
    Literal,
    MIN_UI_SIZE,
    VariableSettings,
    pygame,
    TYPE_CHECKING,
    print,
)
from core.enums import PieceColors
from ui.buttons.clickable import Clickable
from core.utils import get_tui_text_box
from chess.move import Move

if TYPE_CHECKING:
    from chess.board import Board


class BoardSquare(Clickable):
    """
    used as the main chess-playing ui. when clicked, shows all possible moves.
    makes a board square which has a position corresponding to its indices in
    the board 2d array.

    the board square sprite contained here should be drawn
    on to the board sprite and positioned relative to it
    """

    def __init__(
        self,
        pos: tuple[int, int],
        color: Literal["white-square", "black-square"],
        board,
        **kwargs,
    ):
        # get square size
        super().__init__(**kwargs)
        # logical attributes and flags of board square
        self.piece = None
        self.color = COLORS[color]
        self.pos = pos
        self.board: Board = board
        self.selected = False
        self.valid_square = False

        # used to determine color of square highlights at game's end
        self.winning_square = False
        self.losing_square = False
        self.stalemate_square = False

    def render(self):
        # square size
        board_width = self.board.image.get_width()

        board_border_width = board_width * BOARD_RATIOS["border"]

        square_side_length = max(
            MIN_UI_SIZE, (board_width - 2 * board_border_width) // 8
        )

        board_center = (board_width / 2, board_width / 2)
        self.size = (square_side_length, square_side_length)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)

        # color square
        self.image.fill(self.color)

        # highlights
        self.draw_highlight()
        self.draw_move_circle()

        # draw piece centered
        if not self.empty():
            piece = pygame.transform.smoothscale(
                self.piece.image,
                (
                    int(square_side_length * BOARD_SQUARE_RATIOS["piece"]),
                    int(square_side_length * BOARD_SQUARE_RATIOS["piece"]),
                ),
            )
            piece_rect = piece.get_rect(
                center=(square_side_length // 2, square_side_length // 2)
            )
            self.image.blit(piece, piece_rect)

        # compute the drawing rect **centered inside board image**
        board_row, board_col = self.pos

        # flip board if flip board condition is true
        if VariableSettings.flip_board:
            if self.board.turn_color == PieceColors.BLACK:
                board_row = 7 - board_row
                board_col = 7 - board_col
        drawing_x = board_center[0] + (board_col - 4) * square_side_length
        drawing_y = board_center[1] + (board_row - 4) * square_side_length
        self.drawing_rect = pygame.Rect(
            drawing_x, drawing_y, square_side_length, square_side_length
        )

        # compute screen rect relative to board's position
        board_topleft = self.board.rect.topleft
        self.rect = self.drawing_rect.move(board_topleft)

    def draw_highlight(self):
        # dont draw if it isnt selected or it isnt the end of the game
        if not self.selected and not (
            self.stalemate_square or self.winning_square or self.losing_square
        ):
            return

        # determine color to highlight the square
        highlight_color = None
        if self.stalemate_square:
            highlight_color = COLORS["stalemate-sqr-highlight"]
        elif self.winning_square:
            highlight_color = COLORS["winning-sqr-highlight"]
        elif self.losing_square:
            highlight_color = COLORS["losing-sqr-highlight"]
        else:
            highlight_color = COLORS["board-highlight"]

        # create highlight and draw it onto the square image
        image_side_length = self.image.get_width()
        image_center = (image_side_length / 2, image_side_length / 2)
        highlight = pygame.Surface(self.image.size, pygame.SRCALPHA)
        highlight.fill(highlight_color)
        highlight_rect = highlight.get_rect(center=image_center)
        self.image.blit(highlight, highlight_rect)

    def draw_move_circle(self):
        # dont draw if this isnt a valid moving square
        if not self.valid_square:
            return

        # get image center pos
        image_side_length = self.image.get_width()
        image_center = (image_side_length / 2, image_side_length / 2)

        # create circle
        circle_color = (
            COLORS["move-circle-dark"]
            if self.color == COLORS["white-square"]
            else COLORS["move-circle-light"]
        )
        circle_radius = self.image.get_width() * BOARD_SQUARE_RATIOS["move-circle"]
        circle = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            circle, circle_color, (circle_radius, circle_radius), circle_radius
        )
        circle_rect = circle.get_rect(center=image_center)

        # draw circle onto image
        self.image.blit(circle, circle_rect)

    def on_click(self):
        """resolves square being clicked"""
        if self.board.clicked_outside():
            if self.selected:
                self.board.reset_square_flags()

        if not self.detect_release():
            return

        if GameContext.game.debug:
            print(self.piece)

        self.board.dirty = True
        selected_square = self.board.find_selected_square()
        if selected_square:
            if self.valid_square:
                # case: make a move
                self.board.make_move(Move(selected_square.piece, self.pos, self.board))
            else:
                # case: select another piece
                self.board.reset_square_flags(real_move=True)
                self.selected = True
                if not self.empty():
                    if self.piece.color != self.board.turn_color:
                        return
                    self.board.show_valid_moves(self)

        # case: select a piece
        self.selected = True
        if not self.empty():
            if self.piece.color != self.board.turn_color:
                return
            self.board.show_valid_moves(self)

    def update(self):
        self.detect_hovering()
        self.on_click()

    def draw(self):
        self.board.image.blit(self.image, self.drawing_rect)

    def place(self, piece):
        self.piece = piece

    def remove_piece(self):
        self.piece = None

    def empty(self):
        return self.piece is None

    def __str__(self):
        lines = (
            f"BoardSquare {hex(id(self))}\n"
            f"Selected: {self.selected}\n"
            f"Valid Square: {self.valid_square}\n"
            f"Pos: {self.pos}\n"
            f"Piece: {type(self.piece)}\n"
            f"Color: {self.color}\n"
            f"Hover: {self.hover}\n"
            f"Center: {self.drawing_rect.center}"
        )

        return get_tui_text_box(lines)
