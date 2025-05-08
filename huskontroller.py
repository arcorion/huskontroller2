from extron_switcher import ExtronSwitcher, ExtronCommand, ExtronResponse
from display import HuskontrollerUI

class Huskontroller:
    def __init__(self):
        self.extron_switcher = ExtronSwitcher()


    def run(self):
        pass

if __name__ == '__main__':
    controller = Huskontroller()
    controller.run()