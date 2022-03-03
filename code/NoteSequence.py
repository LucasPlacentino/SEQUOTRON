#from Sequencer import MAX_PITCH, MAX_OCTAVE, MAX_STEP, MIN_STEP, MIN_OCTAVE, MIN_PITCH
from Env import NB_STEPS, MAX_PITCH, MAX_OCTAVE, MAX_STEP, MIN_STEP, MIN_OCTAVE, MIN_PITCH
'''
import Env

MAX_OCTAVE = Env.MAX_OCTAVE
MIN_OCTAVE = Env.MIN_OCTAVE
MAX_PITCH = Env.MAX_PITCH
MIN_PITCH = Env.MIN_PITCH
MAX_STEP = Env.
NB_STEPS = Env.NB_STEPS# or from Env import NB_STEPS
#...
'''

class NoteSequence:

    def __init__(self, lcd):
        self.step = 0
        self.lcd = lcd
        self.note = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.listSteps = []
        for i in range(NB_STEPS): # creation of the list of steps
            self.listSteps.append([0, 1]) #cette liste représente l'octave 0 et la note 1
        print("steps list created:\n"+str(self.listSteps))

    def increaseStep(self):
        self.step = (self.step + 1) % (MAX_STEP+1) # MX_STEP+1 ?
        print("Step : " + str(self.step))
        '''
        if self.step < MAX_STEP:
            self.step += 1
        '''

    def decreaseStep(self):
        if self.step == MIN_STEP: 
            self.step = MAX_STEP
        else:
            self.step -= 1
        #self.step = (self.step - 1) % MAX_STEP  # if step = -1 -> 6
        print("Step : " + str(self.step))
        '''
        if self.step > MIN_STEP:
            self.step -= 1
        '''

    def increasePitch(self):
        if self.listSteps[self.step.nbstep][1] == MAX_PITCH:
            self.listSteps[self.step.nbstep][0] += 1
            self.listSteps[self.step.nbstep][0] = self.listSteps[self.step.nbstep][0]%(MAX_OCTAVE + 1)
            self.listSteps[self.step.nbstep][1] += 1
        self.listSteps[self.step.nbstep][1] += 1
        self.listSteps[self.step.nbstep][1] = self.listSteps[self.step.nbstep][1]%(MAX_PITCH + 1)
        print("pitch increase")

    def decreasePitch(self):
        if self.listSteps[self.step][1] == MIN_PITCH:
            self.listSteps[self.step][1] = MAX_PITCH
            if self.listSteps[self.step][0] == MIN_OCTAVE:
                self.listSteps[self.step][0] = MAX_OCTAVE
            else:
                self.listSteps[self.step][0] -= 1
        else:
            self.listSteps[self.step][1] -= 1
        print("pitch decrease")

    def increaseOctave(self):
        if self.listSteps[self.step][0] == MAX_OCTAVE:
            self.listSteps[self.step][0] = MIN_OCTAVE
        else:
            self.listSteps[self.step][0] += 1
        print("octave increase")
    
    def decreaseOctave(self):
        if self.listSteps[self.step][0] == MIN_OCTAVE:
            self.listSteps[self.step][0] = MAX_OCTAVE
        else:
            self.listSteps[self.step][0] -= 1
        print("octave decrease")
