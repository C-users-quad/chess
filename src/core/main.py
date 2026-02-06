from core.settings import *
from core.utils import get_tui_text_box, asset_path
from states.main_menu import MainMenu
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
            'chess': lambda: Chess()
        }
        """
        dict of every state, used to push states to state stack
        current keys:
        ```
        'main-menu' - the main menu
        'chess' - the game itself
        ```
        """
        self.state_stack = []
        self.on = True
        self.board = None

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

    def __str__(self):
        text = (
            f"Game object {hex(id(self))}\n"
            f"Display size: {self.display.get_size()}\n"
            f"State stack: {self.state_stack[:]}"
        )

        return get_tui_text_box(text)

# the pattern:
# you have a state stack, and in it are objects that represent game states.
# for example, for the game you have the game state class and you import it here
# and here in the main menu class when the player presses the button that opens the
# game, you would append the game object to the state stack and yea
def main():
    # create game context
    game = GameContext.game = Game()
    game.board = Board()
    # push initial state
    game.push_state('chess')
    game.push_state('main-menu')

    while game.on:
        # get delta time
        game.dt = game.clock.tick(FPS) / 1000

        # update top state
        top_state = game.state_stack[-1]
        top_state.handle_events()
        top_state.update()

        # draw game
        game.display.fill(COLORS['clear'])
        for state in game.state_stack[0:len(game.state_stack)-1]:
            if state.draw_below: state.draw()
        top_state.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
