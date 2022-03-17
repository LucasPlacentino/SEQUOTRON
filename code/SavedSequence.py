# Saves a sequence or loads a saved one

# ! STILL TODO - TO BE INTEGRATED !
#TODO

from Env import SAVE_FILE

def read_sequences(SAVE_FILE):
    p = []
    with open(SAVE_FILE, encoding='utf-8') as f:
        for i in f:
            a = i.split()
            p.append(a)
    return p

def write_sequences(listStep, SAVE_FILE):
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        for i in range(len(listStep)):
            f.write(listStep[i][0] + ' ' + listStep[i][1] + '\n')
    
