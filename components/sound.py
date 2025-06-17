from components.component import Component
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty

class Sound(Component, EventDispatcher):
    

    def __init__(self):
        super().__init__()
        self._volume = NumericProperty(50)
        self._mute = BooleanProperty(False)

    def set_volume(self, volume=50):
        """
        Takes an integer volume_request between 0 and 100.
        Unmutes the system, if needed, and sets system
        volume to the volume request level given.
        """
        if self._mute:
            self.unset_mute()
        
        command_volume = volume - 100
        self._volume = volume
        command = str(command_volume) + 'V'
        self._commander.send_command(command, True)
        self.set_clock()

    def set_mute(self):
        """
        Enable mute on the system.
        """
        self._mute = True
        self._commander.send_command("disable_audio")
        self.set_clock()

    def unset_mute(self):
        """
        Disable mute on the system. Unmute.
        """
        self._mute = False
        self._commander.send_command("enable_audio")
        self.set_clock()
    
    def get_mute(self):
        """
        Return the mute setting of the Sound object.
        boolean True = Muted, False = Unmuted
        """
        return self._mute

    def get_volume(self):
        """
        Return the volume level of the Sound object.
        Integer from 0-100, low to high volume.
        """
        return self._volume

    def get_state(self):
        """
        Return the state of Sound with a tuple formatted:
        (bool mute_state, int volume, float duration)
        """
        mute_state = self.get_mute()
        volume = self.get_volume()
        duration = self.get_duration()
        return (mute_state, volume, duration)