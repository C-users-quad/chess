from core.settings import GameContext, TYPE_CHECKING
from core.utils import get_tui_text_box

if TYPE_CHECKING:
    from states.base import GameState
    from ui.base import UIElement


class UIManager:
    """manages all ui elements in a particular state"""

    def __init__(self, state: GameState, elements: list[UIElement] = []):
        """
        manages a collection of ui elements
        """
        self.elements = elements
        self.state = state
        self.draw_calls: dict[int, list[callable]] = {}
        """draw calls for this specific ui manager/state."""

    @property
    def game(self):
        return GameContext.game

    def assign_manager_to_elements(self):
        for element in self.elements:
            element.manager = self

    def render(self, force_rendering=False):
        for element in self.elements:
            if (
                not force_rendering
                and not self.game.window_resized()
                and not element.dirty
            ):
                continue
            element.render()
            element.dirty = False

    def draw(self):
        for element in self.elements:
            if not self.state.is_top_state and not element.draw_below:
                continue
            element.register_draw_call()

    def register_draw_call(self, z_index: int, draw_call: callable):
        self.draw_calls.setdefault(z_index, []).append(draw_call)

    def clear_draw_calls(self):
        self.draw_calls.clear()

    def update(self):
        self.assign_manager_to_elements()
        for element in self.elements:
            element.update()

    def __str__(self):
        lines = f"UIManager {hex(id(self))}\nElements: {self.elements}"

        return get_tui_text_box(lines)
