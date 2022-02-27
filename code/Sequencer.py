from DACSequencer import DACSequencer
import gpiozero
# import time
from LCDSequencer import LCDSequencer
# import spidev
# from signal import pause
# from MCP4922 import MCP4922
from RotaryEncoder import RotaryEncoder
from CV import CV


MAX_STEP = 7
MIN_STEP = 0
MAX_TEMPO = 359
MIN_TEMPO = 2
MAX_OCTAVE = 2 # 4 when 5V, here only 2 because only 3.3V
MIN_OCTAVE = 0
MAX_PITCH = 12
MIN_PITCH = 1
MAX_CV = 25
LCD = LCDSequencer() # ? or in SequencerMain
MAX_DAC = 4095
LED_QUANTITY = 8
class Sequencer:

    '''
    MAX_STEP = 7
    MIN_STEP = 0
    MAX_TEMPO = 359
    MIN_TEMPO = 2
    MAX_OCTAVE = 2 # 4 when 5V, here only 2 because only 3.3V
    MIN_OCTAVE = 0
    MAX_PITCH = 12
    MIN_PITCH = 1
    MAX_CV = 25
    LCD = LCDSequencer() #? or in SequencerMain
    '''

    def __init__(self):

        #? self.lcd = LCDSequencer()

        self.button1 = gpiozero.Button(5) # physical pin 29
        self.button2 = gpiozero.Button(6) # physical pin 31
        self.button3 = gpiozero.Button(12) # physical pin 32
        #TODO add more buttons 

        self.rotorTempo = RotaryEncoder(17, 27, "tempo") # physical pin 11 and 13
        self.rotorGate = RotaryEncoder(4, 14, "gate/env") # physical pin 7 and 8
        self.rotorCV1 = RotaryEncoder(15, 18, "cv", 1) # physical pin 10 and 12
        self.rotorCV2 = RotaryEncoder(22, 23, "cv", 2) # physcial pin 15 and 16
        self.rotorCV3 = RotaryEncoder(24, 25, "cv", 3) # physical pin 18 and 22
        #? self.rotorStep = RotaryEncoder(,,"step",) #

        self.dac1 = DACSequencer(0, 0, 5) # could be a MCP4921, physical pin 29
        self.dac2 = DACSequencer(0, 0, 7) # physical pin 26
        self.dac3 = DACSequencer(0, 0, 8) # physical pin 24

        self.cv1 = CV(1, self.dac2, 1)
        self.cv2 = CV(2, self.dac3, 0)
        self.cv3 = CV(3, self.dac3, 1)

        #TODO add switches
        #* OR use a simple Button(pin) and use button.is_pressed (True if HIGH)
        self.switchClock = gpiozero.InputDevice(19) # set pin for the switch1 HIGH
        self.switchPause = gpiozero.InputDevice(20) # set pin for the switch2 HIGH
        #* then use switchExample.is_active (True if HIGH or False if LOW)

        #TODO add input jacks 
            #! convert them to 3.3v







''' #* BELOW IS THE CODE ON THE RPI AT THE END OF Q1 (SequencerSurRPI.py)

button1 = Button(5) #29
button2 = Button(6) #31
button3 = Button(12) #32

rotor1 = RotaryEncoder(17, 27) # 11 et 13 (tempo)
rotor2 = RotaryEncoder(4, 14) # 7 et 8 (gate)
rotor3 = RotaryEncoder(15, 18) # 10 et 12 (CV1)
rotor4 = RotaryEncoder(22, 23) # 15 et 16 (CV2)
rotor5 = RotaryEncoder(24, 25) # 18 et 22 (CV3)

"""
led1 = LED(27) #13
led2 = LED(23) #15
led3 = LED(22) #16

l_led = [led1,led2,led3]
"""

dac1 = MCP4922(0, 0, 5) #29 (4921 mais ça peut aussi fonctionner en 4922)
dac2 = MCP4922(0, 0, 7) #26
dac3 = MCP4922(0, 0, 8) #24


note = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
l_step = []
for i in range(8): #création de la liste des notes
    l_step.append([0, 1]) #cette liste représente l'octave et la note


MAX_STEP = 7
MIN_STEP = 0
MAX_TEMPO = 359
MIN_TEMPO = 2
MAX_OCTAVE = 4
MIN_OCTAVE = 0
MAX_PITCH = 12
MIN_PITCH = 1


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
        l_step[step.n][0] = l_step[step.n][0]%MAX_OCTAVE
    l_step[step.n][1] += 1
    l_step[step.n][1] = l_step[step.n][1]%MAX_PITCH
    print(led_note())


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


def augmenter_octave():
    l_step[step.n][0] += 1
    l_step[step.n][0] = l_step[step.n][0]%MAX_OCTAVE
    print(led_note())


def diminuer_octave():
    if l_step[step.n][0] == MIN_OCTAVE:
        l_step[step.n][0] = MAX_OCTAVE
    else:
        l_step[step.n][0] -= 1
    print(led_note())


def augmenter_tempo():
    if tempo.valeur < MAX_TEMPO:
        tempo.valeur += 1
    print(tempo.valeur)


def diminuer_tempo():
    if tempo.valeur > MIN_TEMPO:
        tempo.valeur -= 1
    print(tempo.valeur)


def augmenter_CV1():
    CV.CV1 += 1
    CV.CV1 = CV.CV1%24
    dac1.setVoltage(0, 4096*CV.CV1/24)


def augmenter_CV2():
    CV.CV2 += 1
    CV.CV2 = CV.CV2%24
    dac2.setVoltage(1, 4096*CV.CV2/24)


def augmenter_CV3():
    CV.CV3 += 1
    CV.CV3 = CV.CV3%24
    dac3.setVoltage(n, 4096*CV.CV3/24)


def diminuer_CV1():
    if CV.CV1 == 0:
        CV.CV1 = 24
    else:
        CV.CV1 -= 1
    dac1.setVoltage(0, 4096*CV.CV1/24)


def diminuer_CV2():
    if CV.CV2 == 0:
        CV.CV2 = 24
    else:
        CV.CV2 -= 1
    dac1.setVoltage(1, 4096*CV.CV2/24)


def diminuer_CV3():
    if CV.CV3 == 0:
        CV.CV3 = 24
    else:
        CV.CV3 -= 1
    dac2.setVoltage(0, 4096*CV.CV3/24)


def augmenter_Gate():
    if CV.Gate == 1:
        CV.Gate = 0
    else:
        CV.Gate += 0.1
    dac3.setVoltage(1, 4096*Gate)
    

def diminuer_Gate():
    if CV.Gate == 0:
        CV.Gate = 1
    else:
        CV.Gate -= 0.05
    dac3.setVoltage(1, 4096*Gate)


def on():
    p = 'on'
    while p == 'on':
        for i in range(8):
            dac3.setVoltage(1, 12*l_step[i][0] + l_step[i][1])
            #led(l_led[i])
            time.sleep(60/tempo.valeur)
        if not button1.is_pressed:
            p = 'off'
    #if keyboard interrupt:
        #(led off)
        #break

# C0 - (B#4) - C5

button1.when_pressed = on
button2.when_pressed = augmenter_pitch
button3.when_pressed = diminuer_pitch

rotor1.when_rotated_clockwise = augmenter_tempo
rotor1.when_rotated_counter_clockwise = diminuer_tempo
rotor2.when_rotated_clockwise = augmenter_Gate
rotor2.when_rotated_counter_clockwise = diminuer_Gate
rotor3.when_rotated_clockwise = augmenter_CV1
rotor3.when_rotated_counter_clockwise = diminuer_CV1
rotor4.when_rotated_clockwise = augmenter_CV2
rotor4.when_rotated_counter_clockwise = diminuer_CV2
rotor5.when_rotated_clockwise = augmenter_CV3
rotor5.when_rotated_counter_clockwise = diminuer_CV3


pause()

'''
