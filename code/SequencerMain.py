"""
TRANH201INFO3 sequencer test code
"""

import gpiozero
import time

from Step import Step #Step class
#from LCDSequencer import LCDSequencer #LCD class
from Simulatelcd import Simulatelcd #Simulated LCD class, for testing purposes and/or when not running on a RPi
from DACSequencer import DACSequencer #DAC class
from RotaryEncoder import RotaryEncoder #Rotary encoder class
from ClockSequencer import ClockSequencer #Clock class
from LEDSequence import LEDSequence #LEDs Sequence class (8 LEDs)

class Tempo: # needs to be changed ?
    # Tempo
    def __init__(self, current_tempo):
        self.current_tempo = current_tempo
    def changeTempo(self, new_tempo):
        self.current_tempo=new_tempo

class Clock: # needs to be changed
    # Clock
    def __init__(self):
        pass
    def ticking(self, tempo):
        print("tick")
        clock=0
        #time.sleep(60/self.tempo.current_tempo)
        #send a clock signal
        print("tack")
        clock=1
        time.sleep(60/tempo.current_tempo)


def main(): # Main function
    lcd = Simulatelcd() # initialization of a simulated LCD, to use when running the program outside of a RPi, it will just print out rather than display on the LCD
    #lcd = LCDSequencer.LCDSequencer() # LCD initialization
    tempo = Tempo(60) # Tempo initialization (default 60 bpm)
    #clock = Clock(tempo) # Clock initialization
    clock = ClockSequencer() # Clock initialization
    ledSequence = LEDSequence(8) # LEDs Sequence initialization (8 LEDs)

    #lcd.toggleBacklight(True) # Turns the backlight ON
    lcd.displayTempo(tempo.current_tempo) # shows the current tempo

    for i in range(1,5):
        # Start of the tick tack sequence (10 times)
        clock.ticking(tempo)
    
    tempo.changeTempo(120)
    lcd.displayTempo(tempo.current_tempo)

    for i in range(1,5):
        # Start of the tick tack sequence (10 times)
        clock.ticking(tempo)

    lcd.toggleBacklight(False) # Turns the backlight OFF for the end of the program

    ''' Test code on RPi
    lcd.displayNote("A#",4)
    lcd.displayTempo(100)
    step7 = Step(7)
    time.sleep(5)
    lcd.displayStep(step7)
    time.sleep(5)
    lcd.clearLCD()
    lcd.toggleBacklight(False)
    '''

if __name__ == "__main__": 
    main()
    # launch main() if this file is launched (SequencerMain.py)


#led1 = gpiozero.LED(17)

