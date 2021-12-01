class Step:

    def __init__(self, nbstep, pitch=3, octave=3):

        self.nbstep = nbstep
        self.pitch = pitch
        ''' 1:C(do)  2:C#(do#)  3:D(re)  4:D#(re#)  5:E(mi)  6:F(fa)  7:F#(fa#)  8:G(sol)  9:G#(sol#)  10:A(la)  11:A#(la#)  12:B(si) '''
        ''' formule note -> freq : f = 2^(n/12) * 440 Hz  où n est le nombre de demi-note par rapport à A4 (positif si plus haut et négatif si plus bas)
            utiliser le mapping MIDI ? : https://en.wikipedia.org/wiki/Musical_note#:~:text=For%20use%20with%20the%20MIDI%20(Musical%20Instrument%20Digital%20Interface)%20standard%2C%20a%20frequency%20mapping%20is%20defined%20by%3A
        '''
        self.octave = octave
        

    