from ui.rects.text_box import UITextBox
from ui.buttons.base import UIButton


class UITextButton(UIButton, UITextBox):
    """button thats composed of a stylized rectangle with text"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
