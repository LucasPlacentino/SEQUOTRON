import gpiozero

class RotaryEncoder:
    
    def __init__(self, pin1, pin2, type="tempo", outputCVNumber=0):
        self.type = type #ie: "tempo", "cv" or "gate/env". Default: "tempo"
        self.outputCVNumber = outputCVNumber
        self.rotor = gpiozero.RotaryEncoder(pin1, pin2)




    '''
    def modifyTempo(self):
        if self.type == "tempo":
            # change tempo, tempo.current_tempo += 1 or -= 1
            pass

    def modifyGateEnv(self):
        if self.type == "gate/env":
            # change Gate/Env
            pass

    def modifyCV(self, outputNumber):
        if self.type == "cv":
            if outputNumber == 1:
                # change CV1
                pass
            elif outputNumber == 2:
                # change CV2
                pass
            elif outputNumber == 3:
                # change CV3
                pass

    # ----- OR -----
    def modifyValue(self, increase=True):
        if self.type == "tempo":
            pass
        elif self.type == "gate/env":
            pass
        elif self.type == "cv":
            if self.outputCVNumber == 1:
                pass
            elif self.outputCVNumber == 2:
                pass
            elif self.outputCVNumber == 3:
                pass
            else:
                print("Error: Rotary Encoder type = 'CV' but outputCVNumber not = 1,2 or 3")
        else:
            print('Error: Rotary Encoder type incorrect, when trying to change value')
    '''
