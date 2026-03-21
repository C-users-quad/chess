from core.enums import AnchorPoints, ResizeAxis
from core.settings import GameContext, pygame, TYPE_CHECKING
from core.utils import get_tui_text_box, resize

if TYPE_CHECKING:
    from ui.composites.manager import UIManager


class UIElement:
    """parent ui class that stores a surface and rect combo with a size and pos."""

    def __init__(
        self,
        pos=(0, 0),
        size=(0, 0),
        anchor=AnchorPoints.TOPLEFT,
        resize_axis=ResizeAxis.AUTO,
        z_index=0,
        draw_below=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.base_size = size
        self.base_pos = pos
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.anchor = anchor
        self.resize_axis = resize_axis
        self.rect = self.get_base_rect()
        self.z_index = z_index
        self.draw_below = draw_below
        """determines if this ui element is drawn when it isnt in the top state"""
        self.manager: UIManager = None
        """the manager for this element. should be set in uimanager constructor."""
        self.dirty = True
        """used for lazily updating """

    @property
    def game(self):
        return GameContext.game

    @property
    def anchored_pos(self):
        """
        returns the screen-relative position on the rect located at the anchor point
        """
        return getattr(self.rect, self.anchor)

    def register_highlight_draw(self):
        """
        if this element is highlightable, this should draw a highlight in absolute
        window coordinates. should be drawn with a z-index of self.z_index + 1.
        """
        pass

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
            if size_override is not None
            else resize(self.base_size, axis=self.resize_axis)
        )
        new_pos = resize(self.base_pos)
        self.image = pygame.Surface(new_size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, new_pos)

    def register_draw_call(self):
        draw_call = lambda: self.game.display.blit(self.image, self.rect)
        self.manager.register_draw_call(self.z_index, draw_call)

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
