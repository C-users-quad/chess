from core.settings import COLORS, TEXT_RESIZE_AXIS, pygame, ANTIALIAS
from core.utils import scale
from ui.base import UIElement


class UIText(UIElement):
    """draws text with a specified font height at a specified position"""

    def __init__(
        self,
        font_height: int,
        text: str,
        text_color,
        max_width=None,
        **kwargs,
    ):
        super().__init__(size=(0, 0), **kwargs)
        self.font_height = font_height
        # compute base size
        base_font_size = (
            self.game.get_font(font_height).render(text, ANTIALIAS, text_color).size
        )
        self.base_size = (
            min(base_font_size[0], max_width) if max_width else base_font_size[0],
            font_height,
        )
        self.text = text
        self.text_color = text_color

    @property
    def font(self) -> pygame.Font:
        return self.game.get_font(scale(self.font_height, axis=TEXT_RESIZE_AXIS))

    def render(self):
        self.resize()
        self.image.fill(COLORS["clear"])
        text_surf = self.font.render(self.text, ANTIALIAS, self.text_color)
        text_surf = pygame.transform.smoothscale(text_surf, self.image.get_size())
        self.image.blit(text_surf)
