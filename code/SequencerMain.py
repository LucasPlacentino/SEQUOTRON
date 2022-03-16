"""
TRANH201INFO3 sequencer main file
"""

from gpiozero import Device #* for testing
from gpiozero.pins.mock import MockFactory #* for testing
import time
import sys
# ? import threading # ?
# ? from signal import pause # ?

from LCDSequencer import LCDSequencer#? #LCD class
from Simulatelcd import Simulatelcd#? #Simulated LCD class, for testing purposes and/or when not running on a RPi
from Sequencer import Sequencer #* critical
from Tempo import Tempo #* critical
from Gate import Gate #* critical

#? :
from Env import SIMULATED_LCD, SIMULATED_DAC


def main(): # Main function, activated when sequencer launched/file run

    # ! here below is for setting the pins from gpiozero as fake pins for testing purposes
    #gpiozero.Device.pin_factory = gpiozero.pins.mock.MockFactory()
    #Device.pin_factory = MockFactory()
    #print("------!-------MOCK PINS------!-------")
    # ! -------------------

    global sequencer
    sequencer = Sequencer()
    global lcd
    #! test:
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
    tempo = Tempo(60, lcd) # initial tempo is 60 bpm
    global gate
    gate = Gate(sequencer.dac2, 0, lcd)

    # Splash screen:
    lcd.splashScreen() # TODO
    time.sleep(3) # ? 3 seconds ?
    lcd.fullClearLCD()

    # Asking user if they want to load a saved sequence:
    # TODO

    # Show default main screen:
    init_tempo = tempo.value
    lcd.displayTempo(init_tempo)
    init_step = sequencer.noteSequence.step
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
    #*sequencer.rotorGate.rotor.when_rotated_clockwise = gate.increaseGate # ! makes the script end when uncommented?
    #*sequencer.rotorGate.rotor.when_rotated_counter_clockwise = gate.decreaseGate # ! makes the script end when uncommented?
    sequencer.rotorCV1.rotor.when_rotated_clockwise = sequencer.cv1.increaseCV
    sequencer.rotorCV1.rotor.when_rotated_counter_clockwise = sequencer.cv1.decreaseCV
    sequencer.rotorCV2.rotor.when_rotated_clockwise = sequencer.cv2.increaseCV
    sequencer.rotorCV2.rotor.when_rotated_counter_clockwise = sequencer.cv2.decreaseCV
    sequencer.rotorCV3.rotor.when_rotated_clockwise = sequencer.cv3.increaseCV
    sequencer.rotorCV3.rotor.when_rotated_counter_clockwise = sequencer.cv3.decreaseCV
    sequencer.rotorStep.rotor.when_rotated_clockwise = sequencer.noteSequence.increaseStep
    sequencer.rotorStep.rotor.when_rotated_counter_clockwise = sequencer.noteSequence.decreaseStep
    

    
    while True: # works at the same time as the rotary encoders are turning and changing values
        print("testing")
        time.sleep(5)
        #on() # FOR TESTING

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

def on(): # plays the sequence #! CAN BE PUT IN A CLASS ?
    tempo.on = "on"
    #* while sequencer.button1.is_pressed: # ?
    while tempo.on == "on": # Clock of sequencer: # TODO
        pitch = sequencer.noteSequence.listSteps[sequencer.noteSequence.step][1]
        octave = sequencer.noteSequence.listSteps[sequencer.noteSequence.step][0]
        sequencer.dac1.output.setVoltage(1, 12*int(octave) + int(pitch)) # ! WHICH DAC ?
        
        print("----step start----")
        
        # start gate
        sequencer.dac2.output.setVoltage(1, 4095) # ! WHICH DAC ?
        time.sleep((60/tempo.value)*(gate.value)) # ?
        
        # end gate
        sequencer.dac2.output.setVoltage(1, 0) # ! WHICH DAC ?
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
        tempo.step = tempo.step%8
        if sequencer.button1.is_pressed == False:
            off()


def endSequencer():
    # Set the DACs to 0V and turns the LCD backlight off (executed when keyboard interrupt or other)
    global sequencer
    global lcd
    for dac in sequencer.dacs:
        for i in range(2):
            dac.output.setVoltage(i, 0)
            print("---DAC", dac.number,"channel",i,"set to 0---")
    lcd.fullClearLCD()
    lcd.toggleBacklight(False)
    # print("LCD Backlight turned OFF")
    print("==========Sequencer ended==========")


if __name__ == "__main__":
    # launch main() if this file is launched/run (SequencerMain.py)
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


