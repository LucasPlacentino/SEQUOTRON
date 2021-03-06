"""
TRANH201INFO3 sequencer main file

Ideally launched on RPi startup

KeyboardInterrupt to exit program and shutdown components

Use "Better Comments" extension on VSCode to see comments colored accordingly 
(#*)
(#!)
(#?)

"""

from gpiozero import Device #* for testing
from gpiozero.pins.mock import MockFactory #* for testing
import time #* critical
import sys #* critical
# ? import threading # ?

from signal import pause # ? is pause() needed ?

#? from LCDSequencer import LCDSequencer#? #LCD class not needed (in Sequencer)
#? from Simulatelcd import Simulatelcd#? #Simulated LCD class, for testing purposes and/or when not running on a RPi
from Sequencer import Sequencer #* critical
from Tempo import Tempo #* critical
from Gate import Gate #* critical

from ClockSequencer import ClockSequencer # ? need some testing

import threading
import logging

from Env import PITCH_CHANNEL, GATE_CHANNEL, MAX_DAC, NB_NOTES, NB_STEPS, STARTUP_SEQUENCE, MOCK_PINS
#* check if all imports from Env.py are necessary/present


def main(): # Main function, activated when sequencer launched/file run

    # ! here below is for setting the pins from gpiozero as fake pins for testing purposes
    if MOCK_PINS:
        gpiozero.Device.pin_factory = gpiozero.pins.mock.MockFactory()
        Device.pin_factory = MockFactory()
        print("------!-------MOCK PINS------!-------")
    else:
        print("--- using real pins ---")
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
    #clock = ClockSequencer(sequencer, tempo, gate) # check line 91

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

    
    #sequencer.buttonDecrOct.when_pressed = lcd.test #* USED FOR TESTING

    # PLAY/PAUSE :
    sequencer.button1.when_pressed = threadOn
    #! testing :
    #sequencer.button1.when_pressed = clock.playClock # check line 68

    # OCTAVES :
    sequencer.buttonIncrOct.when_pressed = sequencer.noteSequence.increaseOctave #?
    sequencer.buttonDecrOct.when_pressed = sequencer.noteSequence.decreaseOctave #?

    # TRIGGER/HEARNOTE : # TODO
    # TODO sequencer.buttonHearNote.when_pressed = sequencer.playNote

    # PITCH :
    sequencer.rotorPitch.rotor.when_rotated_clockwise = sequencer.noteSequence.increasePitch
    sequencer.rotorPitch.rotor.when_rotated_counter_clockwise = sequencer.noteSequence.decreasePitch

    # TEMPO :
    sequencer.rotorTempo.rotor.when_rotated_clockwise = tempo.increaseTempo
    sequencer.rotorTempo.rotor.when_rotated_counter_clockwise = tempo.decreaseTempo

    # GATE :
    sequencer.rotorGate.rotor.when_rotated_clockwise = gate.increaseGate
    sequencer.rotorGate.rotor.when_rotated_counter_clockwise = gate.decreaseGate

    # CV 1 :
    sequencer.rotorCV1.rotor.when_rotated_clockwise = sequencer.cv1.increaseCV
    sequencer.rotorCV1.rotor.when_rotated_counter_clockwise = sequencer.cv1.decreaseCV

    # CV 2 :
    sequencer.rotorCV2.rotor.when_rotated_clockwise = sequencer.cv2.increaseCV
    sequencer.rotorCV2.rotor.when_rotated_counter_clockwise = sequencer.cv2.decreaseCV

    # CV 3 :
    sequencer.rotorCV3.rotor.when_rotated_clockwise = sequencer.cv3.increaseCV
    sequencer.rotorCV3.rotor.when_rotated_counter_clockwise = sequencer.cv3.decreaseCV

    # STEP :
    sequencer.rotorStep.rotor.when_rotated_clockwise = sequencer.noteSequence.increaseStep
    sequencer.rotorStep.rotor.when_rotated_counter_clockwise = sequencer.noteSequence.decreaseStep
    
    pause() # ?


# Functions :

def off(): # pauses the sequence
    global tempo
    tempo.on = "off"

def threadOn():
    threadClock = threading.Thread(target=on)
    threadClock.start()

def on(): # plays the sequence #! CAN BE PUT IN A CLASS ?  # ! THREAD NEEDED ?
    global tempo
    tempo.on = "on"
    #* while sequencer.button1.is_pressed: # ?
    while tempo.on == "on": # Clock of sequencer:
        pitch = sequencer.noteSequence.listSteps[tempo.step][1]
        octave = sequencer.noteSequence.listSteps[tempo.step][0]
        # change note each step
        sequencer.dac1.output.open()
        sequencer.dac1.output.setVoltage(PITCH_CHANNEL, int(MAX_DAC*((12*int(octave) + int(pitch))/NB_NOTES))) # ! CORRECT DAC ?
        sequencer.dac1.output.close()
        print("step", tempo.step+1, "note to dac1 channel0:", pitch, octave)        
        
        print("----step start----")
        
        sequencer.ledSequence.ledOn(tempo.step)
        
        # start gate
        sequencer.dac2.output.open()
        sequencer.dac2.output.setVoltage(GATE_CHANNEL, MAX_DAC) # ! CORRECT DAC ?
        sequencer.dac2.output.close()
        print("Gate value:", gate.value)
        time.sleep((60/tempo.value)*(gate.value)) # ?
        
        # end gate
        sequencer.dac2.output.open()
        sequencer.dac2.output.setVoltage(GATE_CHANNEL, 0) # ! CORRECT DAC ?
        sequencer.dac2.output.close()
        time.sleep((60/tempo.value)*(1-gate.value)) # ?
        
        print("----step ended----")

        tempo.step += 1
        tempo.step = tempo.step%NB_STEPS # if tempo.step == NB_STEPS : tempo.step == 0

        if sequencer.button1.is_pressed == False: # switch is on position "pause" (off)
            off()

def startupSequence():
    global sequencer
    global tempo
    global gate
    notes = STARTUP_SEQUENCE

    print("Startup sequence")

    for current_note in notes:
        sequencer.dac1.output.open()
        sequencer.dac1.output.setVoltage(PITCH_CHANNEL, int(MAX_DAC*((12*int(current_note[0]) + int(current_note[1]))/NB_NOTES)))  # ! CORRECT DAC ?
        sequencer.dac1.output.close()
        print("note to dac1 channel0:", current_note[1], current_note[0])        
        
        # start gate
        sequencer.dac2.output.open()
        sequencer.dac2.output.setVoltage(GATE_CHANNEL, MAX_DAC) # ! CORRECT DAC ?
        sequencer.dac2.output.close()
        print("Gate value:", gate.value)
        time.sleep((60/tempo.value)*(gate.value)) # ?
        
        # end gate
        sequencer.dac2.output.open()
        sequencer.dac2.output.setVoltage(GATE_CHANNEL, 0) # ! CORRECT DAC ?
        sequencer.dac2.output.close()
        time.sleep((60/tempo.value)*(1-gate.value)) # ?
    
    sequencer.dac1.output.open()
    sequencer.dac1.output.setVoltage(PITCH_CHANNEL, 0)
    sequencer.dac1.output.close()

    print("startup sequence ended")


def endSequencer():
    # Set the DACs to 0V and turns the LCD backlight off (executed when keyboard interrupt or other)
    global sequencer
    global lcd
    for dac in sequencer.dacs:
        for i in range(2):
            dac.output.open()
            print("DAC", dac.number, "SPI opened")
            dac.output.setVoltage(i, 0)
            print("DAC", dac.number, "voltage 0")
            #!dac.output.shutdown(i) # ? 
            dac.output.close()
            print("DAC", dac.number, "SPI closed")
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
    except (KeyboardInterrupt, SystemExit) as exit:  # catches a keyboard interrupt or a raised system exit (raise KeyboardInterrupt OR raise SystemExit("_Ending program_") OR sys.exit("_Ending program_"))
        print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n"+exit.__class__.__name__ +
              ", stopping sequencer\n\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
        #endSequencer() # stops the sequencer #* moved to finally:
    except Exception as error: # catches all other errors
        print("\n###### ERROR ######", error.__class__.__name__, "\n")
        print(error)
        print("\n######################\n")
        logging.error('Unexpected error: {0}'.format(error))
    finally:
        print("========Ending Sequencer========")
        endSequencer() # stops the sequencer
        sys.exit(0) # ends the script (with code 0)


