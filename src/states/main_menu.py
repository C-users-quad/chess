from core.settings import *
from states.base import GameState
from core.utils import get_tui_text_box
from ui.button import UIButton
from ui.text_box import UITextBox

def make_ui(ui):
    # reset ui and get needed data from game
    ui.clear()
    game = GameContext.game
    win_w, win_h = game.display.get_size()

    # make title
    title = UITextBox((win_w/2, SPACING), (200, 75),
        "midtop", "CHESS", FONT_SIZES['title'])
    ui.append(title)

    # make buttons
    menu_button_size = (win_w/3 - 2*SPACING, 75)
    play_game = UIButton((SPACING, win_h - SPACING), menu_button_size,
        "bottomleft", "Play Game", FONT_SIZES['subtitle'],
        lambda: print(play_game.__str__()))
    ui.append(play_game)

    settings = UIButton((win_w / 2, win_h - SPACING), menu_button_size,
        "midbottom", "Settings", FONT_SIZES['subtitle'],
        lambda: print(settings.__str__()))
    ui.append(settings)

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

    def draw(self):
        for element in self.ui:
            element.draw()
