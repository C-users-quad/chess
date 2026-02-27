from core.settings import *
from core.utils import get_ui_elem, scale
from ui.buttons.base import UIButton
from ui.rects.image_rect import UIImage

class UIImageButton(UIButton, UIImage):
    """button thats composed of an image and optional background color"""
    def __init__(self, pos, anchor, click_action,
                 image, click_action_args=None, do_auto_size=False, size=(0,0),
                 resize_axis='auto', **kwargs):
        super().__init__(
            pos=pos,
            size=size,
            anchor=anchor,
            do_auto_size=do_auto_size,
            click_action=click_action,
            click_action_args=click_action_args,
            image=image,
            resize_axis=resize_axis,
            **kwargs
        )
