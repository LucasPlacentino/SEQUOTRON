"""
TRANH201INFO3 sequencer test code
"""

import gpiozero
import time

class Tempo:
    # Tempo
    current_tempo = 60
    def changeTempo(self, nouveau_tempo):
        self.current_tempo=nouveau_tempo

tempo = Tempo() # Tempo initialization

class Clock:
    # Clock
    def ticking(self):
        print("tick")
        clock=0
        time.sleep(60/tempo.current_tempo)
        print("tack")
        clock=1
        time.sleep(60/tempo.current_tempo)

clock = Clock() # Clock initialization

for i in range(1,10):
    # Start of the tick tack sequence (10 times)
    clock.ticking()




#led1 = gpiozero.LED(17)

