from core.enums import StateNames
from core.settings import VariableSettings
from ui.rects.text_box import UITextBox


class UIClock(UITextBox):
    def __init__(self, **kwargs):
        """
        displays the time in minutes:seconds
        where to update the time remaining?:
            in chess state in update in a new method like update_time() idk bruh...
        """
        super().__init__(text=self.curr_time_string, **kwargs)
        self.prev_time_remaining = VariableSettings.game_time

    @property
    def time_remaining(self):
        return self.game.get_state(StateNames.CHESS).time_remaining

    @property
    def curr_time_string(self):
        # prevents from accessing time_remaining before fully initialized
        if self.game.get_state(StateNames.CHESS) is None:
            minutes = VariableSettings.game_time // 60
            seconds = VariableSettings.game_time % 60
        else:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60

        if seconds == 0:
            seconds = "00"
            
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
