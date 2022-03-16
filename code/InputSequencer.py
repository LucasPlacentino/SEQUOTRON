# Inputs (jacks) class
# ? import pcf8574_io

# ! NOT NECESSARY ????

class InputSequencer(): # on a PCF8574 port expander

    def __init__(self, portExpander, pin):
        self.pin = pin
        self.portExpander = portExpander

    def readJack(self):
        if self.portExpander.read(self.pin) == "HIGH":
            return True
        else:
            return False
