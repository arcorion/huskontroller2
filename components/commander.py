import serial
from serial.tools import list_ports

class Commander:
    """
    Commander handles the command string that is
    sent to the Extron device.

    It associates the commands themselves with a useful
    name for easy use in other methods.
    """
    def __init__(self):
        """
        Initializes the Commander module. This creates
        a dictionary representing the list of supported commands and
        creates a serial connection to the Extron scaler.

        If a connection to the scaler cannot be made, it will instead
        create a proxy device which just outputs commands to the console.

        It is possible to send a pre-formatted command via the send_command()
        method. The "custom" bool must be set as "True". As I write this, only
        the Sound module uses this. It passes the volume setting this way.
        """
        
        self.command_list = {
            'select_podium': '1!',
            'select_hdmi': '2!',
            'select_usbc': '3!',
            'select_vga': '4!',
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

        self._device = None
        try:
            port_list = list_ports.comports()
            port_names = []
            for port in port_list:
                port_names += port
            self._device = serial.Serial(port_names[0], 9600)
        except serial.SerialException:
            print(f'Error opening connection to port: {port_list[0]}')
            if (self._device is None):
                print("Problems exist with serial device.")
                print("Writing serial commmands to console: ")
                self._device = SerialProxy()
        
    def send_command(self, command, custom=False):
        """
        Takes a command string and sends the command as an
        encoded byte string to the Extron device.
        """
        command_string = self.command_list.get(command)
        if command_string:
            self._device.write(command_string.encode())
        elif custom == True:
            self._device.write(command.encode())
        else:
            print(f'Unsupported command: {command}')

class SerialProxy:
    """
    A proxy device for printing serial commands when
    the serial interface doesn't work.

    It takes serial commands and writes them to the console
    instead of to an actual serial device. Useful for testing.
    """
    def __init__(self):
        pass

    
    def write(self, string):
        """
        Takes an encoded bytestring "string", decodes it, and prints it
        to the console.
        """
        print(string.decode())