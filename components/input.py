import time
from component import Component

class Input(Component):
    
    def __init__(self, controller):
        self._controller = controller
        self._inputs = ["podium", "hdmi", "usbc", "vga"]
        self._current_input = self._inputs[0]
        self._duration = 0
        
    def switch_input(self, ):

    def update_duration(self):
        """
        Update the duration period since the last state change.
        """
        self._duration = time.time() - self._last_state_change
    
    def get_duration(self):
        """
        Return a float of the seconds since the last state change.
        """
        self.update_duration()
        return self._duration