from core.enums import StateNames
from core.settings import *
from states.base import GameState
from core.utils import get_tui_text_box, get_ui_elem
from ui.buttons.text_button import UITextButton
from ui.rects.text_box import UITextBox
from ui.rects.colored_rect import UIColoredRect

def make_ui(ui):
    # reset ui and get needed data from game
    ui.clear()
    game = GameContext.game

    # get needed ui elements
    spacing = get_ui_elem('spacing')
    border_width = get_ui_elem('border-width')
    padding = get_ui_elem('padding')
    subtitle_font_size = get_ui_elem('subtitle')
    sidebar_width = get_ui_elem('sidebar-width')

    # make title
    title = UITextBox(
        pos=(BASE_WIDTH/2, spacing),
        anchor="midtop",
        text="CHESS",
        font_size='title',
        do_auto_size=True
    )
    ui.append(title)

    # make sidebars
    sidebar_size = (sidebar_width, BASE_HEIGHT)
    bar1 = UIColoredRect(
        pos=(0,0),
        size=sidebar_size,
        anchor="topleft",
        color=COLORS['white-square']
    )
    ui.append(bar1)
    bar2 = UIColoredRect(
        pos=(BASE_WIDTH, 0),
        size=sidebar_size,
        anchor="topright",
        color=COLORS['black-square']
    )
    ui.append(bar2)

    # make buttons
    menu_button_size = (
        (BASE_WIDTH - 4*spacing - 2*sidebar_width) / 3,
        subtitle_font_size + border_width * 2 + padding * 2
    )
    play_game = UITextButton(
        pos=(spacing + sidebar_width, BASE_HEIGHT - spacing),
        anchor="bottomleft",
        text="Play Game",
        font_size='subtitle',
        click_action=game.pop_state,
        size=menu_button_size
    )
    ui.append(play_game)

    settings = UITextButton(
        pos=(BASE_WIDTH / 2, BASE_HEIGHT - spacing),
        anchor="midbottom",
        text="Settings",
        font_size='subtitle',
        click_action=game.push_state,
        click_action_args=('settings',),
        size=menu_button_size
    )
    ui.append(settings)

    quit_game = UITextButton(
        pos=(BASE_WIDTH - spacing - sidebar_width, BASE_HEIGHT - spacing),
        anchor="bottomright",
        text="Quit Game",
        font_size='subtitle',
        click_action=game.power_off,
        size=menu_button_size
    )
    ui.append(quit_game)

class MainMenu(GameState):
    """main menu with important buttons"""
    names = StateNames.MAIN_MENU
    def __init__(self):
        super().__init__()
        make_ui(self.ui)
