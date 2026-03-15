from core.settings import BASE_HEIGHT, BASE_WIDTH, pygame
from core.utils import get_ui_elem
from core.enums import StateNames
from states.base import GameState
from ui.composites.widget import UIWidget
from ui.rects.colored_rect import UIColoredRect
from ui.rects.text_box import UITextBox
from ui.composites.manager import UIManager
from ui.slider import UISlider
from ui.text import UIText


def slider_widget_child_factory(base: UIColoredRect):
    children = []
    padding = get_ui_elem("padding")

    text = UIText(
        pos=(base.base_size[0] / 2, padding),
        font_height=base.base_size[1] / 2 - padding*1.5,
        anchor="midtop",
        resize_axis=base.resize_axis,
        text="Slider Test",
        text_color="black",
        max_width=base.base_size[0] - padding*2
    )
    children.append(text)

    slider = UISlider(
        pos=(text.base_pos[0], text.base_size[1] + padding*2),
        size=(base.base_size[0] - padding*2, base.base_size[1] / 4),
        anchor="midtop",
        resize_axis=base.resize_axis,
        value=10,
        min_value=0,
        max_value=100
    )
    children.append(slider)

    return children


class SettingsMenu(GameState):
    """menu for game settings"""

    name = StateNames.SETTINGS

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_input(event.key)

    def handle_input(self, key):
        if key == pygame.K_ESCAPE:
            self.game.pop_state()

    def update(self):
        self.ui.update()

    def render(self, force_rendering=False):
        self.ui.render(force_rendering)

    def draw(self):
        self.ui.draw()

    def make_ui(self):
        elements = []

        spacing = get_ui_elem("spacing")

        title = UITextBox(
            pos=(BASE_WIDTH / 2, spacing),
            anchor="midtop",
            text="Settings",
            font_size="title",
            do_auto_size=True,
        )
        elements.append(title)

        slider_widget_base = UIColoredRect(
            pos=(BASE_WIDTH / 2, BASE_HEIGHT / 4),
            size=(BASE_WIDTH / 4, BASE_HEIGHT / 6),
            anchor="midtop",
            color="white",
            resize_axis="width",
            rounding=True
        )
        slider_widget = UIWidget(
            base=slider_widget_base,
            child_factory=lambda: slider_widget_child_factory(slider_widget_base)
        )
        elements.append(slider_widget)

        self.ui = UIManager(elements)
