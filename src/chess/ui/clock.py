from core.enums import PieceColors, StateNames
from core.settings import VariableSettings
from ui.rects.text_box import UITextBox


class UIClock(UITextBox):
    def __init__(self, **kwargs):
        """
        displays the time remaining in minutes:seconds
        for the player who is currently moving
        """
        super().__init__(text=self.curr_time_string, **kwargs)
        self.prev_time_remaining = VariableSettings.player_time

    @property
    def time_remaining(self) -> int:
        chess_state = self.game.get_state(StateNames.CHESS)
        match chess_state.board.turn_color:
            case PieceColors.WHITE:
                return chess_state.white_time
            case PieceColors.BLACK:
                return chess_state.black_time

    @property
    def curr_time_string(self):

        if self.game.get_state(StateNames.CHESS) is None:
            minutes = VariableSettings.player_time // 60
            seconds = VariableSettings.player_time % 60
        else:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60

        # convert times to strings
        minutes = str(minutes)
        seconds = str(seconds)

        # format time strings if they are single-digit and need a zero
        if len(minutes) < 2:
            minutes = "0" + minutes
        if len(seconds) < 2:
            seconds = "0" + seconds

        return f"{minutes}:{seconds}"

    def detect_time_passing(self):
        """
        if the time remaining has changed,
        re-render with new time string
        """
        if self.prev_time_remaining != self.time_remaining:
            self.text = self.curr_time_string
            self.dirty = True

        self.prev_time_remaining = self.time_remaining

    def update(self):
        self.detect_time_passing()
