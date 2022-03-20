"""
TRANH201INFO3 sequencer main file
"""

from gpiozero import Device #* for testing
from gpiozero.pins.mock import MockFactory #* for testing
import time
import sys
# ? import threading # ?

from signal import pause # ?

from LCDSequencer import LCDSequencer#? #LCD class not needed (in Sequencer)
from Simulatelcd import Simulatelcd#? #Simulated LCD class, for testing purposes and/or when not running on a RPi
from Sequencer import Sequencer #* critical
from Tempo import Tempo #* critical
from Gate import Gate #* critical

# from ClockSequencer import ClockSequencer # ? testing

#? :
from Env import SIMULATED_LCD, SIMULATED_DAC, PITCH_CHANNEL, GATE_CHANNEL, MAX_DAC, NB_NOTES, NB_STEPS, STARTUP_SEQUENCE


def main(): # Main function, activated when sequencer launched/file run

    # ! here below is for setting the pins from gpiozero as fake pins for testing purposes
    # ! comment when testing has ended
    #gpiozero.Device.pin_factory = gpiozero.pins.mock.MockFactory()
    #Device.pin_factory = MockFactory()
    #print("------!-------MOCK PINS------!-------")
    # ! -------------------

    global sequencer
    sequencer = Sequencer()
    global lcd
    #! test: works
    lcd = sequencer.LCD # ? need in Sequencer self.lcd = LCD ?
    # as opposed to:
    '''
    if SIMULATED_LCD:
        lcd = Simulatelcd()
    else:
        lcd = LCDSequencer()
        print("uevbu") # test
    '''
    #? lcd.toggleBacklight(True)
    #lcd.test() # tests the lcd

    global tempo
    tempo = Tempo(120, lcd) # initial tempo is 60 bpm
    print("tempo initialized", tempo.value)
    global gate
    gate = Gate(sequencer.dac2, 0, lcd)
    print("gate initialized", gate.value)

    # test :
    #clock = ClockSequencer(sequencer, tempo, gate)

    # Splash screen and startup sequence:
    lcd.splashScreen() # splash screen
    startupSequence() # startup sequence
    lcd.fullClearLCD() # clears lcd

    # Asking user if they want to load a saved sequence:
    # TODO

    # Show default main screen:
    init_tempo = tempo.value
    lcd.displayTempo(init_tempo)
    init_step = sequencer.noteSequence.step + 1
    init_pitch = sequencer.noteSequence.note[sequencer.noteSequence.listSteps[sequencer.noteSequence.step][1]]
    init_octave = sequencer.noteSequence.listSteps[sequencer.noteSequence.step][0]
    lcd.displayStep(init_step, init_pitch, init_octave)

    
    #sequencer.buttonDecrOct.when_pressed = lcd.test #* FOR TESTING

    sequencer.button1.when_pressed = on # TODO
    sequencer.buttonIncrOct.when_pressed = sequencer.noteSequence.increaseOctave #?
    sequencer.buttonDecrOct.when_pressed = sequencer.noteSequence.decreaseOctave #?
    #* sequencer.buttonHearNote.when_pressed = sequencer.playNote

    sequencer.rotorPitch.rotor.when_rotated_clockwise = sequencer.noteSequence.increasePitch
    sequencer.rotorPitch.rotor.when_rotated_counter_clockwise = sequencer.noteSequence.decreasePitch
    sequencer.rotorTempo.rotor.when_rotated_clockwise = tempo.increaseTempo
    sequencer.rotorTempo.rotor.when_rotated_counter_clockwise = tempo.decreaseTempo
    sequencer.rotorGate.rotor.when_rotated_clockwise = gate.increaseGate # ! makes the script end when uncommented?
    sequencer.rotorGate.rotor.when_rotated_counter_clockwise = gate.decreaseGate # ! makes the script end when uncommented?
    sequencer.rotorCV1.rotor.when_rotated_clockwise = sequencer.cv1.increaseCV
    sequencer.rotorCV1.rotor.when_rotated_counter_clockwise = sequencer.cv1.decreaseCV
    sequencer.rotorCV2.rotor.when_rotated_clockwise = sequencer.cv2.increaseCV
    sequencer.rotorCV2.rotor.when_rotated_counter_clockwise = sequencer.cv2.decreaseCV
    sequencer.rotorCV3.rotor.when_rotated_clockwise = sequencer.cv3.increaseCV
    sequencer.rotorCV3.rotor.when_rotated_counter_clockwise = sequencer.cv3.decreaseCV
    sequencer.rotorStep.rotor.when_rotated_clockwise = sequencer.noteSequence.increaseStep
    sequencer.rotorStep.rotor.when_rotated_counter_clockwise = sequencer.noteSequence.decreaseStep
    

    
    #while True: # works at the same time as the rotary encoders are turning and changing values
    #    print("testing")
    #    time.sleep(5)
        #on() # FOR TESTING

    pause()

''' for testing purposes
def setvoltage(a):
    #dac3.setVoltage(1, 12*l_step[tempo.n][0] + l_step[tempo.n][1])
    print("GATE ON TEST",a)
    #dac3.setVoltage(1, 0)
    print(tempo.step,a)
'''

def off(): # pauses the sequence
    tempo.on = "off"

''' for testing purposes
def setvoltage2(test):
    print("TEST GATE dac ON")
    time.sleep((60/tempo.value)*(gate.value))
    print("TEST GATE dac OFF")
    time.sleep((60/tempo.value)*(1-gate.value))
'''

def on(): # plays the sequence #! CAN BE PUT IN A CLASS ?  # ! THREAD NEEDED ?
    tempo.on = "on"
    #* while sequencer.button1.is_pressed: # ?
    while tempo.on == "on": # Clock of sequencer:
        pitch = sequencer.noteSequence.listSteps[tempo.step][1]
        octave = sequencer.noteSequence.listSteps[tempo.step][0]
        # change note each step
        sequencer.dac1.output.setVoltage(PITCH_CHANNEL, int(MAX_DAC*((12*int(octave) + int(pitch))/NB_NOTES))) # ! WHICH DAC ?
        print("step", tempo.step, "note to dac1 channel0:", pitch, octave)        
        
        print("----step start----")
        
        sequencer.ledSequence.ledOn(tempo.step)
        
        # start gate
        sequencer.dac2.output.setVoltage(GATE_CHANNEL, MAX_DAC) # ! WHICH DAC ?
        print("Gate value:", gate.value)
        time.sleep((60/tempo.value)*(gate.value)) # ?
        
        # end gate
        sequencer.dac2.output.setVoltage(GATE_CHANNEL, 0) # ! WHICH DAC ?
        time.sleep((60/tempo.value)*(1-gate.value)) # ?
        
        print("----step ended----")
        ''' test
        t1 = threading.Timer((60/tempo.value)*(1-gate.value), setvoltage)
        t1.run()
        time.sleep((60/tempo.value)*(gate.value))
        t2 = threading.Thread(setvoltage2)
        t2.run()
        #dac3.setVoltage(1, 0)
        print("Set Voltage test")
        '''
        tempo.step += 1
        tempo.step = tempo.step%NB_STEPS
        if sequencer.button1.is_pressed == False:
            off()

def startupSequence():
    global sequencer
    global tempo
    global gate
    notes = STARTUP_SEQUENCE
    print("Startup sequence")
    i = 0
    for p in notes:
        sequencer.dac1.output.setVoltage(PITCH_CHANNEL, int(MAX_DAC*((12*int(notes[i][0]) + int(notes[i][1]))/NB_NOTES))) # ! WHICH DAC ?
        print("note to dac1 channel0:", notes[i][1], notes[i][0])        
        
        # start gate
        sequencer.dac2.output.setVoltage(GATE_CHANNEL, MAX_DAC) # ! WHICH DAC ?
        print("Gate value:", gate.value)
        time.sleep((60/tempo.value)*(gate.value)) # ?
        
        # end gate
        sequencer.dac2.output.setVoltage(GATE_CHANNEL, 0) # ! WHICH DAC ?
        time.sleep((60/tempo.value)*(1-gate.value)) # ?
        
        i += 1
    sequencer.dac1.output.setVoltage(PITCH_CHANNEL, 0)
    print("startup sequence ended")


def endSequencer():
    # Set the DACs to 0V and turns the LCD backlight off (executed when keyboard interrupt or other)
    global sequencer
    global lcd
    for dac in sequencer.dacs:
        for i in range(2):
            dac.output.setVoltage(i, 0)
            #!dac.output.shutdown(i) # ? 
            print("---DAC", dac.number,"channel",i,"set to 0---")
    sequencer.ledSequence.turnAllLedOff()
    lcd.fullClearLCD()
    lcd.toggleBacklight(False)
    # print("LCD Backlight turned OFF")
    print("==========Sequencer ended==========")


if __name__ == "__main__":
    # launch main() if this file is launched/run (SequencerMain.py)
    #main() #uncomment to see other errors
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as error:  # catches a keyboard interrupt or a raised system exit (raise KeyboardInterrupt OR raise SystemExit("_Ending program_") OR sys.exit("_Ending program_"))
        print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n"+error.__class__.__name__ +
              ", stopping sequencer\n\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
        #endSequencer() # stops the sequencer #* moved to finally:
    finally:
        print("========Ending Sequencer========")
        endSequencer() # stops the sequencer
        sys.exit(0) # exits the interpreter ? ends the script (with code 0)


