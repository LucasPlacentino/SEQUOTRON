from Sequencer import LED_QUANTITY
from gpiozero import LED
class LEDSequence: # TODO

    def __init__(self): # TODO
        self.stepNumber = 1
        #? self.ledQuantity = LED_QUANTITY # = the number of steps in the sequence? #? needed ?
        self.pinLEDs = [3,4] # defines the GPIO pin of each LED in the sequence
        self.leds = {}
        #? self.leds = {1: pinLED1, 2: pinLED2} # LEDs numbers start from 1 (not 0)
        for i in range(1,LED_QUANTITY):
            self.leds[i] = LED(self.pinLEDs[i-1]) # dictionnary with {1: LED(pinLED1), 2: LED(pinLED2), etc}

    def ledOn(self, LEDnumber): # TODO
        #turnOnLED(self.leds[LEDnumber])
        self.leds[LEDnumber].on() # get the LED object from the dictionnary and turn it on gpiozero

    def clockSignal(self): # TODO
        '''
        #* OR
        if self.stepNumber > 8:
            self.stepNumber = 1
        self.ledOn(self.stepNumber)
        self.stepNumber += 1
        '''
        self.stepNumber = (self.stepNumber%8)+1
        self.ledOn(self.stepNumber)
