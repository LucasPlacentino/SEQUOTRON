class Simulatedac():

    def __init__(self, spibus, spidevice, pinCE):
        #self.type = type #12 or 8 bit, # of channels, etc.

        #self.spibus = spibus
        #self.spidevice = spidevice
        self.ce = pinCE

    def setVoltage(self, channel, value):
        print(self, "channel:", channel, "value", value)