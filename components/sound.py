from component import Component

class Sound(Component):
    

    def __init__(self):
        super().__init__()
        self._volume = 50
        self._mute = False