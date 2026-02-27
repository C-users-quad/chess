from core.settings import *
from core.utils import asset_path

# initialize mixer so pygame.Sound() works
pygame.mixer.init()

PIECE_SOUNDS = {}
"""
dict with pygame sound objects corresponding to chess move sounds

key: str -> value: pygame.Sound()

current keys:
```
'capture' - piece capture
'castle' - king castle
'check' - king check
'move' - piece move
'game-end' - checkmate/stalemate etc.
'promote' - pawn promotion
```
"""
for key in ['capture', 'castle', 'check', 'move', 'game-end', 'promote']:
    filename = f"{key}.mp3"
    path = join(PIECE_SOUNDS_PATH, filename)
    PIECE_SOUNDS[key] = pygame.Sound(asset_path(path))

BUTTON_SOUNDS = {}
"""
dict with pygame sound objects corresponding to button presses

key: str -> value: pygame.Sound()

current keys:
```
'button-down' - button press
'button-up' - button release
```
"""
for key in ['button-down', 'button-up']:
    filename = f"{key}.mp3"
    path = join(BUTTON_SOUNDS_PATH, filename)
    BUTTON_SOUNDS[key] = pygame.Sound(asset_path(path))
