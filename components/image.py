from component import Component

class Image(Component):
    """
    Represents the image state - either frozen, blank, or neither.
    """
    def __init__(self):
        """
        Set initial state with freeze and blank disabled.
        """
        super().__init__()
        # Setting clock for last state change
        self.set_clock()

        self._frozen = False
        self._blanked = False
        self._duration = 0
        self.set_freeze(False)
        self.set_blank(False)
        
    def set_freeze(self):
        """
        Send freeze command and update internal state.
        """
        self._commander.send_command("enable_freeze")
        self._frozen = True
        self.set_clock()

    def unset_freeze(self):
        """
        Send unfreeze command and update internal state.
        """
        self._commander.send_command("disable_freeze")
        self._frozen = False
        self.set_clock()

    def set_blank(self):
        """
        Send blank command and update internal state.
        """
        self._commander.send_command("disable_video")
        self._blanked = True
        self.set_clock()

    def unset_blank(self):
        """
        Send unblank command and update internal state.
        """
        self._commander.send_command("enable_video")
        self._blanked = False
        self.set_clock()
    
    def get_blank(self):
        """
        Return blank status boolean - true "blanked", false "unblanked"
        """
        return self._blanked
    
    def get_freeze(self):
        """
        Return freeze status boolean - true "frozen", flase "unfrozen"
        """
        return self._frozen