#from Sequencer import MAX_TEMPO, MIN_TEMPO #? , LCD
from Env import MAX_TEMPO, MIN_TEMPO #*
# ? import Sequencer


class Tempo:

    # ? lcd = Sequencer.lcd
    # ? lcd = LCD

    def __init__(self, initalTempo, lcd):
        self.value = initalTempo
        self.lcd = lcd
        self.step = 0
        self.on = ""

    def increaseTempo(self):
        if self.value < MAX_TEMPO :
            self.value += 1
            self.lcd.displayTempo(self.value)

    def decreaseTempo(self):
        if self.value > MIN_TEMPO :
            self.value -= 1
            self.lcd.displayTempo(self.value)