from core.settings import (
    BASE_HEIGHT,
    BASE_WIDTH,
    VariableSettings,
    pygame,
    MIN_VOLUME,
    MAX_VOLUME,
)
from core.utils import get_ui_elem
from core.enums import AnchorPoints, ResizeAxis, StateNames
from states.base import GameState
from ui.misc.checkbox import UICheckbox
from ui.composites.widget import UIWidget
from ui.rects.colored_rect import UIColoredRect
from ui.rects.text_box import UITextBox
from ui.composites.manager import UIManager
from ui.misc.slider import UISlider
from ui.misc.text import UIText


def sfx_volume_widget_child_factory(base: UIColoredRect):
    children = []
    padding = get_ui_elem("padding")

    text = UIText(
        pos=(base.base_size[0] / 2, padding),
        font_height=base.base_size[1] / 2 - padding * 1.5,
        anchor=AnchorPoints.MIDTOP,
        resize_axis=base.resize_axis,
        text="SFX Volume",
        text_color="black",
        max_width=base.base_size[0] - padding * 2,
    )
    children.append(text)

    slider = UISlider(
        pos=(text.base_pos[0], text.base_size[1] + padding * 2),
        size=(base.base_size[0] - padding * 2, base.base_size[1] / 4),
        anchor=AnchorPoints.MIDTOP,
        resize_axis=base.resize_axis,
        value=VariableSettings.sfx_volume,
        min_value=MIN_VOLUME,
        max_value=MAX_VOLUME,
        on_change=VariableSettings.setter("sfx_volume"),
    )
    children.append(slider)

    return children


def flip_board_widget_child_factory(base: UIColoredRect):
    children = []
    base_size = base.base_size
    padding = get_ui_elem("padding")

    text = UIText(
        pos=(base_size[0] / 2, padding),
        font_height=base_size[1] / 2 - padding * 1.5,
        anchor=AnchorPoints.MIDTOP,
        resize_axis=base.resize_axis,
        text="Flip Board",
        text_color="black",
        max_width=base_size[0] - padding * 2,
    )
    children.append(text)

    checkbox = UICheckbox(
        value=VariableSettings.flip_board,
        change_value=VariableSettings.setter("flip_board"),
        pos=(base_size[0] / 2, base_size[1] / 2 + padding * 0.5),
        anchor=AnchorPoints.MIDTOP,
        side_length=base_size[1] / 2 - padding * 1.5,
        resize_axis=base.resize_axis,
    )
    children.append(checkbox)

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
        settings_widget_size = (BASE_WIDTH / 3.75, BASE_HEIGHT / 5.5)

        title = UITextBox(
            pos=(BASE_WIDTH / 2, spacing),
            anchor=AnchorPoints.MIDTOP,
            text="Settings",
            font_size="title",
            do_auto_size=True,
        )
        elements.append(title)

        sfx_volume_widget_base = UIColoredRect(
            pos=(BASE_WIDTH / 2, BASE_HEIGHT / 4),
            size=settings_widget_size,
            anchor=AnchorPoints.MIDTOP,
            color="white",
            resize_axis=ResizeAxis.HEIGHT,
            rounding=True,
        )
        sfx_volume_widget = UIWidget(
            base=sfx_volume_widget_base,
            child_factory=lambda: sfx_volume_widget_child_factory(
                sfx_volume_widget_base
            ),
        )
        elements.append(sfx_volume_widget)

        prev_widget_rect = sfx_volume_widget_base.get_base_rect()
        flip_board_widget_base = UIColoredRect(
            pos=(prev_widget_rect.centerx, prev_widget_rect.bottom + spacing),
            size=settings_widget_size,
            anchor=AnchorPoints.MIDTOP,
            color="white",
            resize_axis=ResizeAxis.HEIGHT,
            rounding=True,
        )
        flip_board_widget = UIWidget(
            base=flip_board_widget_base,
            child_factory=lambda: flip_board_widget_child_factory(
                flip_board_widget_base
            ),
        )
        elements.append(flip_board_widget)

        self.ui.elements = elements
