from core.enums import AnchorPoints, StateNames
from core.settings import BASE_HEIGHT, BASE_WIDTH, COLORS
from states.base import GameState
from core.utils import get_ui_elem
from ui.buttons.text_button import UITextButton
from ui.rects.text_box import UITextBox
from ui.rects.colored_rect import UIColoredRect
from ui.composites.manager import UIManager


class MainMenu(GameState):
    """main menu with important buttons"""

    name = StateNames.MAIN_MENU

    def update(self):
        self.ui.update()

    def render(self, force_rendering=False):
        self.ui.render(force_rendering)

    def draw(self):
        self.ui.draw()

    def make_ui(self):
        elements = []

        # get needed ui elements
        spacing = get_ui_elem("spacing")
        border_width = get_ui_elem("border-width")
        padding = get_ui_elem("padding")
        subtitle_font_size = get_ui_elem("subtitle")
        sidebar_width = get_ui_elem("sidebar-width")

        # make title
        title = UITextBox(
            pos=(BASE_WIDTH / 2, spacing),
            anchor=AnchorPoints.MIDTOP,
            text="CHESS",
            font_size="title",
            do_auto_size=True,
        )
        elements.append(title)

        # make sidebars
        sidebar_size = (sidebar_width, BASE_HEIGHT)
        bar1 = UIColoredRect(
            pos=(0, 0),
            size=sidebar_size,
            anchor=AnchorPoints.TOPLEFT,
            color=COLORS["white-square"],
        )
        elements.append(bar1)
        bar2 = UIColoredRect(
            pos=(BASE_WIDTH, 0),
            size=sidebar_size,
            anchor=AnchorPoints.TOPRIGHT,
            color=COLORS["black-square"],
        )
        elements.append(bar2)

        # make buttons
        menu_button_size = (
            (BASE_WIDTH - 4 * spacing - 2 * sidebar_width) / 3,
            subtitle_font_size + border_width * 2 + padding * 2,
        )
        # chess is always below main menu.
        play_game = UITextButton(
            pos=(spacing + sidebar_width, BASE_HEIGHT - spacing),
            anchor="bottomleft",
            text="Play Game",
            font_size="subtitle",
            click_action=self.game.pop_state,
            size=menu_button_size,
        )
        elements.append(play_game)

        settings = UITextButton(
            pos=(BASE_WIDTH / 2, BASE_HEIGHT - spacing),
            anchor=AnchorPoints.MIDBOTTOM,
            text="Settings",
            font_size="subtitle",
            click_action=self.game.push_state,
            click_action_args=(StateNames.SETTINGS,),
            size=menu_button_size,
        )
        elements.append(settings)

        quit_game = UITextButton(
            pos=(BASE_WIDTH - spacing - sidebar_width, BASE_HEIGHT - spacing),
            anchor="bottomright",
            text="Quit Game",
            font_size="subtitle",
            click_action=self.game.power_off,
            size=menu_button_size,
        )
        elements.append(quit_game)

        self.ui = UIManager(elements, self)
