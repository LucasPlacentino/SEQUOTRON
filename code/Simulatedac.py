'''
#! USED TO SIMULATE THE DAC (for testing purposes)
'''

from Env import MAX_DAC, MAX_OCTAVE
class Simulatedac():

    def __init__(self, spibus, spidevice, pinCE, number=None):
        #self.type = type #12 or 8 bit, # of channels, etc.

        self.spibus = spibus
        self.spidevice = spidevice
        self.ce = pinCE
        self.number = number
        self.output = MCP4922Simulated(spibus, spidevice, pinCE, number)

    def setVoltage(self, channel, value):
        print("dac", self.number, "channel", channel, "opened")
        self.output.open()
        self.output.setVoltage(channel, value)
        print("dac", self.number, "channel", channel, "closed")
        self.output.close()

class MCP4922Simulated():

    def __init__(self, spibus, spidevice, pinCE, number):
        self.spibus = spibus
        self.spidevice = spidevice
        self.ce = pinCE
        self.number = number

    def setVoltage(self, channel, value):
        print("DAC", self.number,"ce:", self.ce, ", channel:", channel, ", value:", str(value)+"(/"+MAX_DAC+")")
        voltage = (MAX_OCTAVE+1)*(value/MAX_DAC)
        print("(Voltage equivalent:",str(round(voltage,3))+"V)")

    def shutdown(self, i):
        print("DAC shut down, channel",i)

    def open(self):
        print("DAC opened")

    def close(self):
        print("DAC closed")

