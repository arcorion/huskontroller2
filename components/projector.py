from component import Component

class Projector(Component):
    """
    Represents the projector's state - either "off" or "on",
    as well as how long it has been since its state was
    last changed.
    """

    def __init__(self):
        """
        Initialize projector object, setting power state to off
        by default and initializing clock.
        """
        super().__init__()
        self._power_state = "off"

    def disable(self):
        """
        Command function, sets projector to off and sends command.
        """
        self.set_state("off")
        self._commander.send_command("disable_projector")
        self.set_clock()

    def enable(self):
        """
        Command function, sets projector to on and sends command.
        """
        self.set_state("on")
        self._commander.send_command("enable_projector")
        self.set_clock()

    def get_power_state(self):
        """
        Return the power state string "off" or "on".
        """
        return self._power_state

    def get_state(self):
        """
        Return the projector state in the form
        (string power_state, float duration)
        """
        power_state = self.get_power_state()
        duration = self.get_duration()
        return (power_state, duration)

