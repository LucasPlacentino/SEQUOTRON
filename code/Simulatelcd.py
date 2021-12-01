class Simulatelcd:
    '''
    FOR TESTING PURPOSES ONLY
    Simulated LCD, to use when running the program outside of a RPi, it will just print out rather than display on the LCD
    that way you don't get the RPLC or smbus or i2c libraries errors
    '''
    def __init_(self):
        self.testvar = 0
    
    def displayTempo(self, tempo):
        print("tempo:" + tempo)
    
    def displayNote(self, pitch, octave):
        print("pitch:" + pitch + " octave:" + octave)

    def displayStep(self, step):
        print("step:" + step.nbstep)
        self.displayNote(step.picth, step.octave)