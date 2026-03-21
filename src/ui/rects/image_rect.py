from core.enums import ResizeAxis
from core.settings import COLORS, pygame
from ui.base import UIElement


class UIImage(UIElement):
    def __init__(
        self,
        pos,
        size,
        anchor,
        image,
        do_auto_size=False,
        resize_axis=ResizeAxis.AUTO,
        **kwargs,
    ):
        size = image.size if do_auto_size else size
        super().__init__(
            pos=pos, size=size, anchor=anchor, resize_axis=resize_axis, **kwargs
        )
        self._original_image = image.copy()
        self.image = self._original_image.copy()

    def render(self):
        self.resize()
        self.image.fill(COLORS["clear"])
        resized_image = pygame.transform.smoothscale(
            surface=self._original_image, size=self.image.size
        )
        self.image.blit(resized_image, (0, 0))
