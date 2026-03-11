from ui.base import UIElement


class UISlider(UIElement):
    def __init__(
        self, pos, size, anchor, resize_axis, value, min_value, max_value, **kwargs
    ):
        super().__init__(
            pos=pos, size=size, anchor=anchor, resize_axis=resize_axis, **kwargs
        )
        self.min_value = min_value
        self.max_value = max_value
        self.curr_value = value

    def get_slider_x(self):
        max_x, min_x = self.rect.right, self.rect.left

        value_range = self.max_value - self.min_value
        percent_range = self.curr_value / value_range

        slider_range = max_x - min_x
        slider_x = (slider_range * percent_range) + min_x

        return slider_x

    def render(self):
        pass
