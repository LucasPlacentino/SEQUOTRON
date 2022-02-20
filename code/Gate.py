import time
#from Sequencer import Sequencer
#from LCDSequencer import LCDSequencer

class Gate:

    def __init__(self, dac, channel, lcd):
        self.dac = dac
        self.channel = channel
        self.value = 0.5
        self.lcd = lcd

    def increaseGate(self):
        if self.value < 1:
            self.value -= 0.1
            self.lcd.displayGate(self.value)
            #self.dac.setVoltage(self.channel, 4096*self.value)
            #print(self, self.dac, self.channel, self.value)

    
    def decreaseGate(self):
        if self.value > 0:
            self.value += 0.1
            self.lcd.displayGate(self.value)
            #self.dac.setVoltage(self.channel, 4096*self.value)
            #print(self, self.dac, self.channel, self.value)

    def sendGateSignal(self, tempo): # called every step
        self.dac.setVoltage(self.channel, 4096)
        print("Gate sent", self.dac, self.channel, self.value)
        time.sleep((60/tempo.value)*self.value)
        self.dac.setVoltage(self.channel, 0)
