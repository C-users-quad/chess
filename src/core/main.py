from core.settings import *
from core.utils import get_tui_text_box, asset_path
from states.main_menu import MainMenu
from states.settings import SettingsMenu
from states.chess import Chess
from chess.board import Board

class Game:
    """Central game object containing essential game components"""
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.fonts = {}
        """dict of font size (int) : font (pygame.Font)"""
        self.dt = 0
        self.states = {
            'main-menu': lambda: MainMenu(),
            'chess': lambda: Chess(),
            'settings': lambda: SettingsMenu()
        }
        """
        dict of every state, used to push states to state stack
        current keys:
        ```
        'main-menu' - the main menu
        'chess' - the game itself
        'settings' - the settings menu
        ```
        """
        self.state_stack = []
        self.on = True
        self.board = None
        self.dim_surf = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.dim_surf.fill(COLORS['state-dim'])
        self.dim_surf.set_alpha(STATE_DIM_ALPHA)
        self.dim_rect = self.dim_surf.get_rect()
        self.prev_window_size = self.display.get_size()

    def get_font(self, size):
        if size not in self.fonts:
            self.fonts[size] = pygame.Font(
                asset_path(join('assets', 'fonts', 'MerriweatherSans-Medium.ttf')),
                size)
        return self.fonts[size]

    def push_state(self, state):
        self.state_stack.append(self.states[state]())

    def pop_state(self):
        self.state_stack.pop()

    def swap_state(self, state):
        """swaps the top state with state specified by argument"""
        self.state_stack[-1] = self.states[state]()

    def power_off(self):
        self.on = False

    def window_resized(self):
        return self.prev_window_size != self.display.get_size()

    def update(self):
        self.prev_window_size = self.display.get_size()
        self.dt = self.clock.tick(FPS) / 1000

    def __str__(self):
        text = (
            f"Game object {hex(id(self))}\n"
            f"Display size: {self.display.get_size()}\n"
            f"State stack: {self.state_stack[:]}"
        )

        return get_tui_text_box(text)

def main():
    # create game context
    game = GameContext.game = Game()
    game.board = Board()

    # push initial states
    game.push_state('chess')
    game.push_state('main-menu')

    while game.on:
        # update game context
        game.update()

        # update top state
        top_state = game.state_stack[-1]
        top_state.handle_events(pygame.event.get())
        top_state.update()

        # draw game
        game.display.fill(COLORS['clear'])
        for state in game.state_stack[0:-1]:
            if state.draw_below:
                state.draw(force_rendering=True)
                state.draw_dim()
        top_state.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
