import time

class Clock:
    """
    Clock represents the duration since the last state change
    of a component. It stores the last time a state was changed
    and gets the duration since that last time.
    """
    def __init__(self):
        self._last_state_change = time.time()
        self._duration = 0

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
    
    def get_last_state_change(self):
        """
        Return a float of the time when the last state was changed
        (in seconds since unix epoch)
        """
        return self._last_state_change
    
    def set_last_state_change(self):
        """
        Sets the last state change to the current time.
        """
        self._last_state_change = time.time()