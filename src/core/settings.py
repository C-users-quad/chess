from __future__ import annotations
import pygame
from os.path import join
import sys
from pathlib import Path
from typing import Literal
from rich.console import Console
from core.enums import ResizeAxis
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.main import Game

# override print to rich printing for colors yay!!
print = Console().print


class VariableSettings:
    """
    container for global settings
    that can be changed by the user via the settings menu ui
    """

    fps: int = 60
    """[0,inf] fps cap"""
    sfx_volume: float = 0.5
    """[0,1] the volume of the sound effects"""
    flip_board: bool = True
    """determines if the board visually flips every turn"""
    player_time: int = 10
    """the time each player has in seconds"""

    @classmethod
    def setter(cls, attr):
        """
        Gives a callable that takes in argument value that
        allows you to change the value
        of a variable setting with variable name attr.

        Args:
            attr (str) : name of the variable setting you wish to obtain a setter for
        Returns:
            setter (callable) : the variable settings setter.
        """
        return lambda value: setattr(cls, attr, value)


class GameContext:
    """container for game object so that it can be globally accessed"""

    game: Game = None


# sound stuff
DEFAULT_FADEOUT_TIME = 250
MIN_VOLUME, MAX_VOLUME = 0.0, 1.0
"""min and max volume floats for pygame.mixer.Sound's"""

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
"""integer from 0->255 where 0 means no dim to 255 which means black."""
MIN_UI_SIZE = 1
Z_MAX = 9999
"""used to z-order elements that will always be on top of others"""

# scale axis
BOARD_RESIZE_AXIS = ResizeAxis.HEIGHT
TEXT_RESIZE_AXIS = ResizeAxis.HEIGHT

COLORS = {
    "bg": "#68f66a",
    "clear": "#00000000",
    "text": "#FFFFFF",
    "ui-bg": "#220A0A",
    "ui-border": "#32c38b",
    "button-highlight": "#00000055",
    "board-border": "#6F3110",
    "white-square": "#F1E1D8",
    "black-square": "#311201",
    "board-highlight": "#ffee008e",
    "move-circle-dark": "#271978A0",
    "move-circle-light": "#3B29A09F",
    "state-dim": "#000000",
    "winning-sqr-highlight": "#44ff00cd",
    "losing-sqr-highlight": "#ff0000c1",
    "stalemate-sqr-highlight": "#000000CC",
    "promotion-ui-bg": "#ffffff",
    "promotion-ui-btn": "#919191",
    "slider-base-light": "#2e84ca",
    "slider-base-dark": "#224a6c",
    "slider-marker": "#1b1a44",
    "checkbox-ticked": "#4790d3",
    "checkbox-unticked": "#3F3F43",
    "checkbox-border": "#000000",
}
"""
## dicitonary for colors.

### current keys are:

```
'bg' - color used to fill the screen before each drawing sequence
'clear' - color used to wipe surfaces clean (transparent black)
'text' - text color
'ui-bg' - main background color for ui elements
'ui-border' - main color for ui elements' borders
'button-highlight' - color used if button is highlighted
'board-border' - color used for the chess boards sides
'white-square' - color used for the white squares
'black-square' - color used for the black squares
'board-highlight' - color for board squares when they are clicked
'move-circle' - color of circle drawn on squares that a piece can move to
'winning-sqr-highlight' - color the square of the winning king is highlighted
'losing-sqr-highlight' - color the square of the losing king is highlighted
'stalemate-sqr-highlight' - color the kings squares are highlighted if stalemate
'promotion-ui-bg' - color the background box of the pawn promotion ui is
'promotion-ui-btn' - color the buttons are in the pawn promotion ui
'slider-base-light' - color of the right side of the line in a slider ui element
'slider-base-dark' - color of the left side of the line in a slider ui element
'checkbox-ticked' - color for ticked checkboxes
'checkbox-unticked' - color for unticked checkboxes
'checkbox-border' - color for the checkboxes border
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
```
"""
# ratios that are relative to things other than the base window size
# relative to board square side length
BOARD_SQUARE_RATIOS = {"piece": 0.95, "move-circle": 0.2, "game-end-icon": 0.5}
# relative to checkbox side length
CHECKBOX_RATIOS = {"border": 0.2}
# relative to board side length
BOARD_RATIOS = {"border": 0.1}
