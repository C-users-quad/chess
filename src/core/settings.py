import pygame
from os.path import join
import sys
from pathlib import Path

class GameContext:
    """container for game object so that it can be globally accessed"""
    game = None

WINDOW_SIZE = (800, 600)
FPS = 60

# ui-related stuff. colors, sizes, etc.
ROUNDING = 10
BORDER_WIDTH = 10
ANTIALIAS = True
PADDING = 5
SPACING = 10
COLORS = {
    'clear': "#68f66a",
    'text': "#FFFFFF",
    'ui-bg': "#220A0A",
    'ui-border': "#32c38b",
    'button-highlight': "#1F6F78",
}
"""
dicitonary for colors. current keys are:
```
'clear' - color used to clear the screen
'text' - text color
'ui-bg' - main background color for ui elements
'ui-border' - main color for ui elements' borders
'button-highlight' - color used if button is highlighted
```
"""
FONT_SIZES = {
    'title': 50,
    'subtitle': 25,
    'text': 15
}
"""
dictionary for font sizes. current keys are:
```
'title' - largest font size
'subtitle' - medium font size
'text' - smallest font size
```
"""
