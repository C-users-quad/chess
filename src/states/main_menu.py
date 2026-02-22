from core.settings import *
from states.base import GameState
from core.utils import get_tui_text_box, get_ui_elem
from ui.button import UIButton
from ui.text_box import UITextBox
from ui.base import UIElement
from ui.colored_rect import UIColoredRect

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
    title = UITextBox((BASE_WIDTH/2, spacing),
        "midtop", "CHESS", 'title', True)
    ui.append(title)

    # make sidebars
    sidebar_size = (sidebar_width, BASE_HEIGHT)
    bar1 = UIColoredRect(
        (0,0), sidebar_size, "topleft", COLORS['white-square'])
    ui.append(bar1)
    bar2 = UIColoredRect(
        (BASE_WIDTH, 0), sidebar_size, "topright", COLORS['black-square'])
    ui.append(bar2)

    # make buttons
    menu_button_size = (
        (BASE_WIDTH - 4*spacing - 2*sidebar_width) / 3,
        subtitle_font_size + border_width * 2 + padding * 2
    )
    play_game = UIButton((spacing + sidebar_width, BASE_HEIGHT - spacing),
        "bottomleft", "Play Game", 'subtitle',
        lambda: game.pop_state(), size=menu_button_size)
    ui.append(play_game)

    settings = UIButton((BASE_WIDTH / 2, BASE_HEIGHT - spacing),
        "midbottom", "Settings", 'subtitle',
        lambda: game.push_state('settings'), size=menu_button_size)
    ui.append(settings)

    quit_game = UIButton((BASE_WIDTH - spacing - sidebar_width, BASE_HEIGHT - spacing),
        "bottomright", "Quit Game", 'subtitle',
        lambda: game.power_off(), size=menu_button_size)
    ui.append(quit_game)

class MainMenu(GameState):
    def __init__(self):
        super().__init__()
        make_ui(self.ui)

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        for element in self.ui:
            element.update()

    def render(self, force):
        if not force and not self.game.window_resized():
            return
        for element in self.ui:
            element.render()

    def draw(self, force_rendering=False):
        self.render(force_rendering)
        for element in self.ui:
            element.draw()
