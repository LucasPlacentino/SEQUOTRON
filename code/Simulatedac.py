'''
#! USED TO SIMULATE THE DAC (for testing purposes)
'''
class Simulatedac():

    def __init__(self, spibus, spidevice, pinCE, number=None):
        #self.type = type #12 or 8 bit, # of channels, etc.

        self.spibus = spibus
        self.spidevice = spidevice
        self.ce = pinCE
        self.number = number
        self.output = MCP4922Simulated(spibus, spidevice, pinCE, number)

class MCP4922Simulated():

    def __init__(self, spibus, spidevice, pinCE, number):
        self.spibus = spibus
        self.spidevice = spidevice
        self.ce = pinCE
        self.number = number

    def setVoltage(self, channel, value):
        print("DAC", self.number,"ce:", self.ce, ", channel:", channel, ", value:", str(value)+"(/4095)")
        voltage = 5*(value/4095)
        print("(Voltage equivalent:",str(round(voltage,3))+"V)")

    def shutdown(self, i):
        print("DAC shut down, channel",i)

    def open(self):
        print("DAC opened")

    def close(self):
        print("DAC closed")

