from core.settings import *
from core.utils import get_tui_text_box, resize

class UIElement:
    """parent ui class that stores a surface and rect combo with a size and pos."""
    def __init__(self, pos=(0,0), size=(0,0), anchor="topleft",
                 resize_axis='auto', **kwargs):
        # initialize basic sprite attributes
        super().__init__(**kwargs)
        self.size = size
        self.pos = pos
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = pygame.Rect(pos, size)
        self.anchor = anchor
        self.resize_axis = resize_axis
        setattr(self.rect, self.anchor, self.pos)

    @property
    def game(self):
        return GameContext.game

    def update(self):
        pass

    def render(self):
        pass

    def resize(self, size_override=None):
        new_size = size_override if size_override else \
            resize(self.size, axis=self.resize_axis)
        new_pos = resize(self.pos)
        self.image = pygame.Surface(new_size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, new_pos)

    def draw(self):
        self.game.display.blit(self.image, self.rect)

    def __str__(self):
        text = (
            f"UI Element {hex(id(self))}\n"
            f"Size: {self.rect.size}\n"
            f"Topleft: {self.rect.topleft}\n"
            f"Center: {self.rect.center}\n"
            f"Bottomright: {self.rect.bottomright}\n"
            f"Resizing axis: {self.resize_axis}"
        )
        return get_tui_text_box(text)
