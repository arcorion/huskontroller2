from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import *
from kivy.graphics import Callback
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from pathlib import Path
from random import choice
import platform

# Setting color constants:
SELECTED_TRANSPARENCY = .98
UNSELECTED_TRANSPARENCY = .35
# Husky colors - only Husky Purple used as I write this, but
# kept for future options.
HUSKY_PURPLE = [50/255, 0, 100/255]
SPIRIT_PURPLE = [51/255, 0, 111/255]
HUSKY_GOLD = [232/255, 211/255, 162/255]
HERITAGE_GOLD = [145/255, 123/255, 76/255]
SPIRIT_GOLD = [1, 199/255, 0]
ACCENT_GREEN = [170/255, 219/255, 30/255]
ACCENT_TEAL = [42/255, 210/255, 201/255]
ACCENT_PINK = [233/255, 60/255, 172/255]
ACCENT_LAVENDER = [197/255, 180/255, 227/255]
# Input buttons
PODIUM_GREEN = [0/255, 90/255, 45/255]
USBC_RED = [200/255, 30/255, 30/255]
HDMI_YELLOW = [210/255, 210/255, 10/255]
VGA_BLUE = [0/255, 10/255, 150/255]

operating_system = platform.system()
match operating_system:
    case 'Linux':
        Config.set('graphic', 'fullscreen', 'auto')
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '480')
        Config.set('graphics', 'borderless', '1')
        Window.show_cursor = False
    case 'Windows' | 'Darwin':
        Window.size = (800, 480)
    case _:
        Exception("Not a supported OS")

Builder.load_file('gui.kv')

class TouchPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(TouchPanel, self).__init__(**kwargs)

    def get_background(self):
        image_directory = Path.cwd() / 'images' / 'backgrounds'     
        
        background_list = [x for x in image_directory.iterdir()]
        return str(choice(background_list))
        #return "./images/backgrounds/pidubs-normal.png"


class DefaultButton(ToggleButton):
    """
    Describes the default settings for buttons in 
    Huskontroller.
    """
    def __init__(self, **kwargs):
        super(DefaultButton, self).__init__(**kwargs)
        
        base_color = HUSKY_PURPLE
        self.background_color_normal = self.add_transparency(
            base_color, 'unselected')
        self.background_color_down =  self.add_transparency(
            base_color, 'selected')
        self.background_color = self.background_color_normal
        self.background_down = ''
        self.background_normal = ''
        self.color = (250/255, 250/255, 250/255, 1)
        self.font_name = './fonts/open_sans/open_sans_regular.ttf'
        self.font_size = 36
        self.outline_width = 5
        self.outline_color = [0, 0, 0, 1]
        self.bold = True

    def on_state(self, widget, value):
        if value == 'down':
            self.background_color = self.background_color_down
            with self.canvas.after:
                husky_gold = HUSKY_GOLD
                husky_gold.append(SELECTED_TRANSPARENCY)
                Color(husky_gold)
                Line(width=2, rectangle=[self.x, self.y,
                                self.width, self.height])
        else:
            self.background_color = self.background_color_normal
            self.canvas.after.clear()

    def on_text(self, instance, value):
        base_color = None
        match self.text:
            case 'Podium':
                base_color = PODIUM_GREEN
            case 'USB-C':
                base_color = USBC_RED
            case 'HDMI':
                base_color = HDMI_YELLOW
            case 'VGA':
                base_color = VGA_BLUE
            case _:
                base_color = HUSKY_PURPLE

    def add_transparency(self, color, selected):
        match selected:
            case 'selected':
                transparency = SELECTED_TRANSPARENCY
            case 'unselected':
                transparency = UNSELECTED_TRANSPARENCY
        color = list(color)[:3]
        color.append(transparency)
        return color


class TopBar(ToggleButton):
    """
    Top informational bar
    """
    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)


class Desktop(BoxLayout):
    """
    Main desktop compopent - contains everything except
    the TopBar
    """
    pass


class PowerInput(BoxLayout):
    """
    Contains the PowerButton and InputButtons
    """
    pass


class PowerButtonContainer(BoxLayout):
    pass

class PowerButton(DefaultButton):
    
    def __init__(self, **kwargs):
        super(PowerButton, self).__init__(**kwargs)


class InputButtons(GridLayout):
    """
    Contains the different InputButton widgets.
    """
    pass


class InputButton(DefaultButton):
    """
    Buttons used to toggle input
    """
    def __init__(self, **kwargs):
        super(InputButton, self).__init__(**kwargs)
        self.allow_no_selection = False

        #usbc_red = USBC_RED
        #hdmi_yellow = HDMI_YELLOW
        #vga_blue = VGA_BLUE
        #podium_disabled = 
        #usbc_disabled = 
        #hdmi_disabled = 
        #vga_disabled =

    def on_text(self, instance, value):
        base_color = None
        match self.text:
            case 'Podium':
                base_color = PODIUM_GREEN
            case 'USB-C':
                base_color = USBC_RED
            case 'HDMI':
                base_color = HDMI_YELLOW
            case 'VGA':
                base_color = VGA_BLUE
            case _:
                base_color = HUSKY_PURPLE   

        self.background_color_normal = self.add_transparency(
            base_color, 'unselected')
        self.background_color_down =  self.add_transparency(
            base_color, 'selected')
        self.background_color = self.background_color_normal


class BlankSpace(Label):
    """
    Empty Label - provides blank space to make the interface
    more "roomy"
    """
    pass


class ImageButtons(BoxLayout):
    """
    Contains BlankButton and FreezeButton, as well
    as a blank for later use.
    """
    pass


class LaterUseBlank(Label):
    """
    Blank space set aside for later use, probably for the
    camera toggle.
    """
    pass


class BlankButton(DefaultButton):
    pass


class FreezeButton(DefaultButton):
    pass


class SoundControls(BoxLayout):
    """
    Contains VolumeLabel, VolumeSlider, and MuteButton
    """
    pass


class VolumeLabel(Button):
    pass


class VolumeSlider(Slider):    
    pass


class MuteButton(DefaultButton):
    pass


class Huskontroller(App):
    def build(self):
        return TouchPanel()


if __name__ == "__main__":
    """
    Run me, my dear friend!
    """
    Huskontroller().run()