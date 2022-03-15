"""
TRANH201INFO3 sequencer test code
"""

#* import gpiozero # ?
from gpiozero import Device #*
from gpiozero.pins.mock import MockFactory #*
import time
import sys

# from Step import Step #Step class
from LCDSequencer import LCDSequencer #LCD class
from Simulatelcd import Simulatelcd #Simulated LCD class, for testing purposes and/or when not running on a RPi
# from DACSequencer import DACSequencer #DAC class
# from RotaryEncoder import RotaryEncoder #Rotary encoder class
# TODO from ClockSequencer import ClockSequencer # Clock class
# from LEDSequence import LEDSequence #LEDs Sequence class (8 LEDs)
from Sequencer import Sequencer
from Tempo import Tempo
from Gate import Gate
from Env import SIMULATED_LCD, SIMULATED_DAC


def main(): # Main function, activated when sequencer launched

    # ! -------------------
    # ! here below is for setting the pins from gpiozero as fake pins for testing purposes
    #gpiozero.Device.pin_factory = gpiozero.pins.mock.MockFactory()
    Device.pin_factory = MockFactory()
    print("------!-------MOCK PINS------!-------")
    # ! -------------------
    global sequencer
    sequencer = Sequencer()
    global lcd
    if SIMULATED_LCD:
        lcd = Simulatelcd()
    else:
        lcd = LCDSequencer()
    lcd.toggleBacklight(True)
    #lcd.test()

    global tempo
    tempo = Tempo(60, lcd) # initial tempo is 60 bpm
    global gate
    gate = Gate(sequencer.dac2, 0, lcd)

    #init_tempo = tempo.value
    #lcd.displayTempo(init_tempo)
    init_step = sequencer.noteSequence.step
    init_pitch = sequencer.noteSequence.note[sequencer.noteSequence.listSteps[sequencer.noteSequence.step][1]]
    init_octave = sequencer.noteSequence.listSteps[sequencer.noteSequence.step][0]
    lcd.displayStep(init_step, init_pitch, init_octave)

    '''
    note = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    l_steps = []
    for i in range(8): #création de la liste des notes
        l_steps.append([0, 1]) #cette liste représente l'octave 0 et la note 1
    '''

    '''
    def increase_pitch():
        print("test increase pitch")
    def decrease_pitch():
        print("test decrease pitch")
    sequencer.buttonIncrOct.when_pressed = increase_pitch # TODO ?
    sequencer.buttonDecrOct.when_pressed = decrease_pitch # TODO ?
    '''
    
    #* sequencer.button1.when_pressed = ?.on # TODO
    sequencer.buttonIncrOct.when_pressed = sequencer.noteSequence.increaseOctave #?
    sequencer.buttonDecrOct.when_pressed = sequencer.noteSequence.decreaseOctave #?
    #* sequencer.buttonHearNote.when_pressed = sequencer.playNote

    sequencer.rotorPitch.when_rotated_clockwise = sequencer.noteSequence.increasePitch
    sequencer.rotorPitch.when_rotated_counter_clockwise = sequencer.noteSequence.decreasePitch
    sequencer.rotorTempo.when_rotated_clockwise = tempo.increaseTempo
    sequencer.rotorTempo.when_rotated_counter_clockwise = tempo.decreaseTempo
    #* sequencer.rotorGate.when_rotated_clockwise = gate.increaseGate # TODO
    #* sequencer.rotorGate.when_rotated_counter_clockwise = gate.decreaseGate # TODO
    sequencer.rotorCV1.when_rotated_clockwise = sequencer.cv1.increaseCV
    sequencer.rotorCV1.when_rotated_counter_clockwise = sequencer.cv1.decreaseCV
    sequencer.rotorCV2.when_rotated_clockwise = sequencer.cv2.increaseCV
    sequencer.rotorCV2.when_rotated_counter_clockwise = sequencer.cv2.decreaseCV
    sequencer.rotorCV3.when_rotated_clockwise = sequencer.cv3.increaseCV
    sequencer.rotorCV3.when_rotated_counter_clockwise = sequencer.cv3.decreaseCV
    sequencer.rotorStep.when_rotated_clockwise = sequencer.noteSequence.increaseStep
    sequencer.rotorStep.when_rotated_counter_clockwise = sequencer.noteSequence.decreaseStep

    '''
    for i in range(5):
        time.sleep(1)
        print("TEST")
    raise SystemExit
    '''

    # sequence led, sequence gate send following tempo

    ''' for testing :
    for p in range (10): # does the step sequence 10 times
        for i in range(0,7):
            #* gate.sendGateSignal(tempo)
            pitchDAC = 4096*(l_steps[i][1]/12) # need to add octaves
            sequencer.dac1.setVoltage(0, pitchDAC)
            time.sleep(60/tempo.value)
    '''
    while True: # works at the same time as the rotary encoders are turning and changing values
        print("testing")
        time.sleep(3)


def endSequencer():
    # Set the DACs to 0V and turns the LCD backlight off (executed when keyboard interrupt or other)
    global sequencer
    global lcd
    for dac in sequencer.dacs:
        for i in range(2):
            dac.output.setVoltage(i, 0)
            print("---DAC", dac.number,"channel",i,"set to 0---")
    lcd.toggleBacklight(False)
    # print("LCD Backlight turned OFF")
    print("==========Sequencer ended==========")


if __name__ == "__main__":
    # launch main() if this file is launched (SequencerMain.py)
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as error:  # catches a keyboard interrupt or a raised system exit (raise KeyboardInterrupt OR raise SystemExit("_Ending program_") OR sys.exit("_Ending program_"))
        print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n"+error.__class__.__name__ +
              ", stopping sequencer\n\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
        #endSequencer() # stops the sequencer
    finally:
        print("========Ending Sequencer========")
        endSequencer() # stops the sequencer
        sys.exit(0)


