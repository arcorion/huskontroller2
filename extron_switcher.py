import logging
import serial
import time
from components.command import Command
from huskontroller import Huskontroller
from pathlib import Path
from serial.tools import list_ports

class ExtronSwitcher():
    """
    Class representing the Extron device's communication - it
    handles hows commands and response are sent and received.
    """
    def __init__(self):
        """
        Initializes device - gets a list of all connected
        serial devices, picking the first from the list and assuming
        that's the Extron device. If multiple serial devices are
        connected, modify this to account for the devices.
        """
        self.logger = logging.getLogger('extron_serial')
        self.logger.setLevel(logging.DEBUG)
        
        log_path = Path('logs')
        if not log_path.exists():
            log_path.mkdir()
        file_handler = logging.FileHandler('logs/extron_serial.log')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(fmt='%(asctime)s - %(message)s',
                                        datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.info('Extron serial device connection initializing...\n')

        try:
            port_list = list_ports.comports()
            port_names = []
            for port in port_list:
                port_names += port
            self.extron_device = serial.Serial(port_names[0], 9600)
            self.logger.info(f'Device {self.extron_device} created.')
        except serial.SerialException:
            self.logger.error(f'Error opening connection to port: {port_list[0]}')

        self.command = Command(self.extron_device)
        self.update = None
        """
        
        
        CHANGE THIS PART ^^^^ self.update = None!?
        
        """

    def select_input(self, input_device):
        """
        Takes the name of an input device 'podium', 'hdmi', 'usb-c', or 'vga'
        and sends the associated command to the Extron switcher.
        """
        inputs = {'podium': '1!', 'hdmi': '2!', 'usb-c': '3!', 'vga': '4!'}
        command = inputs[input_device]
        self.command.send_command(command)
    
    def freeze(self):
        """
        Tells send_command to freeze display.
        """
        self.command.send_command('enable_freeze')
        
    def unfreeze(self):
        """
        Tells send_command to unfreeze display.
        """
        self.command.send_command('disable_freeze')
    
    def blank(self):
        """
        Tells send_command to blank display.
        """
        self.command.send_command('disable_video')
    
    def unblank(self):
        """
        Tells send_command to unblank display.
        """
        self.command.send_command('enable_video')
        
    def turn_projector_on(self):
        """
        Tells send_command to turn on projector.
        """
        self.command.send_command('enable_projector')
        time.sleep(10)
        self.command.send_command('disable_freeze')
        time.sleep(5)
        self.command.send_command('enable_audio')
        time.sleep(5)
        self.command.send_command('enable_video')

    def turn_projector_off(self):
        """
        Tells send_command to turn off projector.
        """
        self.command.send_command('disable_projector')
    
    def set_volume(self, volume_level):
        """
        Calculates volume and sends custom string of the Extron
        SIS command to send_command.
        """
        self.command.send_command('enable_audio')
        volume = -100
        volume = volume + int(volume_level)
        command = str(volume_level) + 'V'
        self.command.send_command(command, True)
    
    def mute(self):
        """
        Tells send_command to mute the audio.
        """
        self.command.send_command('disable_audio')
    
    def unmute(self):
        """
        Tells send_command to unmute the audio.
        """
        self.command.send_command('enable_audio')