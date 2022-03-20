# clock class
import time

from Env import NB_STEPS, GATE_CHANNEL, MAX_DAC, PITCH_CHANNEL, NB_NOTES



# !   -----  NEED TO TEST  -----


class ClockSequencer():

    def __init__(self, sequencer, tempo, gate):
        self.sequencer = sequencer
        self.tempo = tempo
        self.gate = gate
        #self.noteSequence = sequencer.noteSequence # ?

    def playClock(self):
        self.tempo.active = True
        while self.tempo.active:
            pitch = self.sequencer.noteSequence.listSteps[self.tempo.step][1]
            octave = self.sequencer.noteSequence.listSteps[self.tempo.step][0]
            # change note each step
            self.sequencer.dac1.output.open()
            self.sequencer.dac1.output.setVoltage(PITCH_CHANNEL, int(MAX_DAC*((12*int(octave) + int(pitch))/NB_NOTES))) # ! WHICH DAC ?
            self.sequencer.dac1.output.close()
            print("step", self.tempo.step, "note to dac1 channel0:", pitch, octave)        
        
            print("----step start----")
        
            self.sequencer.ledSequence.ledOn(self.tempo.step)
        
            # start gate
            self.sequencer.dac2.output.open()
            self.sequencer.dac2.output.setVoltage(GATE_CHANNEL, MAX_DAC) # ! WHICH DAC ?
            self.sequencer.dac2.output.close() # ?
            print("Gate value:", self.gate.value)
            time.sleep((60/self.tempo.value)*(self.gate.value)) # ?
        
            # end gate
            self.sequencer.dac2.output.open() # ?
            self.sequencer.dac2.output.setVoltage(GATE_CHANNEL, 0) # ! WHICH DAC ?
            self.sequencer.dac2.output.close()
            time.sleep((60/self.tempo.value)*(1-self.gate.value)) # ?
        
            print("----step ended----")

            self.tempo.step += 1
            self.tempo.step = self.tempo.step%NB_STEPS
            
            if self.sequencer.button1.is_pressed == False:
                self.pauseClock()

    def pauseClock(self):
        self.tempo.active = False



#! NOT NECESSARY ?

'''
import time
import threading


class Tempo:
    value = 100
    n = 0
    on = "on"

tempo = Tempo()


def setvoltage():
    dac3.setVoltage(1, 12*l_step[tempo.n][0] + l_step[tempo.n][1])


def off():
    tempo.on = "off"


def on():
    tempo.on = "on"
    while tempo.on == "on":
        threading.Timer(60/tempo.value, setvoltage).start()
        tempo.n += 1
        tempo.n = tempo.n%8
        button1.when_released = off
'''



"""class ClockSequencer:

    def __init__(self):
        self.internal = True

    def clockTypeToggle(self, type="internal"):
        if type == "internal":
            self.internal = True
        elif type == "external":
            self.internal = False
        else:
            #Error
            print("Error, wrong clock type. Clock set to default (internal)")
            self.internal = True

    def ticking(self, tempo): #! sends the clock signal to gate, note, sequence, steps, etc
        if self.internal:
            print("tick")
            clock = 1
            #time.sleep(60/self.tempo.current_tempo)
            #send a clock signal
            clock = 0
        else:
            #external clock
            pass
"""