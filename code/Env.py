
# * Global variables:

# Saved sequence file path
SAVE_FILE = "/path/to/saved-sequence-file.txt"

# Simulated DAC
SIMULATED_DAC = False

# Simulated LCD
SIMULATED_LCD = False

# PITCH
MAX_PITCH = 12 # should adapt the code to make it 11
MIN_PITCH = 1 # should adapt the code to make it 0

# OCTAVE
MAX_OCTAVE = 2  # 4 when 5V, here only 2 because only 3.3V
MIN_OCTAVE = 0

NB_OCTAVES = MAX_OCTAVE+1

NB_NOTES = MAX_PITCH*(MAX_OCTAVE+1)

# STEP
NB_STEPS = 8 # could be increased ?
#MAX_STEP = 7
MAX_STEP = NB_STEPS-1
MIN_STEP = 0

# DAC
PITCH_CHANNEL = 0 #dac 1
GATE_CHANNEL = 0 #dac 2
CV1_CHANNEL = 1 #dac 2
CV2_CHANNEL = 0 #dac 3
CV3_CHANNEL = 1 #dac 3

NB_BITS_DAC = 12

#MAX_DAC = (2^12) -1
MAX_DAC = 4095 # 12bit
# 3.3V -> 4095
# 3V -> 3723

# CV
MAX_CV = 25
MIN_CV = 0

# TEMPO (BPM)
MAX_TEMPO = 359
MIN_TEMPO = 20

# LED_QUANTITY
LED_QUANTITY = 8

# STARTUP SEQUENCE
# ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
STARTUP_SEQUENCE = [[2,0],[2,0],[1,10],[1,10],[1,9],[1,9],[1,7],[1,7],[1,5],[1,5],[1,3],[1,3],[1,2],[1,2],[1,0],[1,0]]
# C2 C2 A#1 A#1 A1 A1 G1 G1 F1 F1 D#1 D#1 D1 D1 C1 C1
