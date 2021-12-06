class RotaryEncoder:
    
    def __init__(self, type="debug", outputCVNumber=0):
        self.type = type #ie: "tempo", "CV" or "gate/env". Default: "debug" (printing in output)
        self.outputCVNumber = outputCVNumber

    def modifyTempo(self):
        if self.type == "tempo":
            # change tempo, tempo.current_tempo += 1 or -= 1
            pass
        if self.type == "debug": # necessary?
            print("RE tempo: ")

    def modifyGateEnv(self):
        if self.type == "gate/env":
            # change Gate/Env
            pass
        if self.type == "debug": # necessary?
            print("RE gate/env: ")

    def modifyCV(self, outputNumber):
        if self.type == "CV":
            if outputNumber == 1:
                # change CV1
                pass
            elif outputNumber == 2:
                # change CV2
                pass
            elif outputNumber == 3:
                # change CV3
                pass
        if self.type == "debug": #necessary?
            print("RE CV: ")

    def debugEncoder(self, value):
        if self.type == "debug":
            print("RE debug: " + str(value))

    # ----- OR -----
    def modifyValue(self, increase=True):
        if self.type == "debug":
            print('RE debug changed value:')
            print('Value increased from RE') if increase else print('Value decreased from RE')
        elif self.type == "tempo":
            pass
        elif self.type == "gate/env":
            pass
        elif self.type == "CV":
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