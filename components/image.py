from component import Component

class Image(Component):
    """
    Represents the image state - either frozen, blank, or neither.
    """
    def __init__(self, controller):
        """
        Set initial state with freeze and blank disabled.
        """
        super().__init__()
        self._controller = controller
        self._frozen = False
        self._blanked = False
        self._duration = 0
        self.freeze(False)
        self.blank(False)
        self._controller.update(self.get_state)
        
    def freeze(self):
        """
        Send freeze command and update internal state.
        """
        self._controller.set_image("frozen")
        self._frozen = True
        self._clock.set_last_state_change()

    def unfreeze(self):
        """
        Send unfreeze command and update internal state.
        """
        self._controller.set_image("unfrozen")
        self._frozen = False
        self._clock.set_last_state_change()

    def blank(self):
        """
        Send blank command and update internal state.
        """
        self._controller.set_image("blanked")
        self._blanked = True
        self._clock.set_last_state_change()

    def unblank(self):
        """
        Send unblank command and update internal state.
        """
        self._controller.set_image("unblanked")
        self._blanked = False
        self._clock.set_last_state_change()
    
    def get_state(self):
        """
        Return a tuple of the blank state, frozen state, and duration
        in seconds since last state change. (bool, bool, float)
        """
        self._clock.update_duration()
        return (self._blanked, self._frozen, self._duration)