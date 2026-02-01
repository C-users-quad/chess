from core.settings import *
from core.utils import get_tui_text_box

class UIElement:
    """Creates a ui element that displays text in a stylized box"""
    def __init__(self, size, pos, text, anchor="topleft"):
        # initialize basic sprite attributes
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = pygame.Rect(pos, size)
        self.text = text
        setattr(self.rect, anchor, pos)
        self.render_element()

    def render_element(self, bg_color=COLORS['ui-bg'],
    border_color=COLORS['ui-border'], text_color=COLORS['text']):
        # stylize ui element image
        pygame.draw.rect( # draw background color
            self.image, bg_color, self.image.get_rect(), border_radius=ROUNDING)
        pygame.draw.rect( # draw border
            self.image, border_color, self.image.get_rect(), BORDER_WIDTH, ROUNDING)
        # draw text
        text_surf = GameContext.game.font.render(self.text, ANTIALIAS, text_color)
        text_rect = text_surf.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surf, text_rect)

    def draw(self):
        GameContext.game.display.blit(self.image, self.rect)

    def update(self):
        pass

    def __str__(self):
        text = (
            f"UI Element {hex(id(self))}\n"
            f"Size: {self.rect.size}\n"
            f"Topleft: {self.rect.topleft}\n"
            f"Center: {self.rect.center}\n"
            f"Bottomright: {self.rect.bottomright}"
        )
        return get_tui_text_box(text)
