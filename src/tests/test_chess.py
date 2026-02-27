"""Tests for chess engine components."""
import pytest
from unittest.mock import MagicMock, patch

class TestBoard:
    """Tests for Board class."""

    def test_board_initialization(self, mock_game_context):
        """Test Board initializes with 8x8 grid."""
        from chess.board import Board
        
        board = Board()
        
        assert len(board.board) == 8
        assert len(board.board[0]) == 8
        assert board.turn_color.value == "white"

    def test_board_has_kings(self, mock_game_context):
        """Test Board has white and black kings after initialization."""
        from chess.board import Board
        
        board = Board()
        
        assert board.white_king is not None
        assert board.black_king is not None

    def test_board_initial_turn_is_white(self, mock_game_context):
        """Test that white moves first."""
        from chess.board import Board
        
        board = Board()
        
        assert board.turn_color.value == "white"

    def test_get_square_returns_correct_square(self, mock_game_context):
        """Test get_square returns the correct board square."""
        from chess.board import Board
        
        board = Board()
        
        square = board.get_square((0, 0))
        assert square is not None
        assert square.pos == (0, 0)

    def test_pos_on_board_valid_positions(self, mock_game_context):
        """Test pos_on_board returns True for valid positions."""
        from chess.board import Board
        
        board = Board()
        
        assert board.pos_on_board((0, 0)) == True
        assert board.pos_on_board((7, 7)) == True
        assert board.pos_on_board((3, 4)) == True

    def test_pos_on_board_invalid_positions(self, mock_game_context):
        """Test pos_on_board returns False for invalid positions."""
        from chess.board import Board
        
        board = Board()
        
        assert board.pos_on_board((-1, 0)) == False
        assert board.pos_on_board((0, 8)) == False
        assert board.pos_on_board((8, 8)) == False


class TestPieces:
    """Tests for chess pieces."""

    def test_pawn_initialization_white(self, mock_game_context):
        """Test white pawn has correct direction."""
        from chess.pieces import Pawn
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        pawn = Pawn((6, 4), PieceColors.WHITE, board)
        
        assert pawn.dir == -1

    def test_pawn_initialization_black(self, mock_game_context):
        """Test black pawn has correct direction."""
        from chess.pieces import Pawn
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        pawn = Pawn((1, 4), PieceColors.BLACK, board)
        
        assert pawn.dir == 1

    def test_pawn_has_not_moved_initially(self, mock_game_context):
        """Test pawn has not moved initially."""
        from chess.pieces import Pawn
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        pawn = Pawn((6, 4), PieceColors.WHITE, board)
        
        assert pawn.has_moved == False

    def test_pawn_promotion_row_white(self, mock_game_context):
        """Test white pawn promotion row."""
        from chess.pieces import Pawn
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        pawn = Pawn((6, 4), PieceColors.WHITE, board)
        
        assert pawn.promotion_row == 0

    def test_pawn_promotion_row_black(self, mock_game_context):
        """Test black pawn promotion row."""
        from chess.pieces import Pawn
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        pawn = Pawn((1, 4), PieceColors.BLACK, board)
        
        assert pawn.promotion_row == 7


class TestRook:
    """Tests for Rook piece."""

    def test_rook_name(self, mock_game_context):
        """Test Rook has correct name."""
        from chess.pieces import Rook
        from core.enums import PieceNames
        
        assert Rook.name == PieceNames.ROOK


class TestBishop:
    """Tests for Bishop piece."""

    def test_bishop_name(self, mock_game_context):
        """Test Bishop has correct name."""
        from chess.pieces import Bishop
        from core.enums import PieceNames
        
        assert Bishop.name == PieceNames.BISHOP


class TestKnight:
    """Tests for Knight piece."""

    def test_knight_name(self, mock_game_context):
        """Test Knight has correct name."""
        from chess.pieces import Knight
        from core.enums import PieceNames
        
        assert Knight.name == PieceNames.KNIGHT

    def test_knight_directions_count(self, mock_game_context):
        """Test Knight has 8 L-shaped move directions."""
        from chess.pieces import Knight
        
        assert len(Knight.directions) == 8


class TestQueen:
    """Tests for Queen piece."""

    def test_queen_name(self, mock_game_context):
        """Test Queen has correct name."""
        from chess.pieces import Queen
        from core.enums import PieceNames
        
        assert Queen.name == PieceNames.QUEEN


class TestKing:
    """Tests for King piece."""

    def test_king_name(self, mock_game_context):
        """Test King has correct name."""
        from chess.pieces import King
        from core.enums import PieceNames
        
        assert King.name == PieceNames.KING

    def test_king_initialization(self, mock_game_context):
        """Test King can be initialized."""
        from chess.pieces import King
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        king = King((7, 4), PieceColors.WHITE, board)
        
        assert king.pos == (7, 4)
        assert king.color == PieceColors.WHITE


class TestMove:
    """Tests for Move class."""

    def test_move_initialization(self, mock_game_context):
        """Test Move can be initialized."""
        from chess.move import Move
        from chess.pieces import Pawn
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        pawn = Pawn((6, 4), PieceColors.WHITE, board)
        move = Move(pawn, (5, 4), board)
        
        assert move.piece == pawn
        assert move.start == (6, 4)
        assert move.end == (5, 4)

    def test_move_flags_initialized_false(self, mock_game_context):
        """Test all move flags are initialized to False."""
        from chess.move import Move
        from chess.pieces import Pawn
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        pawn = Pawn((6, 4), PieceColors.WHITE, board)
        move = Move(pawn, (5, 4), board)
        
        assert move.is_en_passant == False
        assert move.is_castle == False
        assert move.gives_check == False
        assert move.ends_game == False
        assert move.is_promotion == False

    def test_move_check_flags_sets_original_has_moved(self, mock_game_context):
        """Test check_flags_before_move stores original has_moved."""
        from chess.move import Move
        from chess.pieces import Pawn
        from chess.board import Board
        from core.enums import PieceColors
        
        board = Board()
        pawn = Pawn((6, 4), PieceColors.WHITE, board)
        move = Move(pawn, (5, 4), board)
        
        move.check_flags_before_move()
        
        assert move.original_has_moved == False
