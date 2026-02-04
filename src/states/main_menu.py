from core.settings import *
from states.base import GameState
from core.utils import get_tui_text_box, get_ui_elem
from ui.button import UIButton
from ui.text_box import UITextBox

def make_ui(ui):
    # reset ui and get needed data from game
    ui.clear()
    game = GameContext.game
    win_w, win_h = game.display.get_size()

    # get needed ui elements
    spacing = get_ui_elem('spacing')
    border_width = get_ui_elem('border-width')
    padding = get_ui_elem('padding')
    title_font_size = get_ui_elem('title')
    subtitle_font_size = get_ui_elem('subtitle')

    # make title
    title = UITextBox((win_w/2, spacing),
        "midtop", "CHESS", title_font_size, True)
    ui.append(title)

    # make buttons
    menu_button_size = (
        win_w/3 - 2*spacing,
        subtitle_font_size + border_width * 2 + padding * 2
    )
    play_game = UIButton((spacing, win_h - spacing),
        "bottomleft", "Play Game", subtitle_font_size,
        lambda: print(play_game.__str__()), size=menu_button_size)
    ui.append(play_game)

    settings = UIButton((win_w / 2, win_h - spacing),
        "midbottom", "Settings", subtitle_font_size,
        lambda: print(settings.__str__()), size=menu_button_size)
    ui.append(settings)

    quit_game = UIButton((win_w - spacing, win_h - spacing),
        "bottomright", "Quit Game", subtitle_font_size,
        lambda: print(quit_game.__str__()), size=menu_button_size)
    ui.append(quit_game)

class MainMenu(GameState):
    def __init__(self):
        super().__init__()
        self.draw_below = True
        make_ui(self.ui)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.power_off()
            if event.type == pygame.VIDEORESIZE:
                make_ui(self.ui)

    def update(self):
        for element in self.ui:
            element.update()
        print(self.game)

    def draw(self):
        for element in self.ui:
            element.draw()
