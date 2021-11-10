"""
TRANH201INFO3 sequencer test code
"""

import gpiozero
import time

class Tempo:
    # Tempo
    def __init__(self, current_tempo):
        self.current_tempo = current_tempo
    def changeTempo(self, nouveau_tempo):
        self.current_tempo=nouveau_tempo

class Clock:
    # Clock
    def __init__(self, tempo):
        self.tempo = tempo
    def ticking(self):
        print("tick")
        clock=0
        time.sleep(60/self.tempo.current_tempo)
        print("tack")
        clock=1
        time.sleep(60/self.tempo.current_tempo)


def main():
    tempo = Tempo(60) # Tempo initialization
    clock = Clock(tempo) # Clock initialization

    for i in range(1,10):
        # Start of the tick tack sequence (10 times)
        clock.ticking()

if __name__ == "__main__":
    main()





#led1 = gpiozero.LED(17)

