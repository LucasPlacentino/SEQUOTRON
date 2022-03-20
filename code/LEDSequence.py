# led sequence
import pcf8574_io
#from time import sleep
from Env import LED_QUANTITY


# ! NEED TO UPDATE

class LEDSequence: # TODO

    def __init__(self): # TODO
        #self.stepNumber = 1
        # ? self.ledQuantity = LED_QUANTITY # = the number of steps in the sequence? #? needed ?
        self.portExpanderLED = pcf8574_io.PCF(0x38) # ! set the correct I2C adress of the PCF8574 for the LEDs
        self.pinLEDs = ["p0","p1","p2","p3","p4","p5","p6","p7"] # defines the GPIO pin of each LED in the sequence
        for i in self.pinLEDs:
            self.portExpanderLED.pin_mode(i, "OUTPUT")
        """
        for i in self.pinLEDs:
            self.portExpanderLED.pin_mode(i, "OUTPUT") # set pins of the PCF8574 as OUTPUTs
        self.leds = {} # ?
        # ? self.leds = {1: pinLED1, 2: pinLED2} # LEDs numbers start from 1 (not 0)
        for i in range(0,LED_QUANTITY): # ?
            self.leds[i+1] = LED(self.pinLEDs[i]) # dictionnary with {1: LED(pinLED1), 2: LED(pinLED2), etc} # ?
        """

    def ledOn(self, LEDnumber): # TODO
        self.portExpanderLED.write(self.pinLEDs[LEDnumber-1], "HIGH")        
        self.portExpanderLED.write(self.pinLEDs[LEDnumber], "LOW")
        print("next led")
        """
        self.leds[LEDnumber-1].off()
        #turnOnLED(self.leds[LEDnumber])
        self.leds[LEDnumber].on() # get the LED object from the dictionnary and turn it on gpiozero
        """

    def turnAllLedOff(self):
        for i in self.pinLEDs:
            self.portExpanderLED.write(i,"HIGH")

