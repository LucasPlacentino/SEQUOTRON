
#! NOT NECESSARY

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