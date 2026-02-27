from core.settings import *
from core.utils import asset_path
from core.enums import PieceNames, PieceColors

PIECE_IMAGES = {}
"""
Piece image surfaces

key: (PieceColors(Enum), PieceNames(Enum)) -> value: pygame.Surface()

current keys:
```
every combination of piece color enum to piece name enum -> corresponding piece image
```
"""
for piece in list(PieceNames):
    for color in list(PieceColors):
        key = (color, piece)
        filename = f'{piece.value}-{color.value}.png'
        path = join('assets', 'images', 'pieces', filename)
        PIECE_IMAGES[key] = pygame.image.load(asset_path(path))

GAME_END_ICONS = {}
"""
Icons used for game end

key: str -> value: pygame.Surface()

current keys:
```
'winner' - victory crown icon
'loser' - losing icons
'stalemate' - \"1/2\" stalemate icon
```
"""
for key in ['loser', 'winner', 'stalemate']:
    path = join('assets', 'images', 'game_end_icons', f"{key}.png")
    GAME_END_ICONS[key] = pygame.image.load(asset_path(path))
