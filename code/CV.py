from Sequencer import MAX_CV, LCD
#? from Sequencer import Sequencer, dac1, dac2, dac3

class CV:

    def __init__(self, number, dac, channel=0):
        self.value = 0
        self.dac = dac
        self.channel = channel
        self.number = number

    def increaseCV(self):
        self.value += 1
        #self.value = self.n%24 # (self.n%24) + 1 ?
        self.value = self.n%MAX_CV
        self.dac.setVoltage(self.channel, int(float(4096)*CV.CV1/24)) #! MAX_CV rather than 24 ?
        print(self, self.dac, self.channel, self.value)
        LCD.displayCV(self.number, self.value) #? need to test

    def decreaseCV(self):
        if self.value == 0:
            self.value = 24
        else:
            self.value -= 1
        self.dac.setVoltage(self.channel, int(float(4096)*CV.CV2/24)) #! MAX_CV rather than 24 ?
        print(self, self.dac, self.channel, self.value)
        LCD.displayCV(self.number, self.value) #? need to test
