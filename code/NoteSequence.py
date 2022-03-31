# note sequence

from Env import NB_STEPS, MAX_PITCH, MAX_OCTAVE, MAX_STEP, MIN_STEP, MIN_OCTAVE, MIN_PITCH


class NoteSequence:

    def __init__(self, lcd):
        self.step = 0
        self.lcd = lcd
        self.note = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.listSteps = []
        # * single_note = {"pitch": 0, "octave": 1}
        for i in range(NB_STEPS): # creation of the list of steps
            self.listSteps.append([1, 0]) # list represent octave (1), and pitch (0: C)
            # * self.listSteps.append(single_note) # * would rather use this so we can then get noteSequence.listSteps[nbStep][pitch]
        print("steps list created:\n"+str(self.listSteps))

    def increaseStep(self):
        self.step = (self.step + 1) % (MAX_STEP+1) # MX_STEP+1 ?
        print("Step : " + str(self.step+1)) # +1 because 1->8 not 0->7
        self.lcd.displayStep((self.step+1), self.note[self.listSteps[self.step][1]],self.listSteps[self.step][0]) # +1 because 1->8 not 0->7
        
        ''' # ! REMOVE ?
        if self.step < MAX_STEP:
            self.step += 1
        '''

    def decreaseStep(self):
        if self.step == MIN_STEP: 
            self.step = MAX_STEP
        else:
            self.step -= 1
        #self.step = (self.step - 1) % MAX_STEP  # if step = -1 -> 6
        print("Step : " + str(self.step+1)) # +1 because 1->8 not 0->7
        self.lcd.displayStep((self.step+1), self.note[self.listSteps[self.step][1]-1],self.listSteps[self.step][0]) # +1 because 1->8 not 0->7
        
        ''' # ! REMOVE ?
        if self.step > MIN_STEP:
            self.step -= 1
        '''

    def increasePitch(self):
        if self.listSteps[self.step][1] == MAX_PITCH:
            self.listSteps[self.step][0] += 1
            self.listSteps[self.step][0] = self.listSteps[self.step][0]%(MAX_OCTAVE + 1)
            self.listSteps[self.step][1] = MIN_PITCH
        else:
            self.listSteps[self.step][1] += 1
        print("pitch increase:")
        print(self.note[self.listSteps[self.step][1]-1],self.listSteps[self.step][0]) # - 1 because list start from 0 and not 1
        print(self.listSteps[self.step][1]-1) # - 1 because list start from 0 and not 1
        self.lcd.displayNote(self.note[self.listSteps[self.step][1]-1],self.listSteps[self.step][0]) # - 1 because list start from 0 and not 1

    def decreasePitch(self):
        if self.listSteps[self.step][1] == MIN_PITCH:
            self.listSteps[self.step][1] = MAX_PITCH
            if self.listSteps[self.step][0] == MIN_OCTAVE:
                self.listSteps[self.step][0] = MAX_OCTAVE
            else:
                self.listSteps[self.step][0] -= 1
        else:
            self.listSteps[self.step][1] -= 1
        print("pitch decrease:")
        print(self.note[self.listSteps[self.step][1]-1],self.listSteps[self.step][0]) # - 1 because list start from 0 and not 1
        print(self.listSteps[self.step][1]-1) # - 1 because list start from 0 and not 1
        self.lcd.displayNote(self.note[self.listSteps[self.step][1]-1],self.listSteps[self.step][0]) # - 1 because list start from 0 and not 1

    def increaseOctave(self):
        if self.listSteps[self.step][0] == MAX_OCTAVE:
            self.listSteps[self.step][0] = MIN_OCTAVE
        else:
            self.listSteps[self.step][0] += 1
        print("octave increase")
        self.lcd.displayNote(self.note[self.listSteps[self.step][1]-1],self.listSteps[self.step][0])
    
    def decreaseOctave(self):
        if self.listSteps[self.step][0] == MIN_OCTAVE:
            self.listSteps[self.step][0] = MAX_OCTAVE
        else:
            self.listSteps[self.step][0] -= 1
        print("octave decrease")
        self.lcd.displayNote(self.note[self.listSteps[self.step][1]-1],self.listSteps[self.step][0])

