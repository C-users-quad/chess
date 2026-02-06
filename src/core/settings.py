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
```
"""
SIZE_RATIOS = {
    'board': (600 / BASE_HEIGHT, 'height'),
    'rounding': (10 / BASE_HEIGHT, 'height'),
    'border-width': (10 / BASE_HEIGHT, 'height'),
    'padding': (10 / BASE_HEIGHT, 'height'),
    'spacing': (15 / BASE_HEIGHT, 'height'),
    'title': (75 / BASE_HEIGHT, 'height'),
    'subtitle': (50 / BASE_HEIGHT, 'height'),
    'text': (25 / BASE_HEIGHT, 'height'),
    'sidebar-width': (50 / BASE_WIDTH, 'width'),
    'board-border': (50 / BASE_HEIGHT, 'height')
}
"""
## ratios used in order to determine size of elements drawn
## relative to current window height.
### key/value pair is organized as such:
key:
 - str representing ui element.

value:
 - a tuple with the first index being the ratio and
 - the second index containing whether the ratio is
   with respect to the base width/height of the window.
### the current keys are:
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
'board-border' - width of the board's border
```
"""
