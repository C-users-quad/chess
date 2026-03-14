from core.settings import StrEnum


class SoundNames(StrEnum):
    CAPTURE = "capture"
    CASTLE = "castle"
    CHECK = "check"
    GAME_END = "game-end"
    MOVE = "move"
    PROMOTE = "promote"
    BUTTON_DOWN = "button-down"
    BUTTON_UP = "button-up"
    SLIDER = "slider"


class PieceNames(StrEnum):
    """enums for piece names"""

    KING = "king"
    QUEEN = "queen"
    ROOK = "rook"
    BISHOP = "bishop"
    KNIGHT = "knight"
    PAWN = "pawn"


class PieceColors(StrEnum):
    """enums for piece colors"""

    BLACK = "black"
    WHITE = "white"


class StateNames(StrEnum):
    """enums for state names"""

    BASE = "GameState"
    CHESS = "Chess"
    MAIN_MENU = "Main Menu"
    PROMOTION = "Promotion"
    SETTINGS = "Settings"
    NEW_GAME = "New Game"
