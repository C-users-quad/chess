from core.settings import *
from ui.clickable import Clickable
from core.utils import get_tui_text_box, get_ui_elem, playsound, scale
from chess.move import Move

class BoardSquare(Clickable):
    """
    used as the main chess-playing ui. when clicked, shows all possible moves.
    makes a board square which has a position corresponding to its indices in
    the board 2d array.

    the board square sprite contained here should be drawn
    on to the board sprite and positioned relative to it
    """
    def __init__(self, pos: tuple[int, int],
            color: Literal['white-square', 'black-square'], board, **kwargs):
        # get square size
        super().__init__(**kwargs)
        self.piece = None
        self.color = COLORS[color]
        self.pos = pos
        self.board = board
        self.selected = False
        self.valid_square = False

    def render(self):
        # square size
        board_width = scale(get_ui_elem('board'), axis=BOARD_SCALE_AXIS)
        board_border_width = scale(
            get_ui_elem('board-border'), axis=BOARD_SCALE_AXIS)
        square_side_length = (board_width - 2*board_border_width) // 8
        board_center = (board_width / 2, board_width / 2)
        self.size = (square_side_length, square_side_length)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)

        # color square
        self.image.fill(self.color)

        # draw piece centered
        if not self.empty():
            piece = pygame.transform.smoothscale(
                self.piece.image,
                (int(square_side_length*PIECE_SCALE),
                 int(square_side_length*PIECE_SCALE))
            )
            piece_rect = piece.get_rect(center=(square_side_length//2, square_side_length//2))
            self.image.blit(piece, piece_rect)

        # compute the drawing rect **centered inside board image**
        board_row, board_col = self.pos
        if self.board.turn_color == 'black':
            board_row = 7 - board_row
            board_col = 7 - board_col
        drawing_x = board_center[0] + (board_col - 4) * square_side_length
        drawing_y = board_center[1] + (board_row - 4) * square_side_length
        self.drawing_rect = pygame.Rect(
            drawing_x, drawing_y,
            square_side_length, square_side_length
        )

        # compute screen rect relative to board's position
        board_topleft = self.board.rect.topleft
        self.rect = self.drawing_rect.move(board_topleft)

        # highlights
        self.draw_highlight()
        self.draw_move_circle()

    def draw_highlight(self):
        # dont draw if it isnt selected
        if not self.selected:
            return

        # create highlight and draw it onto the square image
        image_side_length = self.image.get_width()
        image_center = (image_side_length / 2, image_side_length / 2)
        highlight = pygame.Surface(self.image.size, pygame.SRCALPHA)
        highlight.fill(COLORS['board-highlight'])
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
        circle_radius = self.image.get_width() * MOVE_CIRCLE_SCALE
        circle = pygame.Surface((circle_radius*2, circle_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(
            circle, COLORS['move-circle'],
            (circle_radius, circle_radius), circle_radius)
        circle_rect = circle.get_rect(center=image_center)

        # draw circle onto image
        self.image.blit(circle, circle_rect)

    def on_click(self):
        """resolves square being clicked"""
        if self.board.clicked_outside():
            if self.selected:
                self.board.reset_flags()

        if not self.detect_click():
            return

        selected_square = self.board.find_selected_square()
        if selected_square:
            if self.valid_square:
                # case: make a move
                self.board.make_move(Move(self.piece, self.pos))
            else:
                # case: select another piece
                self.board.reset_flags()
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
            f"Piece: {self.piece}\n"
            f"Color: {self.color}\n"
            f"Hover: {self.hover}\n"
            f"Center: {self.drawing_rect.center}"
        )

        return get_tui_text_box(lines)
