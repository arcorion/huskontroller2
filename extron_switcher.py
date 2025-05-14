# REMOVE ME WHEN DONE
import time
from components.command import Command
from huskontroller import Huskontroller


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
        pass

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