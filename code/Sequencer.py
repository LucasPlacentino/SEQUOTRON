# Sequencer Class

from DACSequencer import DACSequencer #* critical
import gpiozero
#? import time
from LCDSequencer import LCDSequencer #* critical
from Simulatelcd import Simulatelcd #* for testing only
from Simulatedac import Simulatedac #* for testing only
#? import spidev
#? from signal import pause
# ? from MCP4922 import MCP4922 # ?
from RotaryEncoder import RotaryEncoder #* critical
from CV import CV #* critical
from NoteSequence import NoteSequence #* critical
from LEDSequence import LEDSequence
#! import pcf8574_io
# ? from InputSequencer import InputSequencer

from Env import SIMULATED_LCD, SIMULATED_DAC, MAX_STEP, MIN_STEP, MAX_TEMPO, MIN_TEMPO, MAX_OCTAVE, MIN_OCTAVE, MAX_PITCH, MIN_PITCH, MAX_CV,MIN_CV, MAX_DAC, LED_QUANTITY, PITCH_CHANNEL, CV1_CHANNEL, CV2_CHANNEL, CV3_CHANNEL, GATE_CHANNEL, NB_NOTES, NB_STEPS
#* check if all imports from Env.py are necessary

''' # ! NOT WORKING - REMOVE
if SIMULATED_LCD:
    LCD = Simulatelcd()  # ? or in SequencerMain
else:
    LCD = LCDSequencer() # ? or in SequencerMain
'''
#! uncomment next line if test (line 44-48) is unconclusive
#LCD = LCDSequencer()

class Sequencer:
    '''
        #* Sequencer class, every "physical" component is initialized here
    '''
    def __init__(self):

        ''' # ! NEEDED ?!
        self.portExpander = pcf8574_io.PCF(0x20) # ! set the correct I2C adress of the PCF8574
        self.pinPortExpander = ["p0","p1","p2","p3","p4","p5","p6","p7"]
        for i in self.pinPortExpander:
            self.portExpander.pin_mode(i,"INPUT") # sets all pins of the PCF8574 as INPUTs
        '''

        global LCD
        # ! to test:
        if SIMULATED_LCD:
            LCD = Simulatelcd()
        else:
            LCD = LCDSequencer()
        self.LCD = LCD

        self.noteSequence = NoteSequence(LCD)
        self.ledSequence = LEDSequence()

        # ? LCD.displayNote(self.noteSequence.listSteps[self.noteSequence.step][0], self.noteSequence.listSteps[self.noteSequence.step][1])

        self.button1 = gpiozero.Button(5) # physical pin 29
        self.buttonIncrOct = gpiozero.Button(13) #? physical pin 33
        self.buttonDecrOct = gpiozero.Button(16) #? physical pin 36
        #* self.buttonHearNote = gpiozero.Button(4000000) # physical pin ? (step RotaryEncoder button)
        #* self.buttonShowCV1 = gpiozero.Button(4000000) # physical pin ? (CV1 RE button)
        #* self.buttonShowCV2 = gpiozero.Button(4000000) # physical pin ? (CV2 RE button)
        #* self.buttonShowCV3 = gpiozero.Button(4000000) # physical pin ? (CV3 RE button)
        #* self.buttonShowTempo = gpiozero.Button(4000000) # physical pin ? (tempo RE button)
        #* self.buttonShowGate = gpiozero.Button(4000000) # physical pin ? (gate RE button)

        self.rotorPitch = RotaryEncoder(6, 12,"pitch") #! phsical pin ?
        self.rotorTempo = RotaryEncoder(27, 17, "tempo") # physical pin 11 and 13
        self.rotorGate = RotaryEncoder(14, 4, "gate/env") # physical pin 7 and 8
        self.rotorCV1 = RotaryEncoder(18, 15, "cv", 1) # physical pin 10 and 12
        self.rotorCV2 = RotaryEncoder(22, 23, "cv", 2) # physcial pin 15 and 16
        self.rotorCV3 = RotaryEncoder(24, 25, "cv", 3) # physical pin 18 and 22
        self.rotorStep = RotaryEncoder(26, 21,"step",) #! physical pin ?

        if SIMULATED_DAC:
            self.dac1 = Simulatedac(0, 0, 7) # could be a MCP4921, physical pin 29
            self.dac2 = Simulatedac(0, 0, 8) # physical pin 26
            self.dac3 = Simulatedac(0, 0, 9) # physical pin 24
        else:
            self.dac1 = DACSequencer(0, 1, 7, 1) # could be a MCP4921, physical pin 29
            self.dac2 = DACSequencer(0, 1, 8, 2) # physical pin 26
            self.dac3 = DACSequencer(0, 1, 9, 3) # physical pin 24
        self.dacs = [self.dac1,self.dac2,self.dac3]
        # need to open and close the spi bus every time we write to 1 dac


        self.cv1 = CV(1, self.dac2, LCD, 1) #? CV1_CHANNEL 
        self.cv2 = CV(2, self.dac3, LCD, 0) #? CV2_CHANNEL 
        self.cv3 = CV(3, self.dac3, LCD, 1) #? CV3_CHANNEL 

        #TODO add switches
        #! Play Pause will be coded as a button
        #* OR use a simple Button(pin) and use button.is_pressed (True if HIGH)
        #? self.switchClock = gpiozero.InputDevice(19) # set pin for the switch1 HIGH - physical pin 35
        #! self.switchPause = gpiozero.InputDevice(20) # set pin for the switch2 HIGH - physical pin 38
        # then use switchExample.is_active (True if HIGH or False if LOW)
         
        #! convert them to 3.3v - voltage divider or via the Logic Level Shifter ?
        # ? self.jackInputClock = InputSequencer(self.portExpander,self.pinPortExpander[0])
        # ? self.jackInputPlay = InputSequencer(self.portExpander,self.pinPortExpander[1])
        #! input jacks actually are switchPause and switchClock (they're physically connected together so the jacks act like the switches do)


    def showCV1(self): #TODO # shows this CV value when button is pressed
        LCD.displayCV(1,self.cv1.value)
        print("show CV1:", self.cv1.value)
    def showCV2(self): #TODO # shows this CV value when button is pressed
        LCD.displayCV(2,self.cv2.value)
        print("show CV2:", self.cv2.value)
    def showCV3(self): #TODO # shows this CV value when button is pressed
        LCD.displayCV(3,self.cv3.value)
        print("show CV3:", self.cv3.value)

    def playNote(self): #TODO # plays the current note (selected current step) when button is pressed
        currentOctave = self.noteSequence.listSteps[self.noteSequence.step][0] # octave of the current note
        currentPitch = self.noteSequence.listSteps[self.noteSequence.step][1] # pitch of the current note
        currentNote = MAX_DAC*(((currentOctave*12)+currentPitch)/NB_NOTES)
        self.dac1.setVoltage(PITCH_CHANNEL, int(currentNote))
        print("play current note:",currentPitch,currentOctave,currentNote)

