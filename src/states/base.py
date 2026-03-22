from core.enums import StateNames
from core.settings import Z_MAX, GameContext, pygame, TYPE_CHECKING
from core.utils import get_tui_text_box

if TYPE_CHECKING:
    from ui.composites.manager import UIManager


class GameState:
    """base game state class, should be inherited by all game state classes"""

    name = StateNames.BASE

    def __init__(self):
        self.draw_below = True
        """determines whether this game state can be drawn below the active one"""
        self.ui: UIManager = None
        """a ui manager that updates a collection of ui elements"""
        self.dim = True
        """"determine if the state is dimmed when drawn below others"""
        self.make_ui()

    @property
    def game(self):
        return GameContext.game

    @property
    def is_top_state(self):
        return self == self.game.state_stack[-1]

    @property
    def position_in_stack(self):
        """
        determines the position of the state in the games state stack.
        used for z-ordering during drawing.
        """
        return self.game.state_stack.index(self)

    def make_ui(self):
        """
        creates a list of all ui elements present in this game state
        and puts them in a ui manager to be assigned to self.ui
        """
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.power_off()
            elif event.type == pygame.VIDEORESIZE:
                self.game.render_dim()

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self, force_rendering=False):
        pass

    def draw(self):
        pass

    def draw_dim(self):
        """used for states below top state, to dim them."""
        if not self.dim:
            return
        draw_call = lambda: self.game.display.blit(
            self.game.dim_surf, self.game.dim_rect
        )
        self.ui.register_draw_call(Z_MAX, draw_call)

    def __str__(self):
        text = f"{self.name} {hex(id(self))}"
        return get_tui_text_box(text)
