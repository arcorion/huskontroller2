from component import Component

class Input(Component):
    

    _INPUTS = ["podium", "hdmi", "usbc", "vga"]

    def __init__(self, controller):
        self._controller = controller
        self._current_input = self._inputs[0]
        self._duration = 0
        self._input = 0
        
    def set_input(self, input):
        """
        Attempt to set the input based off a passed string.
        "podium", "hdmi", "usbc", and "vga" are allowed.
        """
        try: 
            index = self._INPUTS.index(input)
        except ValueError:
            print(f"Input not possible: {input}")
        except Exception as error:
            print(f"Unexpected error with Input: {error}")
        
        self._input = index

    def get_input(self):
        """
        Return a string of the currently set input,
         Options: "podium", "hdmi", "usbc", or "vga"
        """
        return self._INPUTS[self._input]
    
    def get_state(self):
        return self._current_input