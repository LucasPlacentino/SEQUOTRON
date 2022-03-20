# from Sequencer import MAX_CV, LCD, MAX_DAC
# ? from Sequencer import Sequencer, dac1, dac2, dac3
from Simulatelcd import Simulatelcd
from LCDSequencer import LCDSequencer
# ? from Sequencer import LCD
from Env import SIMULATED_LCD, MAX_CV, MAX_DAC

#? MAX_CV = 25
''' # not working
if SIMULATED_LCD:
    LCD = Simulatelcd()
else:
    LCD = LCDSequencer()
'''
#? MAX_DAC = 4095

class CV:

    def __init__(self, number, dac, lcd, channel=0):
        self.value = 0
        self.dac = dac
        self.channel = channel
        self.number = number
        self.lcd = lcd

    def increaseCV(self):
        self.value += 1
        #self.value = self.n%24 # (self.n%24) + 1 ?
        self.value = self.value%MAX_CV
        self.dac.output.open()
        self.dac.output.setVoltage(self.channel, int(MAX_DAC*self.value/24)) #! MAX_CV rather than 24 ?
        self.dac.output.close()
        print("CV", self.number, "increased", " (DAC:", self.dac.number, "channel", self.channel, ") Value:", self.value)
        self.lcd.displayCV(self.number, self.value)

    def decreaseCV(self):
        if self.value == 0:
            self.value = 24
        else:
            self.value -= 1
        self.dac.output.open()
        self.dac.output.setVoltage(self.channel, int(MAX_DAC*self.value/24)) #! MAX_CV rather than 24 ?
        self.dac.output.close()
        print("CV", self.number, "decreased", " (DAC:", self.dac.number, "channel", self.channel, ") Value:", self.value)
        self.lcd.displayCV(self.number, self.value)

