import pygame
from os.path import join
import sys
from pathlib import Path
from typing import Literal
from rich.console import Console
from enum import StrEnum


# override print to rich printing for colors yay!!
print = Console().print


class GameContext:
    """container for game object so that it can be globally accessed"""

    game = None


# window stuff
WINDOW_SIZE = (800, 600)
FPS = 60

# file stuff
BUTTON_SOUNDS_FILEPATH: str = join("assets", "sounds", "ui", "button")
PIECE_SOUNDS_FILEPATH: str = join("assets", "sounds", "piece_moves")
SLIDER_SOUNDS_FILEPATH: str = join("assets", "sounds", "ui", "slider")
FONT_PATH = join("assets", "fonts", "MerriweatherSans-Medium.ttf")

# ui-related stuff. colors, sizes, etc.
BASE_WIDTH, BASE_HEIGHT = (1256, 750)
"""reference dimensions for scaling system"""
ANTIALIAS = True
STATE_DIM_ALPHA = 100
MIN_UI_SIZE = 1

# scale axis
BOARD_SCALE_AXIS = "height"
UI_SCALE_AXIS = "min"
TEXT_SCALE_AXIS = "height"

COLORS = {
    "bg": "#68f66a",
    "clear": (0,0,0,0),
    "text": "#FFFFFF",
    "ui-bg": "#220A0A",
    "ui-border": "#32c38b",
    "button-highlight": "#0000008C",
    "board-border": "#6F3110",
    "white-square": "#F1E1D8",
    "black-square": "#311201",
    "board-highlight": "#ffee008e",
    "move-circle": "#271978A0",
    "state-dim": (0, 0, 0),
    "winning-sqr-highlight": "#44ff00cd",
    "losing-sqr-highlight": "#ff0000c1",
    "stalemate-sqr-highlight": "#000000CC",
    "promotion-ui-bg": "#ffffff",
    "promotion-ui-btn": "#919191",
    "slider-base-light": "#2e84ca",
    "slider-base-dark": "#224a6c",
}
"""
## dicitonary for colors.

### current keys are:

```
'clear' - color used to clear the screen
'text' - text color
'ui-bg' - main background color for ui elements
'ui-border' - main color for ui elements' borders
'button-highlight' - color used if button is highlighted
'board-border' - color used for the chess boards sides
'white-square' - color used for the white squares
'black-square' - color used for the black squares
'move-circle' - color of circle drawn on squares that a piece can move to
'winning-sqr-highlight' - color the square of the winning king is highlighted
'losing-sqr-highlight' - color the square of the losing king is highlighted
'stalemate-sqr-highlight' - color the kings squares are highlighted if stalemate
'promotion-ui-bg' - color the background box of the pawn promotion ui is
'promotion-ui-btn' - color the buttons are in the pawn promotion ui
'slider-base-light' - color of the right side of the line in a slider ui element
'slider-base-dark' - color of the left side of the line in a slider ui element
```
"""
SIZE_RATIOS = {
    "board": (600 / BASE_HEIGHT),
    "rounding": (10 / BASE_HEIGHT),
    "border-width": (10 / BASE_HEIGHT),
    "padding": (7 / BASE_HEIGHT),
    "spacing": (15 / BASE_HEIGHT),
    "title": (75 / BASE_HEIGHT),
    "subtitle": (50 / BASE_HEIGHT),
    "text": (25 / BASE_HEIGHT),
    "sidebar-width": (50 / BASE_WIDTH),
    "board-border": (50 / BASE_HEIGHT),
}
"""
## ratios used in order to determine size of elements drawn
```
'board' - the side length of the board
'rounding' - the rounding of corners
'border-width' - border width on cetain parts of the ui
'padding' - distance between parts inside of a particular ui element
'spacing' - distance between ui elements
'title' - title font size
'subtitle' - subtitle font size
'text' - text font size
'sidebar-width' - width of sidebar in main menu
'board-border' - width of the boards border
```
"""
# relative to board square size
PIECE_SCALE = 0.95
MOVE_CIRCLE_SCALE = 0.2
GAME_END_ICON_SCALE = 0.5
