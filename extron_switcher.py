import logging
import serial
import time
from pathlib import Path
from serial.tools import list_ports

class ExtronSwitcher:
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
        self.extron_response = ExtronResponse(self.extron_device)

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
        Tells send_command to freeze display.
        """
        self.extron_command.send_command('enable_freeze')
        
    def unfreeze(self):
        """
        Tells send_command to unfreeze display.
        """
        self.extron_command.send_command('disable_freeze')
    
    def blank(self):
        """
        Tells send_command to blank display.
        """
        self.extron_command.send_command('disable_video')
    
    def unblank(self):
        """
        Tells send_command to unblank display.
        """
        self.extron_command.send_command('enable_video')
        
    def turn_projector_on(self):
        """
        Tells send_command to turn on projector.
        """
        self.extron_command.send_command('enable_projector')
        time.sleep(10)
        self.extron_command.send_command('disable_freeze')
        time.sleep(5)
        self.extron_command.send_command('enable_audio')
        time.sleep(5)
        self.extron_command.send_command('enable_video')

    def turn_projector_off(self):
        """
        Tells send_command to turn off projector.
        """
        self.extron_command.send_command('disable_projector')
    
    def set_volume(self, volume_level):
        """
        Calculates volume and sends custom string of the Extron
        SIS command to send_command.
        """
        volume = -100
        volume = volume + int(volume_level)
        command = str(volume_level) + 'V'
        self.extron_command.send_command(command, True)
    
    def mute(self):
        """
        Tells send_command to mute the audio.
        """
        self.extron_command.send_command('disable_audio')
    
    def unmute(self):
        """
        Tells send_command to unmute the audio.
        """
        self.extron_command.send_command('enable_audio')


class ExtronCommand:
    """
    ExtronCommand handles the command string that is
    sent to the Extron device.

    It associates the commands themselves with a useful
    name for easy use in other methods.
    """
    def __init__(self, device):
        pass

        self.command_list = {
            'select_input': '1!',
            'view_current_input': '!',
            'enable_freeze': '1*1F',
            'disable_freeze': '1*0F',
            'get_freeze_status': '1F',
            'disable_video': '1*1B',
            'enable_video': '1*0B',
            'get_video_status': '1*B',
            'enable_projector': 'W+snds9*9|%02PON%03',
            'disable_projector': 'W+snds9*9|%02POF%03',
            'get_volume': 'V',
            'disable_audio': '1Z',
            'enable_audio': '0Z',
            'get_audio_status': 'Z'
        }

    def send_command(self, command, custom=False):
        """
        Takes a command string and sends the command as an
        encoded byte string to the Extron device.
        """
        command_string = self.command_list.get(command)
        if command_string:
            self.extron_device.write(command_string.encode())
            self.logger.info(f'Command sent: {command_string}')
        elif custom == True:
            self.extron_device.write(command.encode())
            self.logger.info(f'Custom command sent: {command}')
        else:
            self.logger.error(f'Unsupported command: {command}')


class ExtronResponse:
    pass