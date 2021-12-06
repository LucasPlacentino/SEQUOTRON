class LEDSequence:

    def __init__(self, ledQuantity=8):
        self.stepNumber = 1
        self.ledQuantity = ledQuantity # = the number of steps in the sequence?
        pinLED1,pinLED2 = 3,4 # defines the GPIO pin of each LED in the sequence
        self.leds = {1: pinLED1, 2: pinLED2} # LEDs numbers start from 1 (not 0)

    def ledOn(self, LEDnumber):
        #turnOnLED(self.leds[LEDnumber])
        pass

    def clockSignal(self):
        if self.stepNumber > 8:
            self.stepNumber = 1
        self.ledOn(self.stepNumber)
        self.stepNumber += 1
