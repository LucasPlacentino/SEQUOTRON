from Sequencer import LED_QUANTITY
from gpiozero import LED
import pcf8574_io
from time import sleep # ?


# ! NEED TO UPDATE

class LEDSequence: # TODO

    def __init__(self): # TODO
        self.stepNumber = 1
        # ? self.ledQuantity = LED_QUANTITY # = the number of steps in the sequence? #? needed ?
        self.portExpanderLED = pcf8574_io.PCF(0x38) # ! set the correct I2C adress of the PCF8574 for the LEDs
        self.pinLEDs = ["p0","p1","p2","p3","p4","p5","p6","p7"] # defines the GPIO pin of each LED in the sequence
        for i in self.pinLEDs:
            self.portExpanderLED.pin_mode(i, "OUTPUT") # set pins of the PCF8574 as OUTPUTs
        self.leds = {} # ?
        # ? self.leds = {1: pinLED1, 2: pinLED2} # LEDs numbers start from 1 (not 0)
        for i in range(0,LED_QUANTITY): # ?
            self.leds[i+1] = LED(self.pinLEDs[i]) # dictionnary with {1: LED(pinLED1), 2: LED(pinLED2), etc} # ?

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


'''
try:
    bpm = 240

    p1 = pcf8574_io.PCF(0x38)
    sleep(1)
    pins = ["p0","p1","p2","p3","p4","p5","p6","p7"]
    for i in pins:
        p1.pin_mode(i,"OUTPUT")
    #sleep(1)
    p = 0
    while True:
        p = p%8
        p1.write(pins[p-1],"HIGH")
        p1.write(pins[p],"LOW")
        p += 1
        sleep(60/bpm)
except:
    for n in pins:
        p1.write(n,"HIGH")
'''
