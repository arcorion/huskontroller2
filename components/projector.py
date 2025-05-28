from component import Component

class Projector(Component):
    """
    Represents the projector's state - either "off" or "on",
    as well as how long it has been since its state was
    last changed.
    """

    def __init__(self):
        super().__init__()
        self._power_state = "off"

    def disable(self):
        self.set_state("off")
        self._commander.send_command("disable_projector")

    def enable(self):
        self.set_state("on")
        self._commander.send_command("enable_projector")

    def get_state(self):
        return self._power_state
    
    def set_state(self, power_state):
        """
        Takes a string "power_state" and tracks
        the on and off state of the projector.

        This also triggers the set_clock of the
        component.

        Throws an error if power_state is
        anything other than "on" or "off".
        """
        match power_state:
            case "on" | "off":
                self._power_state = power_state
            case _:
                log_error = f"Error with power_state: {power_state}"
                self.log.error(log_error)
                raise ValueError(log_error)
