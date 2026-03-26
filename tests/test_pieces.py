from chess.pieces import Rook, Bishop, Queen, Knight, Pawn, King
from core.enums import PieceColors, PieceNames


class TestRook:
    def test_rook_gets_horizontal_and_vertical_directions(self):
        assert len(Rook.directions) == 4

    def test_rook_value(self):
        assert Rook.value == 5

    def test_rook_name(self):
        assert Rook.name == PieceNames.ROOK

    def test_rook_pseudo_moves_horizontal_right(self, empty_board):
        rook = Rook((3, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (3, 3))
        moves = rook.get_pseudo_moves()
        assert (3, 4) in moves
        assert (3, 5) in moves
        assert (3, 6) in moves
        assert (3, 7) in moves

    def test_rook_pseudo_moves_horizontal_left(self, empty_board):
        rook = Rook((3, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (3, 3))
        moves = rook.get_pseudo_moves()
        assert (3, 2) in moves
        assert (3, 1) in moves
        assert (3, 0) in moves

    def test_rook_pseudo_moves_vertical_up(self, empty_board):
        rook = Rook((3, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (3, 3))
        moves = rook.get_pseudo_moves()
        assert (4, 3) in moves
        assert (5, 3) in moves
        assert (6, 3) in moves
        assert (7, 3) in moves

    def test_rook_pseudo_moves_vertical_down(self, empty_board):
        rook = Rook((3, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (3, 3))
        moves = rook.get_pseudo_moves()
        assert (2, 3) in moves
        assert (1, 3) in moves
        assert (0, 3) in moves

    def test_rook_pseudo_moves_blocked_by_friendly_piece(self, empty_board):
        rook = Rook((3, 3), PieceColors.WHITE, empty_board)
        friendly_rook = Rook((3, 5), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (3, 3))
        empty_board.place_piece(friendly_rook, (3, 5))
        moves = rook.get_pseudo_moves()
        assert (3, 4) in moves
        assert (3, 5) not in moves
        assert (3, 6) not in moves

    def test_rook_pseudo_moves_captures_enemy_piece(self, empty_board):
        rook = Rook((3, 3), PieceColors.WHITE, empty_board)
        enemy_rook = Rook((3, 5), PieceColors.BLACK, empty_board)
        empty_board.place_piece(rook, (3, 3))
        empty_board.place_piece(enemy_rook, (3, 5))
        moves = rook.get_pseudo_moves()
        assert (3, 4) in moves
        assert (3, 5) in moves
        assert (3, 6) not in moves


class TestBishop:
    def test_bishop_gets_diagonal_directions(self):
        assert len(Bishop.directions) == 4

    def test_bishop_value(self):
        assert Bishop.value == 3

    def test_bishop_name(self):
        assert Bishop.name == PieceNames.BISHOP

    def test_bishop_pseudo_moves_all_diagonals(self, empty_board):
        bishop = Bishop((3, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(bishop, (3, 3))
        moves = bishop.get_pseudo_moves()
        assert (4, 4) in moves
        assert (5, 5) in moves
        assert (6, 6) in moves
        assert (7, 7) in moves
        assert (2, 4) in moves
        assert (1, 5) in moves
        assert (0, 6) in moves
        assert (4, 2) in moves
        assert (5, 1) in moves
        assert (6, 0) in moves
        assert (2, 2) in moves
        assert (1, 1) in moves
        assert (0, 0) in moves

    def test_bishop_pseudo_moves_blocked_by_friendly(self, empty_board):
        bishop = Bishop((3, 3), PieceColors.WHITE, empty_board)
        friendly_bishop = Bishop((5, 5), PieceColors.WHITE, empty_board)
        empty_board.place_piece(bishop, (3, 3))
        empty_board.place_piece(friendly_bishop, (5, 5))
        moves = bishop.get_pseudo_moves()
        assert (4, 4) in moves
        assert (5, 5) not in moves


class TestQueen:
    def test_queen_has_all_sliding_directions(self):
        assert len(Queen.directions) == 8

    def test_queen_value(self):
        assert Queen.value == 9

    def test_queen_name(self):
        assert Queen.name == PieceNames.QUEEN

    def test_queen_combines_rook_and_bishop_moves(self, empty_board):
        queen = Queen((3, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(queen, (3, 3))
        moves = queen.get_pseudo_moves()
        assert (3, 7) in moves
        assert (0, 3) in moves
        assert (0, 0) in moves
        assert (7, 7) in moves


class TestKnight:
    def test_knight_gets_8_l_directions(self):
        assert len(Knight.directions) == 8

    def test_knight_value(self):
        assert Knight.value == 3

    def test_knight_name(self):
        assert Knight.name == PieceNames.KNIGHT

    def test_knight_pseudo_moves_center(self, empty_board):
        knight = Knight((4, 4), PieceColors.WHITE, empty_board)
        empty_board.place_piece(knight, (4, 4))
        moves = knight.get_pseudo_moves()
        expected_moves = [
            (2, 3),
            (2, 5),
            (3, 2),
            (3, 6),
            (5, 2),
            (5, 6),
            (6, 3),
            (6, 5),
        ]
        for move in expected_moves:
            assert move in moves

    def test_knight_pseudo_moves_corner(self, empty_board):
        knight = Knight((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(knight, (0, 0))
        moves = knight.get_pseudo_moves()
        expected_moves = [(1, 2), (2, 1)]
        for move in expected_moves:
            assert move in moves

    def test_knight_can_jump_over_pieces(self, empty_board):
        knight = Knight((4, 4), PieceColors.WHITE, empty_board)
        for i in range(1, 4):
            empty_board.place_piece(
                Rook((i, 4), PieceColors.WHITE, empty_board), (i, 4)
            )
        empty_board.place_piece(knight, (4, 4))
        moves = knight.get_pseudo_moves()
        assert (2, 3) in moves
        assert (2, 5) in moves


class TestPawn:
    def test_white_pawn_value(self):
        assert Pawn.value == 1

    def test_white_pawn_name(self):
        assert Pawn.name == PieceNames.PAWN

    def test_white_pawn_moves_up(self, empty_board):
        pawn = Pawn((6, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(pawn, (6, 3))
        assert pawn.dir == -1

    def test_black_pawn_moves_down(self, empty_board):
        pawn = Pawn((1, 3), PieceColors.BLACK, empty_board)
        empty_board.place_piece(pawn, (1, 3))
        assert pawn.dir == 1

    def test_pawn_initial_double_move(self, empty_board):
        pawn = Pawn((6, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(pawn, (6, 3))
        moves = pawn.get_pseudo_moves()
        assert (5, 3) in moves
        assert (4, 3) in moves

    def test_pawn_single_forward_move(self, empty_board):
        pawn = Pawn((4, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(pawn, (4, 3))
        moves = pawn.get_pseudo_moves()
        assert (3, 3) in moves

    def test_pawn_blocked_cannot_move(self, empty_board):
        pawn = Pawn((6, 3), PieceColors.WHITE, empty_board)
        blocking_pawn = Pawn((5, 3), PieceColors.BLACK, empty_board)
        empty_board.place_piece(pawn, (6, 3))
        empty_board.place_piece(blocking_pawn, (5, 3))
        moves = pawn.get_pseudo_moves()
        assert (5, 3) not in moves
        assert (4, 3) not in moves

    def test_pawn_captures_diagonally(self, empty_board):
        pawn = Pawn((5, 3), PieceColors.WHITE, empty_board)
        enemy_pawn = Pawn((4, 2), PieceColors.BLACK, empty_board)
        empty_board.place_piece(pawn, (5, 3))
        empty_board.place_piece(enemy_pawn, (4, 2))
        moves = pawn.get_pseudo_moves()
        assert (4, 2) in moves

    def test_pawn_cannot_capture_forward(self, empty_board):
        pawn = Pawn((5, 3), PieceColors.WHITE, empty_board)
        enemy_pawn = Pawn((4, 3), PieceColors.BLACK, empty_board)
        empty_board.place_piece(pawn, (5, 3))
        empty_board.place_piece(enemy_pawn, (4, 3))
        moves = pawn.get_pseudo_moves()
        assert (4, 3) not in moves

    def test_pawn_en_passant_setup(self, empty_board):
        white_pawn = Pawn((3, 2), PieceColors.WHITE, empty_board)
        black_pawn = Pawn((1, 3), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_pawn, (3, 2))
        empty_board.place_piece(black_pawn, (1, 3))
        black_pawn.update_pos((3, 3))
        empty_board.place_piece(black_pawn, (3, 3))
        black_pawn.just_moved_forward_two = True
        en_passant_moves = white_pawn.get_en_passant_moves()
        assert (2, 3) in en_passant_moves

    def test_pawn_attack_moves(self, empty_board):
        pawn = Pawn((4, 4), PieceColors.WHITE, empty_board)
        empty_board.place_piece(pawn, (4, 4))
        attacks = pawn.get_attack_moves()
        assert (3, 3) in attacks
        assert (3, 5) in attacks


class TestKing:
    def test_king_value(self):
        assert King.value is not None

    def test_king_name(self):
        assert King.name == PieceNames.KING

    def test_king_adjacent_moves(self, empty_board):
        king = King((4, 4), PieceColors.WHITE, empty_board)
        empty_board.place_piece(king, (4, 4))
        empty_board.white_king = king
        moves = king.get_pseudo_moves()
        assert (3, 3) in moves
        assert (3, 4) in moves
        assert (3, 5) in moves
        assert (4, 3) in moves
        assert (4, 5) in moves
        assert (5, 3) in moves
        assert (5, 4) in moves
        assert (5, 5) in moves

    def test_king_corner_moves(self, empty_board):
        king = King((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(king, (0, 0))
        empty_board.white_king = king
        moves = king.get_pseudo_moves()
        assert (0, 1) in moves
        assert (1, 0) in moves
        assert (1, 1) in moves

    def test_king_in_check(self, empty_board):
        king = King((4, 4), PieceColors.WHITE, empty_board)
        queen = Queen((4, 7), PieceColors.BLACK, empty_board)
        empty_board.place_piece(king, (4, 4))
        empty_board.place_piece(queen, (4, 7))
        empty_board.white_king = king
        assert king.in_check() is True

    def test_king_not_in_check(self, empty_board):
        king = King((4, 4), PieceColors.WHITE, empty_board)
        queen = Queen((7, 6), PieceColors.BLACK, empty_board)
        blocker = Rook((5, 5), PieceColors.WHITE, empty_board)
        empty_board.place_piece(king, (4, 4))
        empty_board.place_piece(queen, (7, 6))
        empty_board.place_piece(blocker, (5, 5))
        empty_board.white_king = king
        assert king.in_check() is False


class TestPieceFilterIllegalMoves:
    def test_piece_cannot_move_into_check(self, empty_board):
        king = King((0, 0), PieceColors.WHITE, empty_board)
        rook = Rook((0, 7), PieceColors.BLACK, empty_board)
        empty_board.place_piece(king, (0, 0))
        empty_board.place_piece(rook, (0, 7))
        empty_board.white_king = king
        empty_board.black_king = King((7, 7), PieceColors.BLACK, empty_board)
        empty_board.place_piece(empty_board.black_king, (7, 7))
        legal_moves = king.get_legal_moves()
        assert (0, 1) not in legal_moves

    def test_piece_can_block_check(self, empty_board):
        king = King((0, 0), PieceColors.WHITE, empty_board)
        rook = Rook((0, 5), PieceColors.BLACK, empty_board)
        blocker = Rook((1, 1), PieceColors.WHITE, empty_board)
        empty_board.place_piece(king, (0, 0))
        empty_board.place_piece(rook, (0, 5))
        empty_board.place_piece(blocker, (1, 1))
        empty_board.white_king = king
        empty_board.black_king = King((7, 7), PieceColors.BLACK, empty_board)
        empty_board.place_piece(empty_board.black_king, (7, 7))
        legal_moves = king.get_legal_moves()
        assert (1, 0) in legal_moves
