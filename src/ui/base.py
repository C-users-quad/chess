from core.settings import *
from core.utils import get_tui_text_box

class UIElement:
    """parent ui class that stores a surface and rect combo with a size and pos."""
    def __init__(self, pos, size, anchor):
        # initialize basic sprite attributes
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = pygame.Rect(pos, size)
        setattr(self.rect, anchor, pos)

    def update(self):
        pass

    def draw(self):
        GameContext.game.display.blit(self.image, self.rect)

    def __str__(self):
        text = (
            f"UI Element {hex(id(self))}\n"
            f"Size: {self.rect.size}\n"
            f"Topleft: {self.rect.topleft}\n"
            f"Center: {self.rect.center}\n"
            f"Bottomright: {self.rect.bottomright}"
        )
        return get_tui_text_box(text)
