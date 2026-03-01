import pygame
from core.settings import GameContext
from core.utils import get_tui_text_box


class GameState:
    """base game state class, should be inherited by all game state classes"""

    name = None

    def __init__(self):
        self.draw_below = True
        """determines whether this game state can be drawn below the active one"""
        self.ui = None
        """a ui manager that updates a collection of ui elements"""
        self.dim = True
        """"determine if the state is dimmed when drawn below others"""

    @property
    def game(self):
        return GameContext.game

    def make_ui(self):
        """creates a list of all ui elements present in this game state"""
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
        self.game.display.blit(self.game.dim_surf, self.game.dim_rect)

    def __str__(self):
        text = f"{self.name.value} {hex(id(self))}"
        return get_tui_text_box(text)
