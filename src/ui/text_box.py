from core.settings import *
from core.utils import get_tui_text_box, get_ui_elem, resize, scale
from ui.base import UIElement

class UITextBox(UIElement):
    def __init__(self, pos, anchor, text, font_size: str,
            do_auto_size=False, size=(0,0), **kwargs):
        """
        note: font size should be a key for SIZE_RATIOS
        dict which corresponds to a font size
        """
        self.text = text
        self.font_size = font_size
        self.do_auto_size = do_auto_size
        super().__init__(pos=pos, size=size, anchor=anchor, **kwargs)
        if do_auto_size: self.auto_size()
        self.render()

    @property
    def font(self):
        return self.game.get_font(scale(get_ui_elem(self.font_size), axis='height'))

    def auto_size(self):
        """makes it so that the size is snug around the text"""
        # get needed ui elements
        border_width = scale(get_ui_elem('border-width'), axis=UI_SCALE_AXIS)
        padding = scale(get_ui_elem('padding'), axis=UI_SCALE_AXIS)

        text_width, text_height = self.font.render(
            self.text, ANTIALIAS, (0,0,0)).size
        width = text_width + 2*border_width + 2*padding
        height = text_height + 2*border_width + 2*padding
        self.size = (width, height)
        self.resize(self.size)

    def render(self, bg_color=COLORS['ui-bg'],
            border_color=COLORS['ui-border'], text_color=COLORS['text']):
        # get needed ui elements
        rounding = scale(get_ui_elem('rounding'), axis=UI_SCALE_AXIS)
        border_width = scale(get_ui_elem('border-width'), axis=UI_SCALE_AXIS)
        padding = scale(get_ui_elem('padding'), axis=UI_SCALE_AXIS)

        # resize sprite
        if self.do_auto_size:
            self.auto_size()
        else:
            self.resize()

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
