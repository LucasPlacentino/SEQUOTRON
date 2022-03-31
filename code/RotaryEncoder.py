# rotary encoder

import gpiozero

# ! really necessary ?

class RotaryEncoder:
    
    def __init__(self, pin1, pin2, type="", outputCVNumber=0):
        self.type = type #ie: "tempo", "cv" or "gate".
        self.outputCVNumber = outputCVNumber # if type = "cv"
        self.rotor = gpiozero.RotaryEncoder(pin1, pin2) # GPIO of the A and B pins of the rotary encoder


