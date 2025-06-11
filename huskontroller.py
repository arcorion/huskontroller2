import logging
import os

from pathlib import Path
from time import sleep

from components.image import Image
from components.input import Input
from components.projector import Projector
from components.sound import Sound
from gui import HuskontrollerGUI

class Huskontroller:
    def __init__(self):
        self._image = Image(self)
        self._input = Input(self)
        self._projector = Projector(self)
        self._sound = Sound(self)
        self._gui = HuskontrollerGUI()
        
        # Defines wait time between projector start
        # and sending the first command
        self._projector_wait = 10

        self.set_initial_state()

        self._device_list = [self._image,
                             self._input, self._projector,
                             self._sound, self._gui]

        self._gui.run()

        

    def set_initial_state(self):
        """
        Set default state of the AV system. Projector is turned off,
        Image is set to unfrozen and unblanked, Input is set to podium,
        sound is enabled and set to volume of 50.
        """
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


class Logger:
    """
    Logger object that gets used to write to the log file.
    """
    _logger = logging.getLogger('huskontroller')
    _logger.setLevel(logging.DEBUG)

    # Set the log path to the application_root/logs folder.
    _log_path = Path.cwd()
    _log_path = _log_path.parent
    _log_path = _log_path / 'logs'

    # Make sure the log directory exists
    if not _log_path.exists():
        _log_path.mkdir()

    # Assign the main and backup log paths
    _main_log = _log_path / 'huskontroller.log'
    _backup_log = _log_path / 'backup.log'

    # Set maximum log size to 100MB, copy main to backup,
    # and delete the log file, if overly large.
    _logger_size_limit = 100 * 1024 * 1024
    if _main_log.exists():
        _log_size = os.path.getsize(_main_log)
        if _log_size > _logger_size_limit:
            if _backup_log.exists():
                os.remove(_backup_log)
            os.rename(_main_log, _backup_log)

    # Set the filehandler output to huskontroller.log
    _file_handler = logging.FileHandler(_main_log)
    _file_handler.setLevel(logging.DEBUG)

    # Using the format "YYYY-MM-DD HH:MM:SS" for the timestamp, then a
    # dash, and then the actual message.
    _formatter = logging.Formatter(fmt='%(asctime)s - %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
    _file_handler.setFormatter(_formatter)

    # Appl
    _logger.addHandler(_file_handler)

    def __init__(self, instance_name, enabled=False):
        """
        Takes a string instance_name and boolean enabled.
        The instance name field adds itself immediately after
        each log line's time and before the actual log contents.

        The enabled boolean does what it says. It enables or disables
        logging to disk.
        """
        self._instance_name = instance_name
        self._logger.info(f'Enabling logging for {self._instance_name}')
        self.enabled = enabled
    
    def info(self, log_string):
        """
        Writes the string "log_string" to the log file as an info log.
        """
        if self.enabled:
            self._logger.info(f"{self._instance_name}: {log_string}")

    def warning(self, log_string):
        """
        Writes the string "log_string" to the log file as a warning log.
        """
        if self.enabled:
            self._logger.warning(f"{self._instance_name}: {log_string}")
    
    def error(self, log_string):
        """
        Writes the string "log_string" to the log file as an error log.
        """
        if self.enabled:
            self._logger.error(f"{self._instance_name}: {log_string}")

if __name__ == '__main__':
    controller = Huskontroller()
    controller.run()