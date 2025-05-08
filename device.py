"""
This module contains the Device class, a virtual class representing the methods needed
for a device to function and update the huskontroller.
"""
from abc import ABC


class Device(ABC):
    """
    The Device class is meant to represent a generic device.
    It should function as a template for other classes implementing it.
    
    The Device object will interact with the controller by passing
    along commands requested of it and by updating the controller with any
    pertinent changes to its state.
    """
    def __init__(self, controller = None):
        self._controller = controller
    
    def get_controller(self):
        return self._controller
    
    def set_controller(self, controller):
        self._controller = controller


class Projector:
    """
    Represents the projector's state - either off or on.
    """
    power_status = False

    def __init__():
        pass

class Screen:
    """
    Represents the screen state - either frozen, blank, or neither.
    """
    pass


class Volume:
    pass