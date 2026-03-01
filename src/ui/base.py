from core.settings import GameContext, pygame
from core.utils import get_tui_text_box, resize


class UIElement:
    """parent ui class that stores a surface and rect combo with a size and pos."""

    def __init__(
        self, pos=(0, 0), size=(0, 0), anchor="topleft", resize_axis="auto", **kwargs
    ):
        super().__init__(**kwargs)
        self.base_size = size
        self.base_pos = pos
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.anchor = anchor
        self.resize_axis = resize_axis
        self.rect = self.get_base_rect()

    @property
    def game(self):
        return GameContext.game

    def update(self):
        pass

    def render(self):
        pass

    def get_base_rect(self):
        base_rect = pygame.Rect(self.base_pos, self.base_size)
        setattr(base_rect, self.anchor, self.base_pos)

        return base_rect

    def resize(self, size_override=None):
        new_size = (
            size_override
            if size_override
            else resize(self.base_size, axis=self.resize_axis)
        )
        new_pos = resize(self.base_pos)
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
            f"Resizing axis: {self.resize_axis}\n"
            f"Base pos: {self.base_pos}\n"
            f"Base size: {self.base_size}"
        )
        return get_tui_text_box(text)
