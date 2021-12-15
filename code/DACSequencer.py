from MCP4922 import MCP4922
import spidev

class DACSequencer():

    def __init__(self, spibus, spidevice, pinCE):
        #self.type = type #12 or 8 bit, # of channels, etc.

        #self.spibus = spibus
        #self.spidevice = spidevice
        #self.ce = ce
        self.dac = MCP4922(spibus, spidevice, pinCE)