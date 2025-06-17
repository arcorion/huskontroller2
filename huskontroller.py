from time import sleep

from components.commander import Commander
from components.image import Image
from components.input import Input
from components.projector import Projector
from components.sound import Sound
from gui import HuskontrollerApp

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty

class Huskontroller:
    def __init__(self):
        self._commander = Commander()
        self._image = Image()
        self._input = Input(self._commander)
        self._projector = Projector()
        self._sound = Sound()
        self._touchscreen = HuskontrollerApp()
        
        # Defines wait time between projector start
        # and sending the first command
        self._projector_wait = 10

        self.set_initial_state()

        self._device_list = [self._image,
                             self._input, self._projector,
                             self._sound]
    
        self._touchscreen.run()

    def set_initial_state(self):
        """
        Set default state of the AV system. Projector is turned off,
        Image is set to unfrozen and unblanked, Input is set to podium,
        sound is enabled and set to volume of 50.
        """
        sleep(self._projector_wait)
        self._projector.disable()
        sleep(self._projector_wait)
        self._image.unset_blank()
        self._image.unset_freeze()
        self._input.set_input("podium")
        self._sound.unset_mute()
        self._sound.set_volume(50)

    def turn_on_projector(self):
        self._projector.enable()
        sleep(self._projector_wait)
        self._image.unset_blank()
        self._image.unset_freeze()
    
    def turn_off_projector(self):
        self._projector.enable()
        sleep(self._projector_wait)
        self._image.unset_blank()
        self._image.unset_freeze()
    
    def set_input_podium(self):
        power_on = self._projector.get_power_state()
        if not power_on:
            self.turn_on_projector()
        self._input.set_input("podium")

    def set_input_hdmi(self):
        power_on = self._projector.get_power_state()
        if not power_on:
            self.turn_on_projector()
        self._input.set_input("hdmi")

    def set_input_usbc(self):
        power_on = self._projector.get_power_state()
        if not power_on:
            self.turn_on_projector()
        self._input.set_input("usbc")

    def set_input_vga(self):
        power_on = self._projector.get_power_state()
        if not power_on:
            self.turn_on_projector()
        self._input.set_input("vga")

    def toggle_blank(self):
        blank = self._image.get_blank()
        if blank:
            self._image.unset_blank()
        else:
            self._image.set_blank()

    def toggle_freeze(self):
        frozen = self._image.get_freeze()
        if frozen:
            self._image.unset_freeze()
        else:
            self._image.set_freeze()

    def toggle_camera(self):
        """
        Not implemented - will toggle camera off
        and on when done.
        """
        pass

    def set_volume(self, volume):
        self._sound.unset_mute()
        self._sound.set_volume(volume)
    
    def toggle_mute(self):
        muted = self._sound.get_mute()
        if muted:
            self._sound.unset_mute()
        else:
            self._sound.set_mute()

    def run(self):
        pass

if __name__ == '__main__':
    controller = Huskontroller()
    controller.run()