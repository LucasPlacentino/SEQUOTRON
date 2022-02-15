import time

class ClockSequencer:         # TODO

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

    def ticking(self, tempo):
        #sends the clock signal
        if self.internal:
            print("tick")
            clock = 1
            #time.sleep(60/self.tempo.current_tempo)
            #send a clock signal
            time.sleep(60/tempo.current_tempo)
            clock = 0
        else:
            #external clock
            pass