from ui.buttons.base import UIButton
from ui.rects.image_rect import UIImage


class UIImageButton(UIButton, UIImage):
    """button thats composed of an image"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
