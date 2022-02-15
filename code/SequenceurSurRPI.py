from gpiozero import *
import time
import spidev
from signal import pause  # ?
from MCP4922 import MCP4922

'''
    TODO:
        add buttons
        add LCD screen
        add other DAC
        incorporate this code into the rest -> OOP
        ...
'''

#button1 = Button(5) #29
#button2 = Button(38) #31
#button3 = Button(40) #32

rotor1 = RotaryEncoder(4, 14) # 7 & 8 (gate)
rotor2 = RotaryEncoder(15, 18) # 10 & 12 (CV1)
rotor3 = RotaryEncoder(17, 27) # 11 & 13 (tempo)
rotor4 = RotaryEncoder(22, 23) # 15 & 16 (CV2)
rotor5 = RotaryEncoder(24, 25) # 18 & 22 (CV3)
rotor6 = RotaryEncoder(6, 12) #31 & 32 (pitch)


"""
led1 = LED(27) #13
led2 = LED(23) #15
led3 = LED(22) #16

l_led = [led1,led2,led3]
"""

dac1 = MCP4922(0, 0, 8) #24 (is a 4921 but can also work as a 4922?)
dac2 = MCP4922(0, 0, 7) #26
#dac3 = MCP4922(0, 0, 8) #24 TODO change gpio


note = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
l_step = []
for i in range(8): #creates the notes list
    l_step.append([0, 1]) #represents the octave & the note


MAX_STEP = 7
MIN_STEP = 0
MAX_TEMPO = 359
MIN_TEMPO = 2
MAX_OCTAVE = 4
MIN_OCTAVE = 0
MAX_PITCH = 12
MIN_PITCH = 1
MAX_CV = 25


class Tempo:
    value = 100

tempo = Tempo()


class Step:
    n = 0 #position in the list to modify

step = Step()


class CV:
    CV1 = 0
    CV2 = 0
    CV3 = 0
    Gate = 1
    
CV = CV()


def led(n):
    n.on()
    time.sleep(60/tempo.value)
    n.off()


def led_note():
    octave = str(l_step[step.n][0])
    pitch = note[l_step[step.n][1]-1]
    return "Note : " + pitch + octave


def increase_step():
    step.n += 1
    step.n = step.n%MAX_STEP
    print("Step : " + str(step.n))


def decrease_step():
    if step.n == MIN_STEP: # step.pitch
        step.n = MAX_STEP
    else:
        step.n -= 1
    print("Step : " + str(step.n))


def increase_pitch():
    if l_step[step.n][1] == MAX_PITCH:
        l_step[step.n][0] += 1
        l_step[step.n][0] = l_step[step.n][0]%(MAX_OCTAVE + 1)
        l_step[step.n][1] += 1
    l_step[step.n][1] += 1
    l_step[step.n][1] = l_step[step.n][1]%(MAX_PITCH + 1)
    print(led_note())
    dac1.setVoltage(0,int(4096*(((l_step[step.n][0]*12)+l_step[step.n][1])/60)))


def decrease_pitch():
    if l_step[step.n][1] == MIN_PITCH:
        l_step[step.n][1] = MAX_PITCH
        if l_step[step.n][0] == MIN_OCTAVE:
            l_step[step.n][0] = MAX_OCTAVE
        else:
            l_step[step.n][0] -= 1
    else:
        l_step[step.n][1] -= 1
    print(led_note())
    dac1.setVoltage(0,int(4096*(((l_step[step.n][0]*12)+l_step[step.n][1])/60)))


def increase_octave():
    l_step[step.n][0] += 1
    l_step[step.n][0] = l_step[step.n][0]%(MAX_OCTAVE + 1)
    #print(led_note())
    #TODO update dac


def decrease_octave():
    if l_step[step.n][0] == MIN_OCTAVE:
        l_step[step.n][0] = MAX_OCTAVE
    else:
        l_step[step.n][0] -= 1
    #print(led_note())
    #TODO update dac


def increase_tempo():
    if tempo.value < MAX_TEMPO:
        tempo.value += 1
    print("Tempo:",tempo.value)


def decrease_tempo():
    if tempo.value > MIN_TEMPO:
        tempo.value -= 1
    print("Tempo",tempo.value)


def increase_CV1():
    CV.CV1 += 1
    CV.CV1 = CV.CV1%MAX_CV
    dac1.setVoltage(1, int(float(4096)*CV.CV1/24))
    print("CV1:",CV.CV1)


def increase_CV2():
    CV.CV2 += 1
    CV.CV2 = CV.CV2%MAX_CV
    dac2.setVoltage(0, int(float(4096)*CV.CV2/24))
    print("CV2:",CV.CV2)


def increase_CV3():
    CV.CV3 += 1
    CV.CV3 = CV.CV3%MAX_CV
    dac2.setVoltage(1, int(float(4096)*CV.CV3/24))
    print("CV3:",CV.CV3)


def decrease_CV1():
    if CV.CV1 == 0:
        CV.CV1 = 24
    else:
        CV.CV1 -= 1
    dac1.setVoltage(1, int(float(4096)*CV.CV1/24))
    print("CV1:",CV.CV1)


def decrease_CV2():
    if CV.CV2 == 0:
        CV.CV2 = 24
    else:
        CV.CV2 -= 1
    dac2.setVoltage(0, int(float(4096)*CV.CV2/24))
    print("CV2:",CV.CV2)


def decrease_CV3():
    if CV.CV3 == 0:
        CV.CV3 = 24
    else:
        CV.CV3 -= 1
    dac2.setVoltage(1, int(float(4096)*CV.CV3/24))
    print("CV3:",CV.CV3)


def increase_Gate():
    if CV.Gate >= 0.95:
        CV.Gate = 0
    else:
        CV.Gate += 0.1
    #dac3.setVoltage(1, int(4096*CV.Gate))
    print("Gate:",round(CV.Gate,1))
    #TODO update dac correctly timed
    

def decrease_Gate():
    if CV.Gate <= 0.05:
        CV.Gate = 1
    else:
        CV.Gate -= 0.1
    #dac3.setVoltage(1, int(4096*CV.Gate))
    print("Gate:",round(CV.Gate,1))
    #TODO update dac correctly timed


''' TODO add a button/switch/keyboard interrupt ?
def on():
    p = 'on'
    while p == 'on':
        for i in range(8):
            dac3.setVoltage(1, 12*l_step[i][0] + l_step[i][1]) 
            # led(l_led[i])
            time.sleep(60/tempo.value)
        if not button1.is_pressed:
            p = 'off'
    #if keyboard interrupt:
        #(led off)
        #break
'''
# C0 - (B#4) - C5

#button1.when_pressed = on
#button2.when_pressed = increase_octave
#button3.when_pressed = decrease_octave


rotor1.when_rotated_clockwise = increase_pitch
rotor1.when_rotated_counter_clockwise = decrease_pitch
rotor2.when_rotated_clockwise = increase_CV1
rotor2.when_rotated_counter_clockwise = decrease_CV1
rotor3.when_rotated_clockwise = increase_Gate
rotor3.when_rotated_counter_clockwise = decrease_Gate
rotor4.when_rotated_clockwise = increase_CV2
rotor4.when_rotated_counter_clockwise = decrease_CV2
rotor5.when_rotated_clockwise = increase_CV3
rotor5.when_rotated_counter_clockwise = decrease_CV3
rotor6.when_rotated_clockwise = increase_tempo
rotor6.when_rotated_counter_clockwise = decrease_tempo


pause()  # TODO ?