"""
This module contains the Device class, a virtual class representing the methods needed
for a device to function and update the huskontroller.
"""
class Component():
    """
    The Component class is meant to represent a generic component of the AV
    system. It is a template for other classes implementing it.
    
    The Component object will interact with the controller by passing
    along commands requested of it and by updating the controller with any
    pertinent changes to its state.
    """
    def __init__(self, controller = None):
        self._controller = controller
    
    def get_controller(self):
        return self._controller
    
    def set_controller(self, controller):
        self._controller = controller

    def get_state():
        pass

    def get_duration():
        pass