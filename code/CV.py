from Sequencer import Sequencer, dac1, dac2, dac3

class CV:

    def __init__(self, dac, channel=0):
        self.value = 0
        self.dac = dac
        self.channel = channel

    def increaseCV(self):
        self.value += 1
        self.value = self.n%24 # (self.n%24) + 1 ?
        self.dac.setVoltage(self.channel, 4096*(self.value/24))
        print(self, self.dac, self.channel, self.value)

    def decreaseCV(self):
        if self.value == 0:
            self.value = 24
        else:
            self.value -= 1
        self.dac.setVoltage(self.channel, 4096*(self.value/24))
        print(self, self.dac, self.channel, self.value)
