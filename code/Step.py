#from Sequencer import MIN_STEP, MAX_STEP
from Env import MAX_STEP, MIN_STEP

class Step: # ! NOT NECESSARY ANYMORE, SEE NoteSequence.py

    def __init__(self, nbstep=MAX_STEP+1, pitch=3, octave=3):

        self.nbstep = nbstep # here 8
        self.pitch = pitch
        ''' 1:C(do)  2:C#(do#)  3:D(re)  4:D#(re#)  5:E(mi)  6:F(fa)  7:F#(fa#)  8:G(sol)  9:G#(sol#)  10:A(la)  11:A#(la#)  12:B(si) '''
        ''' formule note -> freq : f = 2^(n/12) * 440 Hz  où n est le nombre de demi-note par rapport à A4 (positif si plus haut et négatif si plus bas)
            utiliser le mapping MIDI ? : https://en.wikipedia.org/wiki/Musical_note#:~:text=For%20use%20with%20the%20MIDI%20(Musical%20Instrument%20Digital%20Interface)%20standard%2C%20a%20frequency%20mapping%20is%20defined%20by%3A
        '''
        self.octave = octave


        self.n = 0
        
    def increaseStep(self):
        self.n = (self.n + 1) % MAX_STEP
        print("Step : " + str(self.n)) #


    def decreaseStep(self):
        self.n = (self.n - 1) % MAX_STEP # si -1 -> 7
        '''
        if self.n == MIN_STEP:  # step.pitch
            self.n = MAX_STEP
        else:
            self.n -= 1
        '''
        print("Step : " + str(self.n)) #
    

    