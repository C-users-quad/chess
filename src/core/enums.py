from core.settings import *

class PieceNames(Enum):
    """enums for piece names"""
    KING = 'king'
    QUEEN = 'queen'
    ROOK = 'rook'
    BISHOP = 'bishop'
    KNIGHT = 'knight'
    PAWN = 'pawn'

class PieceColors(Enum):
    """enums for piece colors"""
    BLACK = 'black'
    WHITE = 'white'

class StateNames(Enum):
    BASE = "GameState"
    CHESS = "Chess"
    MAIN_MENU = "Main Menu"
    PROMOTION = "Promotion"
    SETTINGS = "Settings"
    NEW_GAME = "New Game"
