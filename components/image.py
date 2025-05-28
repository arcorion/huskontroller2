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
        self._frozen = False
        self._blanked = False

        self.unset_freeze()
        self.unset_blank()
        
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
    
    def get_state(self):
        """
        Return image state in the form of tuple
        (bool freeze_state, bool blank_state, float duration).
        """
        freeze_state = self.get_freeze()
        blank_state = self.get_blank()
        duration = self.get_duration()
        return (freeze_state, blank_state, duration)