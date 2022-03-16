# Saves a sequence or loads a saved one

# ! STILL TODO - TO BE INTEGRATED !
#TODO

def read_sequences(file):
    p = []
    with open(file, encoding='utf-8') as f:
        for i in f:
            a = i.split()
            p.append(a)
    return p

def write_sequences(l, file):
    with open(file, 'w', encoding='utf-8') as f:
        for i in range(len(l)):
            f.write(l[i][0] + ' ' + l[i][1] + '\n')
    
