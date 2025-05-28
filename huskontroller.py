from time import sleep

from components.commander import Command
from components.image import Image
from components.input import Input
from components.projector import Projector
from components.sound import Sound
from components.touchscreen.touchscreen import Touchscreen
from serial.tools import list_ports

class Huskontroller:
    def __init__(self):
        self._command = Command(self)
        self._image = Image(self)
        self._input = Input(self)
        self._projector = Projector(self)
        self._sound = Sound(self)
        self._touchscreen = Touchscreen(self)

        self.set_initial_state()

        self._device_list = [self._command, self._image,
                             self._input, self._projector,
                             self._sound, self._touchscreen]

    def set_initial_state(self):
        """
        Set default state of the AV system. Projector is turned off,
        Image is set to unfrozen and unblanked, Input is set to podium,
        sound is enabled and set to volume of 50.
        """
        self._projector.disable()
        sleep(10)
        self._image.unblank()
        self._image.unfreeze()
        self._input.switch_input("podium")
        self._sound.on()
        self._sound.set_volume(50)

    def turn_on_projector(self):
        self._projector.on()
        self._image.unblank()
        self._image.unfreeze()
        self._sound.on()
        self._sound.set_volume(50)
    
    def turn_off_projector():
        pass





    def run(self):
        pass

if __name__ == '__main__':
    controller = Huskontroller()
    controller.run()