from core.settings import (
    BOARD_SCALE_AXIS,
    COLORS,
    GameContext,
    GAME_END_ICON_SCALE,
    pygame,
)
from core.utils import get_ui_elem, scale, opposite_color
from core.images import GAME_END_ICONS
from core.enums import PieceColors, StateNames
from chess.square import BoardSquare
from chess.move import Move
from chess.pieces import (
    King,
    Knight,
    Pawn,
    Queen,
    Rook,
    Bishop,
    get_all_pieces_of_color,
)


class Board:
    """
    # The chessboard represented with a 2d array.
        - every index has a boardsquare object
    """

    def __init__(self):
        # make and populate the 2d board array with boardsquares
        self.board = [
            [
                BoardSquare((r, c), ("white-square", "black-square")[(r + c) % 2], self)
                for c in range(8)
            ]
            for r in range(8)
        ]
        self.turn_color = PieceColors.WHITE  # whos turn it is
        self.white_king = None
        self.black_king = None
        self.checkmate = False
        self.stalemate = False
        self.game_end = False
        self.winning_color = None
        self.populate_board()  # give board initial pieces
        self.render()

    def render(self):
        """re-creates the board's image"""
        # get needed info
        window_width, window_height = GameContext.game.display.get_size()
        board_side_length = scale(get_ui_elem("board"), axis=BOARD_SCALE_AXIS)
        rounding = scale(get_ui_elem("rounding"), axis=BOARD_SCALE_AXIS)

        # create border image
        self.image = pygame.Surface(
            size=(board_side_length, board_side_length), flags=pygame.SRCALPHA
        )

        # center board on screen
        self.rect = self.image.get_rect(center=(window_width / 2, window_height / 2))

        # draw boards border
        pygame.draw.rect(
            surface=self.image,
            color=COLORS["board-border"],
            rect=(0, 0, board_side_length, board_side_length),
            border_radius=rounding,
        )

        # draw squares onto board
        for row in self.board:
            for square in row:
                square.render()  # creates the squares image
                square.draw()  # draws the square onto the boards image

    def render_game_end_overlay(self):
        white_king_sqr = self.get_square(self.white_king.pos)
        black_king_sqr = self.get_square(self.black_king.pos)
        icon_length = white_king_sqr.rect.width * GAME_END_ICON_SCALE
        icon_size = (icon_length, icon_length)

        if self.checkmate:
            winning_sqr = (
                white_king_sqr
                if self.winning_color == PieceColors.WHITE
                else black_king_sqr
            )
            losing_sqr = (
                white_king_sqr
                if self.winning_color != PieceColors.WHITE
                else black_king_sqr
            )
            win_icon, lose_icon = GAME_END_ICONS["winner"], GAME_END_ICONS["loser"]

            win_icon = pygame.transform.smoothscale(win_icon, icon_size)
            lose_icon = pygame.transform.smoothscale(lose_icon, icon_size)

            win_icon_rect = win_icon.get_rect(center=winning_sqr.rect.topright)
            lose_icon_rect = lose_icon.get_rect(center=losing_sqr.rect.topright)

            GameContext.game.display.blit(win_icon, win_icon_rect)
            GameContext.game.display.blit(lose_icon, lose_icon_rect)

        elif self.stalemate:
            stalemate_icon = GAME_END_ICONS["stalemate"]
            stalemate_icon = pygame.transform.smoothscale(stalemate_icon, icon_size)

            icon_rect_white_king = stalemate_icon.get_rect(
                center=white_king_sqr.rect.topright
            )
            icon_rect_black_king = stalemate_icon.get_rect(
                center=black_king_sqr.rect.topright
            )

            GameContext.game.display.blit(stalemate_icon, icon_rect_white_king)
            GameContext.game.display.blit(stalemate_icon, icon_rect_black_king)

    def handle_game_end(self):
        pieces = get_all_pieces_of_color(self.turn_color, self)
        player_can_move = False
        for piece in pieces:
            if piece.get_legal_moves():
                player_can_move = True
                break

        if not player_can_move:
            white_king_sqr = self.get_square(self.white_king.pos)
            black_king_sqr = self.get_square(self.black_king.pos)
            self.game_end = True
            king = getattr(self, f"{piece.color}_king")
            if king.in_check():
                self.checkmate = True
                self.winning_color = opposite_color(self.turn_color)
                winning_sqr = (
                    white_king_sqr
                    if self.winning_color == PieceColors.WHITE
                    else black_king_sqr
                )
                losing_sqr = (
                    white_king_sqr
                    if self.winning_color != PieceColors.WHITE
                    else black_king_sqr
                )
                winning_sqr.winning_square = True
                losing_sqr.losing_square = True
            else:
                white_king_sqr.stalemate_square = True
                black_king_sqr.stalemate_square = True
                self.stalemate = True

        if self.game_end:
            self.reset_square_flags()
            GameContext.game.push_state(StateNames.NEW_GAME)

    def find_selected_square(self):
        for row in self.board:
            for square in row:
                if square.selected:
                    return square

    def reset_square_flags(self, real_move=True):
        if not real_move:
            return

        for row in self.board:
            for square in row:
                if square.selected or square.valid_square:
                    square.selected = False
                    square.valid_square = False

    def show_valid_moves(self, selected_square):
        if selected_square.empty():
            return

        valid_moves = selected_square.piece.get_legal_moves()
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

    def get_square(self, pos):
        row, col = pos
        return self.board[row][col]

    def pos_on_board(self, pos):
        row, col = pos
        return 0 <= row <= 7 and 0 <= col <= 7

    def make_move(self, move: Move):
        """
        makes the move.

        precondition: move is legal.
        """
        move.check_flags_before_move()
        self._apply_move(move)
        move.check_flags_after_move()
        move.play_move_sound()

    def unmake_move(self, move: Move):
        # reset squares
        self.place_piece(move.piece, move.start)
        self.remove_piece(move.end)
        if move.capture_square:
            self.place_piece(move.captured_piece, move.capture_square)

        # reset board
        self.reset_pawn_flags()
        self.change_turn()

        # reset piece
        move.piece.has_moved = move.original_has_moved
        if hasattr(move, "original_just_moved_forward_two"):
            move.piece.just_moved_forward_two = move.original_just_moved_forward_two
        if move.is_castle:
            rook = self.get_square(move.rook_end).piece
            self.remove_piece(move.rook_end)
            self.place_piece(rook, move.rook_start)
            rook.has_moved = False

    def _apply_move(self, move: Move):
        move.piece.has_moved = True
        self.remove_piece(move.start)
        self.place_piece(move.piece, move.end)
        self._capture_pawn_if_en_passant(move)
        self._move_rook_if_castling(move)
        self.handle_pawn_promotion(move)
        self.reset_square_flags(move.real_move)
        self.reset_pawn_flags()
        self.change_turn()

    def place_piece(self, piece, pos):
        """
        place a piece on a square at pos.
        used during piece creation.
        """
        square = self.get_square(pos)
        square.place(piece)
        piece.update_pos(pos)

    def remove_piece(self, pos):
        square = self.get_square(pos)
        square.remove_piece()

    def change_turn(self):
        self.turn_color = opposite_color(self.turn_color)

    def update(self):
        if self.game_end:
            return

        for row in self.board:
            for square in row:
                square.update()

        self.handle_game_end()

    def draw(self):
        self.render()
        GameContext.game.display.blit(self.image, self.rect)
        if self.game_end:
            self.render_game_end_overlay()

    def populate_board(self):
        """adds the initial arrangement of chess pieces to the board"""
        colors = list(PieceColors)
        # make back rows
        for color in colors:
            row = 0 if color == PieceColors.BLACK else 7
            col = 0
            for piece_class in [
                Rook,
                Knight,
                Bishop,
                Queen,
                King,
                Bishop,
                Knight,
                Rook,
            ]:
                pos = (row, col)
                piece = piece_class(pos, color, self)
                self.place_piece(piece, pos)
                if isinstance(piece, King):
                    setattr(self, f"{color}_king", piece)
                col += 1

        # make pawns
        for color in colors:
            row = 1 if color == PieceColors.BLACK else 6
            col = 0
            for _ in range(8):
                pos = (row, col)
                self.place_piece(Pawn(pos, color, self), pos)
                col += 1

    def _capture_pawn_if_en_passant(self, move: Move):
        # the piece thats moving must be a pawn
        if not isinstance(move.piece, Pawn):
            return

        # the position the piece is moving to must be an en passant move
        if not move.is_en_passant:
            return

        # capture the piece
        row, col = move.end
        victim_pos = (row - move.piece.dir, col)
        victim_square = self.get_square(victim_pos)
        victim_square.remove_piece()

    def _move_rook_if_castling(self, move: Move):
        if not move.is_castle:
            return

        # determine rooks initial and final positions
        kingside_castle_col = 6
        queenside_castle_col = 2

        if move.end[1] == kingside_castle_col:
            # kingside
            rook_initial_pos = (move.end[0], move.end[1] + 1)
            rook_final_pos = (move.end[0], move.end[1] - 1)
        elif move.end[1] == queenside_castle_col:
            # queenside
            rook_initial_pos = (move.end[0], move.end[1] - 2)
            rook_final_pos = (move.end[0], move.end[1] + 1)

        # move rook
        piece = self.get_square(rook_initial_pos).piece
        self.remove_piece(rook_initial_pos)
        self.place_piece(piece, rook_final_pos)

        # update move info
        move.rook_start = rook_initial_pos
        move.rook_end = rook_final_pos

    def reset_pawn_flags(self):
        """
        once the turn changes,
        make the previous mover's pawns' reset their en passant flags
        """
        previous_move_color = opposite_color(self.turn_color)
        for row in self.board:
            for square in row:
                if square.empty():
                    continue
                if not isinstance(square.piece, Pawn):
                    continue
                if square.piece.color != previous_move_color:
                    continue
                square.piece.just_moved_forward_two = False

    def handle_pawn_promotion(self, move: Move):
        if not move.real_move:
            return

        if not move.is_promotion:
            return

        GameContext.game.push_state(StateNames.PROMOTION, (move,))
