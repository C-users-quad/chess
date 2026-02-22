from core.settings import *
from core.utils import get_ui_elem, scale
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
        self.white_king = None
        self.black_king = None
        self.checkmate = False
        self.stalemate = False
        self.game_end = False
        self.winning_color = None
        self.populate_board() # give board initial pieces
        self.turn_color = 'white' # whos turn it is
        self.render()

    def render(self):
        """re-creates the board's image"""
        # get needed info
        window_width, window_height = GameContext.game.display.get_size()
        board_side_length = scale(get_ui_elem('board'), axis=BOARD_SCALE_AXIS)
        rounding = scale(get_ui_elem('rounding'), axis=BOARD_SCALE_AXIS)

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

    def render_game_end_overlay(self):
        pass

    def handle_checkmate(self):
        pieces = get_all_pieces_of_color(self.turn_color)
        player_can_move = False
        for piece in pieces:
            if piece.get_valid_moves():
                player_can_move = True
                break

        if not player_can_move:
            self.game_end = True
            king = self.white_king if self.turn_color == 'white' else self.black_king
            if king.in_check():
                self.checkmate = True
                self.winning_color = (
                    'white' if self.turn_color == 'black' else 'black')
            else:
                self.stalemate = True

    def find_selected_square(self):
        for row in self.board:
            for square in row:
                if square.selected: return square

    def reset_square_flags(self):
        for row in self.board:
            for square in row:
                if square.selected or square.valid_square:
                    square.selected = False
                    square.valid_square = False

    def show_valid_moves(self, selected_square):
        if selected_square.empty():
            return

        valid_moves = selected_square.piece.get_valid_moves()
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

    def make_move(self, move: Move, real_move=True):
        """
        makes the move.

        precondition: move is legal.
        """
        move.check_flags_before_move()
        self._apply_move(move, real_move)
        move.check_flags_after_move()

    def unmake_move(self, move: Move):
        self.get_square(*move.start).place(move.piece)
        if move.capture_square:
            self.get_square(*move.capture_square).place(move.captured_piece)
        self.get_square(*move.end).remove_piece()

    def _apply_move(self, move: Move, real_move=True):
        self.get_square(*move.start).remove_piece()
        self.get_square(*move.end).place(move.piece)
        self.capture_pawn_if_en_passant(move)
        self.change_turn()
        if real_move: self.reset_square_flags()
        self.reset_pawn_flags()

    def place_piece(self, piece, pos):
        """
        place a piece on a square at pos.
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
        if self.game_end:
            return

        for row in self.board:
            for square in row:
                square.update()

        self.handle_checkmate()

    def draw(self):
        self.render()
        GameContext.game.display.blit(self.image, self.rect)
        if self.game_end:
            self.render_game_end_overlay()

    def populate_board(self):
        """adds the initial arrangement of chess pieces to the board"""
        colors = ['black', 'white']
        # make back rows
        for color in colors:
            row = 0 if color == 'black' else 7
            col = 0
            for piece_class in [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]:
                pos = (row, col)
                piece = piece_class(pos, color)
                self.place_piece(piece, pos)
                if isinstance(piece, King):
                    if color == 'black':
                        self.black_king = piece
                    else:
                        self.white_king = piece
                col += 1

        # make pawns
        for color in colors:
            row = 1 if color == 'black' else 6
            col = 0
            for _ in range(8):
                pos = (row, col)
                self.place_piece(Pawn(pos, color), pos)
                col += 1

    def capture_pawn_if_en_passant(self, move: Move):
        # the piece thats moving must be a pawn
        if not isinstance(move.piece, Pawn):
            return

        # the position the piece is moving to must be an en passant move
        en_passant_moves = move.piece.get_en_passant_moves()
        if not move.end in en_passant_moves:
            return

        # capture the piece
        row, col = move.end
        victim_pos = (row - move.piece.dir, col)
        victim_square = self.get_square(*victim_pos)
        victim_square.remove_piece()

    def reset_pawn_flags(self):
        """
        once the turn changes,
        make the previous mover's pawns' reset their en passant flags
        """
        for row in self.board:
            for square in row:
                if square.empty():
                    continue
                if square.piece.color == self.turn_color:
                    continue
                if hasattr(square.piece, 'just_moved_forward_two'):
                    square.piece.just_moved_forward_two = False
