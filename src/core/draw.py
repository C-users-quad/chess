from core.settings import GameContext


class DrawingManager:
    def __init__(self):
        self.draw_calls: dict[int, dict[int, list[callable]]] = {}
        """
        is a dictionary of
        z-index -> dictionary of z-index -> list of draw calls.

        main tool used to z-order drawing.
        """

    @property
    def game(self):
        return GameContext.game

    def construct_draw_calls(self):
        """
        call draw on every applicable state and combine the draw calls generated
        by those calls into self.draw_calls
        """
        # setup draw calls for lower states
        for z_index, state in enumerate(self.game.state_stack[:-1]):
            if not state.draw_below:
                continue
            state.render(force_rendering=True)
            state.draw()
            state.draw_dim()
            self.draw_calls[z_index] = state.ui.draw_calls

        # setup draw calls for top state
        top_state = self.game.state_stack[-1]
        top_state.render()
        top_state.draw()
        self.draw_calls[top_state.position_in_stack] = top_state.ui.draw_calls

    def reset_draw_calls(self):
        """
        empty all draw calls here and across all states' managers.
        """
        self.draw_calls.clear()
        for state in self.game.state_stack:
            state.ui.clear_draw_calls()

    def draw(self):
        """
        draws every state, z-ordered.
        """
        # populate self.draw_calls
        self.construct_draw_calls()

        # iterate draw_calls with respect to the z-ordering and draw
        for _, draw_calls in sorted(self.draw_calls.items()):
            for _, call_list in sorted(draw_calls.items()):
                for draw_call in call_list:
                    draw_call()

        # empty self.draw_calls and draw_calls
        self.reset_draw_calls()
