from core.utils import get_tui_text_box, resize
from ui.base import UIElement
from ui.rects.colored_rect import UIColoredRect


class UIWidget(UIElement):
    """a manager for a composite ui element with a visual base"""

    def __init__(self, base: UIColoredRect, child_factory: callable, **kwargs):
        """
        ui widget maker
        Args:
            base (UIElement):
                the bottom of the widget where all the children are displayed
            child_factory (function):
                a lambda that creates and returns the widgets child elements
        """
        super().__init__(
            pos=base.base_pos,
            size=base.base_size,
            anchor=base.anchor,
            resize_axis=base.resize_axis,
            **kwargs,
        )
        self.base = base
        self.child_factory = child_factory
        self.children = self.child_factory()
        self.render()

    def get_child_relative_rect(self, child):
        """
        positions child relative to the base
        to avoid undefined behavior on window resize
        """
        # remake base and child original rects
        base_base_rect = self.base.get_base_rect()
        base_child_rect = child.get_base_rect()

        # position child rect relative to base rect
        child_rel_topleft = (
            base_child_rect.left - base_base_rect.left,
            base_child_rect.top - base_base_rect.top,
        )
        base_child_rect.topleft = child_rel_topleft

        # scale rect to current window size
        base_child_rect.size = resize(base_child_rect.size, child.resize_axis)
        setattr(
            base_child_rect, child.anchor, resize(child.base_pos, child.resize_axis)
        )

        return base_child_rect

    def update(self):
        for child in self.children:
            self.set_child_screen_rect(child)
            child.update()
        self.dirty = any(child.dirty for child in self.children)

    def set_child_screen_rect(self, child):
        # get the childs rect relative to widget, and widget base rect.
        child_relative_rect = self.get_child_relative_rect(child)
        base_screen_rect = self.base.rect.copy()

        # get the childs position in window space and set rects size
        child_screen_rect = base_screen_rect.move(child_relative_rect.topleft)
        child_screen_rect.size = child_relative_rect.size

        # modify child.rect to new child screen rect
        child.rect = child_screen_rect

    def render(self):
        # should re-render base, then draw children onto base
        self.base.render()
        self.rect = self.base.rect
        for child in self.children:
            child.render()
            child_rect = self.get_child_relative_rect(child)
            self.base.image.blit(child.image, child_rect)

    def draw(self):
        # draw base widget
        self.game.display.blit(self.base.image, self.base.rect)
        # if widget has buttons, draw their highlights on top
        for child in self.children:
            if hasattr(child, "draw_highlight"):
                child.draw_highlight()

    def __str__(self):
        lines = (
            f"UIWidget {hex(id(self))}\n"
            f"Children: {self.children[:2]}...\n"
            f"Base: {self.base}"
        )

        return get_tui_text_box(lines)
