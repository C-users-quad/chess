from core.draw import DrawingManager
from core.settings import (
    pygame,
    BASE_WIDTH,
    BASE_HEIGHT,
    COLORS,
    STATE_DIM_ALPHA,
    FONT_PATH,
    GameContext,
    sys,
    VariableSettings,
    TYPE_CHECKING,
)
from core.utils import get_tui_text_box, asset_path
from core.enums import StateNames
from states.main_menu import MainMenu
from states.settings_menu import SettingsMenu
from states.chess import Chess
from states.promotion import Promotion
from states.new_game import NewGame

if TYPE_CHECKING:
    from states.base import GameState


class Game:
    """Central game object containing essential game components"""

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(
            (BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE
        )
        self.clock = pygame.time.Clock()
        self.fonts = {}
        """dict of font size (int) : font (pygame.Font)"""
        self.dt = 0
        """time between frames in seconds"""
        self.states = {
            StateNames.MAIN_MENU: MainMenu,
            StateNames.CHESS: Chess,
            StateNames.SETTINGS: SettingsMenu,
            StateNames.PROMOTION: Promotion,
            StateNames.NEW_GAME: NewGame,
        }
        """
        dict of every state, used to push states to state stack

        key: StateNames.[some state name] -> value: state class
        """
        self.state_stack: list[GameState] = []
        self.on = True
        self.prev_window_size = self.display.get_size()
        self.debug = False
        self.drawing_manager = DrawingManager()
        self.render_dim()

    def initialize_state_stack(self):
        self.push_state(StateNames.CHESS)
        self.push_state(StateNames.MAIN_MENU)

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
                filename=asset_path(FONT_PATH),
                size=size,
            )
        return self.fonts[size]

    def get_state(self, name: StateNames):
        state_type = self.states.get(name)
        for state in self.state_stack:
            if isinstance(state, state_type):
                return state

    def push_state(self, state, args=None):
        if args is None:
            state = self.states[state]()
        else:
            state = self.states[state](*args)
        self.state_stack.append(state)

        return state

    def pop_state(self):
        return self.state_stack.pop()

    def power_off(self):
        self.on = False

    def window_resized(self):
        return self.prev_window_size != self.display.get_size()

    def mouse_moved(self):
        return self.prev_mouse_pos != pygame.mouse.get_pos()

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
        self.prev_mouse_pos = pygame.mouse.get_pos()
        self.dt = self.clock.tick(VariableSettings.fps) / 1000
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
    game.initialize_state_stack()

    while game.on:
        # update game context
        game.update()

        # update top state
        top_state = game.state_stack[-1]
        top_state.handle_events(pygame.event.get())
        top_state.update()

        # draw game
        game.display.fill(COLORS["bg"])
        game.drawing_manager.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
