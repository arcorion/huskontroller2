import logging
import serial
from extron_command import ExtronCommand
from extron_response import ExtronResponse
from pathlib import Path
from serial.tools import list_ports

class ExtronComm:
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

        self.extron_command = ExtronCommand(self.extron_device)
        self.extron_response = ExtronResponse(self.extron_device))

    def select_input(self, input_device):
        """
        Takes the name of an input device 'podium', 'hdmi', 'usb-c', or 'vga'
        and sends the associated command to the Extron switcher.
        """
        inputs = {'podium': '1!', 'hdmi': '2!', 'usb-c': '3!', 'vga': '4!'}
        command = inputs[input_device]
        self.extron_command.send_command(command)
    
    def freeze(self):
        """
        Sends the Extron command necessary for 
        """
        self.extron_command.send_command('enable_freeze')
        
    def unfreeze(self):
        self.extron_command.send_command('disable_freeze')
    
    def blank(self):
        self.extron_command.send_command('disable_video')
    
    def unblank(self):
        self.extron_command.send_command('enable_video')
        
    def turn_projector_on(self):
        self.extron_command.send_command('enable_projector')
    
    def turn_projector_off(self):
        self.extron_command.send_command('disable_projector')
    
    def set_volume(self, volume_level):
        volume = -100
        volume = volume + int(volume_level)
        command = str(volume_level) + 'V'
        self.extron_command.send_command(command, True)
    
    def mute(self):
        self.extron_command.send_command('disable_audio')
    
    def unmute(self):
        self.extron_command.send_command('enable_audio')