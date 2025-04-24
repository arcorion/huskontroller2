
class ExtronCommand:
    """
    ExtronCommand handles the command string that is
    sent to the Extron device.
    """"
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
            'get_video_status': '1*B','
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
        self.logger.info(f'Sending command: {command}')
        self.extron_device.write(command.encode())

        command_string = self.command_list.get(command)
        if command_string:
            self.extron_device.write(command_string.encode())
            self.logger.info(f'Command sent: {command_string}')
        else if custom == True:
            self.extron_device.write(command.encode())
            self.logger.info(f'Custom command sent: {command}')
        else:
            self.logger.error(f'Unsupported command: {command}')