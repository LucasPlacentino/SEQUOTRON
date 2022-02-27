# import time
# from Sequencer import Sequencer
# from LCDSequencer import LCDSequencer

class Gate:

    def __init__(self, dac, channel, lcd):
        self.dac = dac
        self.channel = channel
        self.value = 0.5
        self.lcd = lcd

    def increaseGate(self):
        if self.value >= 0.95:
            self.value = 0
        else:
            self.value += 0.1
        self.lcd.displayGate(round(self.value,1))
        # self.dac.setVoltage(self.channel, 4096) for an amount of time
        print(self, self.dac, self.channel, round(self.value,1))

    
    def decreaseGate(self):
        if self.value <= 0.05:
            self.value = 1
        else:
            self.value -= 0.1
        self.lcd.displayGate(round(self.value,1))
        # self.dac.setVoltage(self.channel, 4096)  for an amount of time
        print(self, self.dac, self.channel, round(self.value,1))

    def sendGateSignal(self, tempo): # called every step
        self.dac.setVoltage(self.channel, 4096)
        print("Gate sent", self.dac, self.channel, self.value)
        # time.sleep((60/tempo.value)*self.value)
        self.dac.setVoltage(self.channel, 0)
