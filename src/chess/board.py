from core.settings import *
from core.utils import get_ui_elem
from chess.square import BoardSquare
from chess.pieces import *

class Board:
    """
    # The chessboard represented with a 2d array.
        - every index has a boardsquare object
    """
    def __init__(self):
        # make and populate the 2d board array with boardsquares
        self.board = [
            [BoardSquare((r,c), ('white-square','black-square')[(r+c)%2], self)
             for c in range(8)] for r in range(8)
        ]
        populate_board(self) # give board initial pieces
        self.turn_color = 'white' # whos turn it is
        self.render()

    def render(self):
        """re-creates the board's image"""
        # get needed info
        window_width, window_height = GameContext.game.display.get_size()
        board_side_length = get_ui_elem('board')
        rounding = get_ui_elem('rounding')

        # create border image
        self.image = pygame.Surface(
            (board_side_length, board_side_length),
            pygame.SRCALPHA)

        # center board on screen
        self.rect = self.image.get_rect(
            center=(window_width/2, window_height/2))

        # draw boards border
        pygame.draw.rect(
            self.image, COLORS['board-border'],
            (0,0,board_side_length,board_side_length),
            border_radius=rounding)

        # draw squares onto board
        for row in self.board:
            for square in row:
                square.render() # creates the squares image
                square.draw() # draws the square onto the boards image

    def find_selected_square(self):
        for row in self.board:
            for square in row:
                if square.selected: return square

    def reset_flags(self):
        for row in self.board:
            for square in row:
                if square.selected or square.valid_square:
                    square.selected = False
                    square.valid_square = False

    def show_valid_moves(self, selected_square):
        if selected_square.empty():
            return

        valid_moves = selected_square.piece.get_valid_moves() # code breaks here
        if not valid_moves:
            return

        for row in self.board:
            for square in row:
                if square.pos in valid_moves:
                    square.valid_square = True

    def clicked_outside(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return False
        if not pygame.mouse.get_just_released()[0]:
            return False
        return True

    def get_square(self, row, col):
        return self.board[row][col]

    def pos_on_board(self, row, col):
        return 0 <= row <= 7 and 0 <= col <= 7

    def move_piece(
        self, piece, end_pos: tuple[int, int]):
        """
        moves a piece to end pos. assumes move is legal.

        Args:
            piece (Piece): the piece to be moved
            end_pos (tuple[int, int]): the position the piece will be moved to
            represented as (row, col) indices in the board array.
        """
        start_row, start_col = piece.pos
        end_row, end_col = end_pos
        start_square = self.board[start_row][start_col]
        end_square = self.board[end_row][end_col]
        start_square.remove_piece()
        capture_pawn_if_en_passant(piece, self, end_pos)
        self.place_piece(piece, end_square.pos)
        reset_pawn_conditions(self)
        piece.has_moved = True

    def place_piece(self, piece, pos):
        """
        place a piece at pos.
        used during piece creation.
        """
        row, col = pos
        square = self.board[row][col]
        square.place(piece)
        piece.update_pos(pos)

    def change_turn(self):
        if self.turn_color == 'white':
            self.turn_color = 'black'
        else:
            self.turn_color = 'white'

    def update(self):
        for row in self.board:
            for square in row:
                square.update()

    def draw(self):
        self.render()
        GameContext.game.display.blit(self.image, self.rect)

def capture_pawn_if_en_passant(piece, board: Board, end_pos):
    # the piece thats moving must be a pawn
    if not isinstance(piece, Pawn):
        return
    print("boom")

    # the position the piece is moving to must be an en passant move
    en_passant_moves = piece.get_en_passant_moves()
    if not end_pos in en_passant_moves:
        return

    # capture the piece
    row, col = end_pos
    victim_pos = (row - piece.dir, col)
    victim_square = board.get_square(*victim_pos)
    print("yee")
    victim_square.remove_piece()

def reset_pawn_conditions(board: Board):
    """
    once the turn changes,
    make the previous mover's pawns' reset their en passant flags
    """
    for row in board.board:
        for square in row:
            if square.empty():
                continue
            if square.piece.color == board.turn_color:
                continue
            if hasattr(square.piece, 'just_moved_forward_two'):
                square.piece.just_moved_forward_two = False

def populate_board(board: Board):
    """adds the initial arrangement of chess pieces to the board"""
    colors = ['black', 'white']
    # make back rows
    for color in colors:
        row = 0 if color == 'black' else 7
        col = 0
        for piece in [Rook, Knight, Bishop, Queen, Queen, Bishop, Knight, Rook]:
            pos = (row, col)
            board.place_piece(piece(pos, color), pos)
            col += 1

    # make pawns
    for color in colors:
        row = 1 if color == 'black' else 6
        col = 0
        for _ in range(8):
            pos = (row, col)
            board.place_piece(Pawn(pos, color), pos)
            col += 1
