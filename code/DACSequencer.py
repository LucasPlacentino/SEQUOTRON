from MCP4922 import MCP4922
# ? import spidev

class DACSequencer():

    def __init__(self, spibus, spidevice, pinCE, number=None):
        #self.type = type #12 or 8 bit, # of channels, etc.

        self.spibus = spibus
        self.spidevice = spidevice
        self.output = MCP4922(spibus, spidevice, pinCE)
        self.ce = pinCE
        self.number = number

