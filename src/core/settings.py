import pygame
from os.path import join
import sys
from pathlib import Path
from typing import Literal

class GameContext:
    """container for game object so that it can be globally accessed"""
    game = None

WINDOW_SIZE = (800, 600)
FPS = 60

# ui-related stuff. colors, sizes, etc.
BASE_WIDTH, BASE_HEIGHT = (1256, 750)
"""the window sizes i used when making the ui, used for scaling"""
ANTIALIAS = True
COLORS = {
    'clear': "#68f66a",
    'text': "#FFFFFF",
    'ui-bg': "#220A0A",
    'ui-border': "#32c38b",
    'button-highlight': "#1F6F78",
    'board-border': "#6F3110",
    'white-square': "#F1E1D8",
    'black-square': "#311201",
    'board-highlight': "#ffee008e",
    'move-circle': "#271978A0"
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
'sidebar' - color of the sidebar used in the main menu
'move-circle' - color of circle drawn on squares that a piece can move to
```
"""
SIZE_RATIOS = {
    'board': (600 / BASE_HEIGHT),
    'rounding': (10 / BASE_HEIGHT),
    'border-width': (10 / BASE_HEIGHT),
    'padding': (10 / BASE_HEIGHT),
    'spacing': (15 / BASE_HEIGHT),
    'title': (75 / BASE_HEIGHT),
    'subtitle': (50 / BASE_HEIGHT),
    'text': (25 / BASE_HEIGHT),
    'sidebar-width': (50 / BASE_WIDTH),
    'board-border': (50 / BASE_HEIGHT),
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
PIECE_SCALE = 0.95
MOVE_CIRCLE_SCALE = 0.2
