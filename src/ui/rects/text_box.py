from core.enums import ResizeAxis
from core.settings import (
    ANTIALIAS,
    COLORS,
    TEXT_SCALE_AXIS,
    MIN_UI_SIZE,
    pygame,
)
from core.utils import get_ui_elem, resize, scale
from ui.base import UIElement


class UITextBox(UIElement):
    """a stylized rectangle with text"""

    def __init__(
        self,
        text,
        font_size: str,
        do_auto_size=False,
        **kwargs,
    ):
        """
        note: font size should be a key for SIZE_RATIOS
        dict which corresponds to a font size or "auto"
        """
        self.text = text
        self.font_size = font_size
        self.do_auto_size = do_auto_size
        super().__init__(**kwargs)
        if do_auto_size:
            self.auto_size()
        self.render()

    @property
    def font(self):
        # if auto, get font with height that fits perfectly into text rect
        if self.font_size == ResizeAxis.AUTO:
            # get needed ui elements
            border_width = scale(get_ui_elem("border-width"), axis=ResizeAxis.MIN)

            # compute font height from current button size
            btn_height = resize(self.size, self.resize_axis)[1]
            font_height = btn_height - border_width * 2

            return self.game.get_font(font_height)

        return self.game.get_font(
            scale(get_ui_elem(self.font_size), axis=TEXT_SCALE_AXIS)
        )

    def auto_size(self):
        """makes it so that the size is snug around the text"""
        # get needed ui elements
        border_width = scale(get_ui_elem("border-width"), axis=ResizeAxis.MIN)
        padding = scale(get_ui_elem("padding"), axis=ResizeAxis.MIN)

        text_width, text_height = self.font.render(self.text, ANTIALIAS, (0, 0, 0)).size
        width = text_width + 2 * border_width + 2 * padding
        height = text_height + 2 * border_width + 2 * padding
        self.size = (width, height)
        self.resize(self.size)

    def render(
        self,
        bg_color=COLORS["ui-bg"],
        border_color=COLORS["ui-border"],
        text_color=COLORS["text"],
    ):
        self.image.fill(COLORS["clear"])

        # get needed ui elements
        rounding = scale(get_ui_elem("rounding"), axis=ResizeAxis.MIN)
        border_width = scale(get_ui_elem("border-width"), axis=ResizeAxis.MIN)
        padding = scale(get_ui_elem("padding"), axis=ResizeAxis.HEIGHT)

        # resize sprite
        if self.do_auto_size:
            self.auto_size()
        else:
            self.resize()

        # stylize ui element image
        image_rect = self.image.get_rect()
        pygame.draw.rect(  # draw background color
            self.image, bg_color, image_rect, border_radius=rounding
        )
        pygame.draw.rect(  # draw border
            self.image, border_color, image_rect, border_width, rounding
        )

        # draw text
        if not self.text:
            return

        text_surf = self.font.render(self.text, ANTIALIAS, text_color)
        text_max_width = max(
            MIN_UI_SIZE, image_rect.width - 2 * border_width - 2 * padding
        )
        text_max_height = max(MIN_UI_SIZE, image_rect.height - 2 * border_width)

        if text_surf.width > text_max_width or text_surf.height > text_max_height:
            new_text_width = min(text_surf.width, text_max_width)
            new_text_height = min(text_surf.height, text_max_height)
            text_surf = pygame.transform.smoothscale(
                text_surf, (new_text_width, new_text_height)
            )

        text_rect = text_surf.get_rect(center=image_rect.center)
        self.image.blit(text_surf, text_rect)
