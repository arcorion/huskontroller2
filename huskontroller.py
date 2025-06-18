from time import sleep

from components.commander import Commander
from components.image import Image
from components.input import Input
from components.projector import Projector
from components.sound import Sound
from gui import HuskontrollerApp

from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty

class Huskontroller(EventDispatcher):
    def __init__(self):
        self._commander = Commander()
        self.image = Image()
        self.input = Input(self._commander)
        self.projector = Projector()
        self.sound = Sound()

        # Defines wait time between projector start
        # and sending the first command
        self.projector_wait = 20

        self.components_dictionary = {
            "image" : self.image,
            "input" : self.input,
            "projector" : self.projector,
            "sound" : self.sound
        }
        
        self.touchscreen = HuskontrollerApp(self.components_dictionary)
        self.set_initial_state()

        self.touchscreen.run()

    def set_everything_on(self):
        self.projector.enable()
        self.image.set_blank()
        self.image.set_freeze()
        self.input.set_input("usbc")
        self.sound.set_mute()
        self.sound.set_volume(100)

    def set_initial_state(self):
        """
        Set default state of the AV system. Projector is turned off,
        Image is set to unfrozen and unblanked, Input is set to podium,
        sound is enabled and set to volume of 50.
        """
        self.projector.disable()
        sleep(self.projector_wait)
        self.image.unset_blank()
        self.image.unset_freeze()
        self.input.set_input("podium")
        self.sound.unset_mute()
        self.sound.set_volume(20)

    def turn_on_projector(self):
        self.projector.enable()
        sleep(self.projector_wait)
        self.image.unset_blank()
        self.image.unset_freeze()
    
    def turn_off_projector(self):
        self.projector.enable()
        sleep(self.projector_wait)
        self.image.unset_blank()
        self.image.unset_freeze()
    
    def set_input_podium(self):
        power_on = self.projector.get_power_state()
        if not power_on:
            self.turn_on_projector()
        self.input.set_input("podium")

    def set_input_hdmi(self):
        power_on = self._projector.get_power_state()
        if not power_on:
            self.turn_on_projector()
        self.input.set_input("hdmi")

    def set_input_usbc(self):
        power_on = self.projector.get_power_state()
        if not power_on:
            self.turn_on_projector()
        self.input.set_input("usbc")

    def set_input_vga(self):
        power_on = self.projector.get_power_state()
        if not power_on:
            self.turn_on_projector()
        self.input.set_input("vga")

    def toggle_blank(self):
        blank = self.image.get_blank()
        if blank:
            self.image.unset_blank()
        else:
            self.image.set_blank()

    def toggle_freeze(self):
        frozen = self.image.get_freeze()
        if frozen:
            self.image.unset_freeze()
        else:
            self.image.set_freeze()

    def toggle_camera(self):
        """
        Not implemented - will toggle camera off
        and on when done.
        """
        pass

    def set_volume(self, volume):
        self.sound.unset_mute()
        self.sound.set_volume(volume)
    
    def toggle_mute(self):
        muted = self.sound.get_mute()
        if muted:
            self.sound.unset_mute()
        else:
            self.sound.set_mute()

if __name__ == '__main__':
    controller = Huskontroller()