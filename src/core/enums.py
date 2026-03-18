from enum import StrEnum


class ResizeAxis(StrEnum):
    """resize axis for ui elements"""

    WIDTH = "width"
    HEIGHT = "height"
    MIN = "min"
    MAX = "max"
    AUTO = "auto"


class AnchorPoints(StrEnum):
    """used when assigning anchor points to ui elements"""

    TOPLEFT = "topleft"
    TOPRIGHT = "topright"
    BOTTOMLEFT = "bottomleft"
    BOTTOMRIGHT = "bottomright"
    MIDTOP = "midtop"
    MIDBOTTOM = "midbottom"
    MIDLEFT = "midleft"
    MIDRIGHT = "midright"
    CENTER = "center"


class SoundNames(StrEnum):
    """sound name identifiers"""

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
