from extron_switcher import ExtronSwitcher, ExtronCommand, ExtronResponse
from huskontroller_ui import HuskontrollerUI

class Huskontroller:
    def __init__(self):
        self.extron_switcher = ExtronSwitcher()


    def run(self):
        pass

if __main__ == '__main__':
    controller = Huskontroller()
    controller.run()