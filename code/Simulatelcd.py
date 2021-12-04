class Simulatelcd:
    '''
    FOR TESTING PURPOSES ONLY
    Simulated LCD, to use when running the program outside of a RPi, it will just print out rather than display on the LCD
    that way you don't get the RPLC or smbus or i2c libraries errors
    '''
    def __init_(self):
        self.testvar = 0
    
    def displayTempo(self, tempo):
        print("tempo:" + str(tempo))
    
    def displayNote(self, pitch, octave):
        print("pitch:" + str(pitch) + " octave:" + str(octave))

    def displayStep(self, step):
        print("step:" + str(step.nbstep))
        self.displayNote(str(step.picth), str(step.octave))
    
    def clearLCD(self):
        print("clear LCD")

    def toggleBacklight(self, boolean):
        print("Backlight: " + str(boolean))