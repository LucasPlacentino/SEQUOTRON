# tempo class
from Env import MAX_TEMPO, MIN_TEMPO


class Tempo:

    def __init__(self, initalTempo, lcd):
        self.value = initalTempo
        self.lcd = lcd
        self.step = 0

        self.on = "" # remove if using self.active
        # test :
        self.active = False

    def increaseTempo(self):
        if self.value < MAX_TEMPO :
            self.value += 1
            self.lcd.displayTempo(self.value)

    def decreaseTempo(self):
        if self.value > MIN_TEMPO :
            self.value -= 1
            self.lcd.displayTempo(self.value)