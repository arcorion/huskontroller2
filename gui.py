from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.graphics import *
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from pathlib import Path
from random import choice
from time import sleep
import platform, threading

from components.sound import Sound

# Use this to enable a random background selection on start
# If False, a specific background will always be chosen..
ENABLE_RANDOM_BACKGROUND = False
# Setting color constants:
SELECTED_TRANSPARENCY = .98
UNSELECTED_TRANSPARENCY = .4
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
        Config.set('graphics', 'fullscreen', 'auto')
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '480')
        Config.set('graphics', 'borderless', '1')
        Window.show_cursor = False
    case 'Windows' | 'Darwin':
        Window.size = (800, 480)
    case _:
        Exception("Not a supported OS")


class TouchPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(TouchPanel, self).__init__(**kwargs)

    def get_background(self, random=ENABLE_RANDOM_BACKGROUND):
        source_path = Path(__file__).resolve()
        source_dir = source_path.parent
        image_directory = source_dir / 'images' / 'backgrounds'     
        
        background = str(image_directory / 'handsome_doggy_2.png')
        if random:
            background_list = [x for x in image_directory.iterdir()]
            background = str(choice(background_list))

        return background


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
        self.font_size = 24
        self.outline_width = 1
        self.outline_color = [0, 0, 0, 1]
        self.bold = True
        self.corner_radius = 10
        with self.canvas.after:
            self._col = Color(1, 1, 1, 0)
            self._border = Line(width=3)
        
        self.bind(pos=self.update, size=self.update, state=self.update)
        Clock.schedule_once(self.update, 0)

    def update(self, *args):
        self._border.rounded_rectangle = (self.x, self.y, self.width, self.height, 4)
        self._col.a = 1 if self.state == 'down' else 0

    def on_state(self, widget, value):
        if value == 'down':
            self.background_color = self.background_color_down
        else:
            self.background_color = self.background_color_normal
            #self.canvas.after.clear()

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
        self.app = App.get_running_app()

    # def on_state(self, widget, value):
    #     popup = PowerOnPopup()
    #     Clock.schedule_once(partial(popup.open), 0.1)
    #     if self.app.projector.power_state == True:
    #         self.state = 'down'
    #     else:
    #         self.state = 'normal'
    #     self.app.controller.turn_on_projector() if (self.state == "down") else self.app.controller.turn_off_projector()

    def start_projector(self):
        threading.Thread(target=self.app.controller.turn_on_projector, daemon=True).start()
        power_on_message = PowerPopup()
        power_on_message.open()
        Clock.schedule_once(self.call_unset_blank, 10)
        Clock.schedule_once(self.call_unset_freeze, 10)
    
    def stop_projector(self):
        Clock.schedule_once(self.call_unset_blank, 1)
        Clock.schedule_once(self.call_unset_freeze, 1)
        threading.Thread(target=self.app.controller.turn_off_projector, daemon=True).start()
        power_off_message = PowerPopup("off")
        power_off_message.open()
    
    def call_unset_blank(self, timer):
        self.app.image.unset_blank()

    def call_unset_freeze(self, timer):
        self.app.image.unset_freeze()
 

class PowerPopup(Popup):
    def __init__(self, on_off_text="on", **kwargs):
        super(PowerPopup, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.auto_dismiss = False
        self.background = ''
        self.background_color = tuple(HUSKY_PURPLE + [SELECTED_TRANSPARENCY])
        self.on_off_text = on_off_text
        self.seconds = self.app.controller.PROJECTOR_WAIT
        self.size_hint = (0.9, 0.9)
        self.title = 'Projector'
        self.title_align = 'center'
        self.title_font = './fonts/open_sans/open_sans_regular.ttf'
        self.title_size = '36sp'

        self.message = f"Powering {self.on_off_text}.\nInterface available in {self.seconds} seconds."
        self.content = Label(text=self.message)
        
        Clock.schedule_interval(self.update_message, 1)
    
    def update_message(self, seconds):
        self.seconds -= 1
        if self.seconds == 0:
            self.dismiss()
        else:
            self.content.text =  f"Powering {self.on_off_text}.\nInterface available in {self.seconds} seconds."

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


class HuskontrollerApp(App):
    def __init__(self, components_dictionary):
        super(HuskontrollerApp, self).__init__()
        self.image = components_dictionary["image"]
        self.input = components_dictionary["input"]
        self.projector = components_dictionary["projector"]
        self.sound = components_dictionary["sound"]
        self.controller = components_dictionary["controller"]
        self.controller.set_initial_state()

    def build(self):
        Builder.load_file("gui.kv")
        return TouchPanel()