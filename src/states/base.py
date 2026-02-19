from core.settings import *
from core.utils import get_tui_text_box

class GameState:
    """base game state class, should be inherited by all game state classes"""
    def __init__(self):
        self.draw_below = False
        """determines whether this game state can be drawn below the active one"""
        self.ui = []
        """a list of ui elements, so that you can easily update and draw them."""
        self.dim = True
        """"determine if the state is dimmed when drawn below others"""

    @property
    def game(self):
        return GameContext.game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.power_off()
            elif event.type == pygame.VIDEORESIZE:
                self.game.dim_surf = pygame.Surface(
                    self.game.display.get_size(), pygame.SRCALPHA)
                self.game.dim_surf.fill((*COLORS['state-dim'], STATE_DIM_ALPHA))
                self.game.dim_rect = self.game.dim_surf.get_rect()

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def draw(self):
        pass

    def draw_dim(self):
        """used for states below top state, to dim them."""
        if not self.dim: return
        self.game.display.blit(self.game.dim_surf, self.game.dim_rect)

    def __str__(self):
        text = f"GameState {hex(id(self))}"
        return get_tui_text_box(text)
