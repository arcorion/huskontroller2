from component import Component

class Projector(Component):
    """
    Represents the projector's state - either "off" or "on",
    as well as how long it has been since its state was
    last changed.
    """

    def __init__(self):
        self._power_state = False
        self._duration = 0

    def get_state(self):
        if self._power_state:
            return "on"
        else:
            return "off"
    
    def set_state(self, power_state):
        """
        Takes a 
        """