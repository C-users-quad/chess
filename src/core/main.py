from core.settings import (
    pygame,
    WINDOW_SIZE,
    COLORS,
    STATE_DIM_ALPHA,
    join,
    FPS,
    GameContext,
    sys,
)
from core.utils import get_tui_text_box, asset_path
from states.main_menu import MainMenu
from states.settings_menu import SettingsMenu
from states.chess import Chess
from states.promotion import Promotion
from states.new_game import NewGame
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
            "main-menu": MainMenu,
            "chess": Chess,
            "settings": SettingsMenu,
            "promotion": Promotion,
            "new-game": NewGame,
        }
        """
        dict of every state, used to push states to state stack
        current keys:
        ```
        'main-menu' - the main menu
        'chess' - the game itself
        'settings' - the settings menu
        'promotion' - the pawn promotion piece selection menu
        ```
        """
        self.state_stack = []
        self.on = True
        self.prev_window_size = self.display.get_size()
        self.debug = False
        self.render_dim()

    def render_dim(self):
        self.dim_surf = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        self.dim_surf.fill(COLORS["state-dim"])
        self.dim_surf.set_alpha(STATE_DIM_ALPHA)
        self.dim_rect = self.dim_surf.get_rect()

    def get_font(self, size):
        """gets a pygame.Font object given a numeric font size"""
        size = int(size)  # type safety
        if size not in self.fonts:
            self.fonts[size] = pygame.Font(
                filename=asset_path(
                    join("assets", "fonts", "MerriweatherSans-Medium.ttf")
                ),
                size=size,
            )
        return self.fonts[size]

    def push_state(self, state, args=None):
        if not args:
            state = self.states[state]()
        else:
            state = self.states[state](*args)
        self.state_stack.append(state)

        return state

    def pop_state(self):
        self.state_stack.pop()

    def power_off(self):
        self.on = False

    def window_resized(self):
        return self.prev_window_size != self.display.get_size()

    def detect_debug_toggle(self):
        """
        toggles debug mode if ctrl+alt+shift+d is pressed
        """
        keys = pygame.key.get_just_pressed()
        mods = pygame.key.get_mods()
        if (
            mods & pygame.KMOD_CTRL
            and mods & pygame.KMOD_ALT
            and mods & pygame.KMOD_SHIFT
            and keys[pygame.K_d]
        ):
            self.debug = not self.debug

    def update(self):
        self.prev_window_size = self.display.get_size()
        self.dt = self.clock.tick(FPS) / 1000
        self.detect_debug_toggle()

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

    # push initial states
    game.push_state("chess", (Board(),))
    game.push_state("main-menu")

    while game.on:
        # update game context
        game.update()

        # update top state
        top_state = game.state_stack[-1]
        top_state.handle_events(pygame.event.get())
        top_state.update()

        # draw game
        game.display.fill(COLORS["clear"])
        for state in game.state_stack[0:-1]:
            if state.draw_below:
                state.render(force_rendering=True)
                state.draw()
                state.draw_dim()
        top_state.render()
        top_state.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
