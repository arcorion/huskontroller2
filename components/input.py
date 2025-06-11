from components.component import Component

class Input(Component):
    """
    The Input component manages the state of the AV
    input. It ensures that one of the four inputs,
    "podium", "hdmi", "usbc", and "vga" are selected
    and provides a getter module for the input.
    """

    _INPUTS = ["podium", "hdmi", "usbc", "vga"]

    def __init__(self, huskontroller):
        super().__init__()

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
        
        # Input number set from index
        self._input = index

        # Commander expects 1-4, not 0-3, so increment and then
        # append to select string.
        command = self._INPUTS[self._input]
        input_command = "select_" + str(command)
        self._commander.send_command(input_command)

    def get_input(self):
        """
        Return a string of the currently set input,
         Options: "podium", "hdmi", "usbc", or "vga"
        """
        return self._INPUTS[self._input]
    
    def get_state(self):
        """
        Return the state of the input as a tuple in the form
        (string input, float duration).
        """
        input = self.get_input()
        duration = self.get_duration()
        return (input, duration)