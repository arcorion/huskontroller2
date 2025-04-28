from extron_switcher import ExtronSwitcher, ExtronCommand, ExtronResponse
from huskontroller_ui import HuskontrollerUI

class Huskontroller:
    def __init__(self):
        self.extron_switcher = ExtronSwitcher()
        self.root = tk.Tk()
        self.root.title("Huskontroller")
        self.create_widgets()

    def run(self):
        self.root.mainloop()

if __main__ == '__main__':
    controller = Huskontroller()
    controller.run()