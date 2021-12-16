from gpiozero import *
import time
import spidev
from signal import pause
from MCP4922 import MCP4922


#button1 = Button(5) #29
#button2 = Button(38) #31
#button3 = Button(40) #32

rotor1 = RotaryEncoder(4, 14) # 7 et 8 (gate)
rotor2 = RotaryEncoder(15, 18) # 10 et 12 (CV1)
rotor3 = RotaryEncoder(17, 27) # 11 et 13 (tempo)
rotor4 = RotaryEncoder(22, 23) # 15 et 16 (CV2)
rotor5 = RotaryEncoder(24, 25) # 18 et 22 (CV3)
rotor6 = RotaryEncoder(6, 12) #31 et 32 (pitch)


"""
led1 = LED(27) #13
led2 = LED(23) #15
led3 = LED(22) #16

l_led = [led1,led2,led3]
"""

dac1 = MCP4922(0, 0, 8) #24 (4921 mais ca peut aussi fonctionner en 4922)
dac2 = MCP4922(0, 0, 7) #26
#dac3 = MCP4922(0, 0, 8) #24


note = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
l_step = []
for i in range(8): #creation de la liste des notes
    l_step.append([0, 1]) #cette liste represente l'octave et la note


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
    valeur = 100

tempo = Tempo()


class Step:
    n = 0 #indice de la liste a modifier

step = Step()


class CV:
    CV1 = 0
    CV2 = 0
    CV3 = 0
    Gate = 1
    
CV = CV()


def led(n):
    n.on()
    time.sleep(60/tempo.valeur)
    n.off()


def led_note():
    octave = str(l_step[step.n][0])
    pitch = note[l_step[step.n][1]-1]
    return "Note : " + pitch + octave


def augmenter_step():
    step.n += 1
    step.n = step.n%MAX_STEP
    print("Step : " + str(step.n))


def diminuer_step():
    if step.n == MIN_STEP: # step.pitch
        step.n = MAX_STEP
    else:
        step.n -= 1
    print("Step : " + str(step.n))


def augmenter_pitch():
    if l_step[step.n][1] == MAX_PITCH:
        l_step[step.n][0] += 1
        l_step[step.n][0] = l_step[step.n][0]%(MAX_OCTAVE + 1)
        l_step[step.n][1] += 1
    l_step[step.n][1] += 1
    l_step[step.n][1] = l_step[step.n][1]%(MAX_PITCH + 1)
    print(led_note())
    dac1.setVoltage(0,int(4096*(((l_step[step.n][0]*12)+l_step[step.n][1])/60)))


def diminuer_pitch():
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


def augmenter_octave():
    l_step[step.n][0] += 1
    l_step[step.n][0] = l_step[step.n][0]%(MAX_OCTAVE + 1)
    #print(led_note())


def diminuer_octave():
    if l_step[step.n][0] == MIN_OCTAVE:
        l_step[step.n][0] = MAX_OCTAVE
    else:
        l_step[step.n][0] -= 1
    #print(led_note())


def augmenter_tempo():
    if tempo.valeur < MAX_TEMPO:
        tempo.valeur += 1
    print("Tempo:",tempo.valeur)


def diminuer_tempo():
    if tempo.valeur > MIN_TEMPO:
        tempo.valeur -= 1
    print("Tempo",tempo.valeur)


def augmenter_CV1():
    CV.CV1 += 1
    CV.CV1 = CV.CV1%MAX_CV
    dac1.setVoltage(1, int(float(4096)*CV.CV1/24))
    print("CV1:",CV.CV1)


def augmenter_CV2():
    CV.CV2 += 1
    CV.CV2 = CV.CV2%MAX_CV
    dac2.setVoltage(0, int(float(4096)*CV.CV2/24))
    print("CV2:",CV.CV2)


def augmenter_CV3():
    CV.CV3 += 1
    CV.CV3 = CV.CV3%MAX_CV
    dac2.setVoltage(1, int(float(4096)*CV.CV3/24))
    print("CV3:",CV.CV3)


def diminuer_CV1():
    if CV.CV1 == 0:
        CV.CV1 = 24
    else:
        CV.CV1 -= 1
    dac1.setVoltage(1, int(float(4096)*CV.CV1/24))
    print("CV1:",CV.CV1)


def diminuer_CV2():
    if CV.CV2 == 0:
        CV.CV2 = 24
    else:
        CV.CV2 -= 1
    dac2.setVoltage(0, int(float(4096)*CV.CV2/24))
    print("CV2:",CV.CV2)


def diminuer_CV3():
    if CV.CV3 == 0:
        CV.CV3 = 24
    else:
        CV.CV3 -= 1
    dac2.setVoltage(1, int(float(4096)*CV.CV3/24))
    print("CV3:",CV.CV3)


def augmenter_Gate():
    if CV.Gate >= 0.95:
        CV.Gate = 0
    else:
        CV.Gate += 0.1
    #dac3.setVoltage(1, int(4096*CV.Gate))
    print("Gate:",round(CV.Gate,1))
    

def diminuer_Gate():
    if CV.Gate <= 0.05:
        CV.Gate = 1
    else:
        CV.Gate -= 0.1
    #dac3.setVoltage(1, int(4096*CV.Gate))
    print("Gate:",round(CV.Gate,1))

'''
def on():
    p = 'on'
    while p == 'on':
        for i in range(8):
            dac3.setVoltage(1, 12*l_step[i][0] + l_step[i][1]) 
            # led(l_led[i])
            time.sleep(60/tempo.valeur)
        if not button1.is_pressed:
            p = 'off'
    #if keyboard interrupt:
        #(led off)
        #break
'''
# C0 - (B#4) - C5

#button1.when_pressed = on
#button2.when_pressed = augmenter_octave
#button3.when_pressed = diminuer_octave


rotor1.when_rotated_clockwise = augmenter_pitch
rotor1.when_rotated_counter_clockwise = diminuer_pitch
rotor2.when_rotated_clockwise = augmenter_CV1
rotor2.when_rotated_counter_clockwise = diminuer_CV1
rotor3.when_rotated_clockwise = augmenter_Gate
rotor3.when_rotated_counter_clockwise = diminuer_Gate
rotor4.when_rotated_clockwise = augmenter_CV2
rotor4.when_rotated_counter_clockwise = diminuer_CV2
rotor5.when_rotated_clockwise = augmenter_CV3
rotor5.when_rotated_counter_clockwise = diminuer_CV3
rotor6.when_rotated_clockwise = augmenter_tempo
rotor6.when_rotated_counter_clockwise = diminuer_tempo


pause()