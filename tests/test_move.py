from chess.move import Move
from chess.pieces import Rook, Queen, King, Pawn
from core.enums import PieceColors


class TestMoveInitialization:
    def test_move_stores_piece(self, empty_board):
        rook = Rook((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (0, 0))
        move = Move(rook, (0, 1), empty_board)
        assert move.piece == rook

    def test_move_stores_start_position(self, empty_board):
        rook = Rook((3, 4), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (3, 4))
        move = Move(rook, (3, 5), empty_board)
        assert move.start == (3, 4)

    def test_move_stores_end_position(self, empty_board):
        rook = Rook((3, 4), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (3, 4))
        move = Move(rook, (3, 5), empty_board)
        assert move.end == (3, 5)

    def test_move_defaults_to_real_move(self, empty_board):
        rook = Rook((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (0, 0))
        move = Move(rook, (0, 1), empty_board)
        assert move.real_move is True

    def test_move_can_be_unreal(self, empty_board):
        rook = Rook((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (0, 0))
        move = Move(rook, (0, 1), empty_board, real_move=False)
        assert move.real_move is False


class TestMoveFlags:
    def test_move_flags_initially_false(self, empty_board):
        rook = Rook((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (0, 0))
        move = Move(rook, (0, 1), empty_board)
        assert move.is_en_passant is False
        assert move.is_castle is False
        assert move.gives_check is False
        assert move.ends_game is False
        assert move.double_pawn_push is False
        assert move.is_promotion is False

    def test_double_pawn_push_flag(self, empty_board):
        pawn = Pawn((6, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(pawn, (6, 3))
        move = Move(pawn, (4, 3), empty_board)
        move.check_flags_before_move()
        assert move.double_pawn_push is True

    def test_en_passant_flag(self, empty_board):
        white_pawn = Pawn((3, 2), PieceColors.WHITE, empty_board)
        black_pawn = Pawn((1, 3), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_pawn, (3, 2))
        empty_board.place_piece(black_pawn, (1, 3))
        black_pawn.update_pos((3, 3))
        empty_board.place_piece(black_pawn, (3, 3))
        black_pawn.just_moved_forward_two = True
        move = Move(white_pawn, (2, 3), empty_board)
        move.check_flags_before_move()
        assert move.is_en_passant is True

    def test_promotion_flag(self, empty_board):
        pawn = Pawn((1, 3), PieceColors.WHITE, empty_board)
        empty_board.place_piece(pawn, (1, 3))
        move = Move(pawn, (0, 3), empty_board)
        move.check_flags_before_move()
        assert move.is_promotion is True

    def test_capture_sets_captured_piece(self, empty_board):
        white_rook = Rook((0, 0), PieceColors.WHITE, empty_board)
        black_rook = Rook((0, 1), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_rook, (0, 0))
        empty_board.place_piece(black_rook, (0, 1))
        move = Move(white_rook, (0, 1), empty_board)
        move.check_flags_before_move()
        assert move.captured_piece == black_rook
        assert move.capture_square == (0, 1)

    def test_original_has_moved_saved(self, empty_board):
        rook = Rook((0, 0), PieceColors.WHITE, empty_board)
        empty_board.place_piece(rook, (0, 0))
        move = Move(rook, (0, 1), empty_board)
        move.check_flags_before_move()
        assert move.original_has_moved is False
        assert rook.has_moved is True


class TestMoveGivesCheck:
    def test_move_gives_check_flag(self, empty_board):
        white_queen = Queen((0, 0), PieceColors.WHITE, empty_board)
        black_king = King((0, 7), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_queen, (0, 0))
        empty_board.place_piece(black_king, (0, 7))
        empty_board.white_king = King((7, 0), PieceColors.WHITE, empty_board)
        empty_board.black_king = black_king
        move = Move(white_queen, (0, 5), empty_board)
        move.check_flags_before_move()
        move.check_flags_after_move()
        assert move.gives_check is True

    def test_move_does_not_give_check(self, empty_board):
        white_queen = Queen((0, 0), PieceColors.WHITE, empty_board)
        black_king = King((7, 6), PieceColors.BLACK, empty_board)
        empty_board.place_piece(white_queen, (0, 0))
        empty_board.place_piece(black_king, (7, 6))
        empty_board.white_king = King((7, 0), PieceColors.WHITE, empty_board)
        empty_board.black_king = black_king
        move = Move(white_queen, (0, 5), empty_board)
        move.check_flags_before_move()
        move.check_flags_after_move()
        assert move.gives_check is False
