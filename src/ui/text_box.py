from core.settings import *
from core.utils import get_tui_text_box, get_ui_elem
from ui.base import UIElement

class UITextBox(UIElement):
    def __init__(self, pos, anchor, text, font_size,
            auto_size=False, size=(0,0), **kwargs):
        self.text = text
        self.font = GameContext.game.get_font(font_size)
        self.font_size = font_size
        if auto_size:
            super().__init__(pos, self.get_auto_size(), anchor, **kwargs)
        else:
            super().__init__(pos, size, anchor, **kwargs)
        self.render_element()

    def get_auto_size(self):
        # get needed ui elements
        border_width = get_ui_elem('border-width')
        padding = get_ui_elem('padding')

        text_width, text_height = self.font.render(
            self.text, ANTIALIAS, (000,000,000)).size
        width = text_width + 2*border_width + 2*padding
        height = text_height + 2*border_width + 2*padding
        return (width, height)

    def render_element(self, bg_color=COLORS['ui-bg'],
            border_color=COLORS['ui-border'], text_color=COLORS['text']):
        # get needed ui elements
        rounding = get_ui_elem('rounding')
        border_width = get_ui_elem('border-width')
        padding = get_ui_elem('padding')

        # stylize ui element image
        image_rect = self.image.get_rect()
        pygame.draw.rect( # draw background color
            self.image, bg_color, image_rect, border_radius=rounding)
        pygame.draw.rect( # draw border
            self.image, border_color, image_rect, border_width, rounding)
        # draw text
        if not self.text:
            return
        text_surf = self.font.render(
            self.text, ANTIALIAS, text_color)
        text_max_width = image_rect.width - 2*border_width - 2*padding
        if text_surf.width > text_max_width:
            text_surf = pygame.transform.smoothscale(
                text_surf, (text_max_width, text_surf.height))
        text_rect = text_surf.get_rect(center=image_rect.center)
        self.image.blit(text_surf, text_rect)

    def __str__(self):
        text = (
            f"Text Box {hex(id(self))}\n"
            f"Size: {self.rect.size}\n"
            f"Topleft: {self.rect.topleft}\n"
            f"Center: {self.rect.center}\n"
            f"Bottomright: {self.rect.bottomright}\n"
            f"Text: {self.text}\n"
            f"Font size: {self.font_size}"
        )
        return get_tui_text_box(text)
