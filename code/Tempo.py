from Sequencer import MAX_TEMPO, MIN_TEMPO #? , LCD
# ? import Sequencer


class Tempo:

    # ? lcd = Sequencer.lcd
    # ? lcd = LCD

    def __init__(self, initalTempo, lcd):
        self.value = initalTempo
        self.lcd = lcd

    def increaseTempo(self):
        if self.value < MAX_TEMPO :
            self.value += 1
            self.lcd.displayTempo(self.value)

    def decreaseTempo(self):
        if self.value > MIN_TEMPO :
            self.value -= 1
            self.lcd.displayTempo(self.value)