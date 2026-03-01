from ui.rects.text_box import UITextBox
from ui.buttons.base import UIButton


class UITextButton(UIButton, UITextBox):
    """button thats composed of a stylized rectangle with text"""

    def __init__(
        self,
        pos,
        anchor,
        text,
        font_size,
        click_action,
        click_action_args=None,
        do_auto_size=False,
        size=(0, 0),
        resize_axis="auto",
        **kwargs,
    ):
        super().__init__(
            pos=pos,
            anchor=anchor,
            text=text,
            font_size=font_size,
            click_action=click_action,
            do_auto_size=do_auto_size,
            click_action_args=click_action_args,
            size=size,
            resize_axis=resize_axis,
            **kwargs,
        )
