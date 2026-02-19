from core.settings import *
from core.utils import get_tui_text_box, resize

class UIElement:
    """parent ui class that stores a surface and rect combo with a size and pos."""
    def __init__(self, pos, size, anchor, **kwargs):
        # initialize basic sprite attributes
        super().__init__(**kwargs)
        self.size = size
        self.pos = pos
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = pygame.Rect(pos, size)
        self.anchor = anchor
        setattr(self.rect, self.anchor, self.pos)
        self.win_base_size = self.game.display.get_size()
        """used to resize ui elements dynamically"""

    @property
    def game(self):
        return GameContext.game

    def update(self):
        pass

    def render(self):
        pass

    def resize(self):
        self.image = pygame.Surface(
            resize(self.win_base_size, self.size),
            pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, resize(self.win_base_size, self.pos))

    def draw(self):
        self.game.display.blit(self.image, self.rect)

    def __str__(self):
        text = (
            f"UI Element {hex(id(self))}\n"
            f"Size: {self.rect.size}\n"
            f"Topleft: {self.rect.topleft}\n"
            f"Center: {self.rect.center}\n"
            f"Bottomright: {self.rect.bottomright}"
        )
        return get_tui_text_box(text)
