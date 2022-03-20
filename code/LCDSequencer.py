# activate I2C
# install smbus

from RPLCD.i2c import CharLCD

class LCDSequencer: # must initiate in main file: lcd = LCDSequencer()
    """
        * LCD Class
    """
    #dans l'init: lcd = lcd = CharLCD(i2c_expander='PCF8574', address=0x26, cols=16, rows=2, auto_linebreaks=True, backlight_enabled=True)

    def __init__(self):
        ''' #! remove
        self.testvar = 0
        
        self.pitch = pitch    # besoin ?
        self.tempo = tempo    # besoin ?
        self.octave = octave  # besoin ?
        self.step = step      # besoin ?
        self.cv = cv  # besoin ?
        '''
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x26, cols=16, rows=2, auto_linebreaks=True, backlight_enabled=False)  # initiate the LCD from the RPLCD.i2c library with these parameters
        self.fullClearLCD() # Clears the LCD
        self.lcd.backlight_enabled = True # Turns the backlight ON # ?

    def displayTempo(self, tempo):
        
        self.clearRightLCD()
        '''We should calculate the space left in the line and reposition the cursor like 16-length("Tempo:")
        or (PREFERRED) add white spaces before the string and put cursor pos at something like 8 because it will clear any text left on the screen if the previous one was longer'''
        stringTempo = str(tempo)+"BPM"
        cursorPosTempo = 16 - len(stringTempo) # because the LCD is 16 character long
        
        self.lcd.cursor_pos = (0, 10)
        self.lcd.write_string("Tempo:")

        self.lcd.cursor_pos = (1, cursorPosTempo)
        self.lcd.write_string(stringTempo)

        print("Tempo:",stringTempo)

    def displayNote(self, pitch, octave):
        
        self.clearBottomLeftLCD()

        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(str(pitch) + str(octave))

    def displayStep(self, step, pitch, octave):
        
        self.clearTopLeftLCD()

        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Step " + str(step))

        self.displayNote(pitch, octave)

    def displayCV(self, cvNumber, cvValue):
        
        self.clearRightLCD()
        stringCV = str(int(cvValue)) #? +"%" ?
        cursorPosCV = 16 - len(stringCV)

        self.lcd.cursor_pos = (0, 10) #! need to check
        self.lcd.write_string("CV #"+str(cvNumber)+":")  # ! need to check

        self.lcd.cursor_pos = (1, cursorPosCV)  # ! need to check
        self.lcd.write_string(stringCV)  # ! need to check

        print("CV",cvNumber, "value:",stringCV)

    def displayGate(self, gate):

        self.clearRightLCD()

        stringGate = str(int(gate*100))+"%" #? int()
        cursorPosGate = 16 - len(stringGate)

        self.lcd.cursor_pos = (0, 11) #! need to check
        self.lcd.write_string("Gate:") #! need to check

        self.lcd.cursor_pos = (1, cursorPosGate) #! need to check
        self.lcd.write_string(stringGate)  # ! need to check
        
        print("Gate:",stringGate)
        
    def test(self):
        print("test lcd")# + str(self.testvar))
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("TEST")

    def fullClearLCD(self):
        self.lcd.clear()
        print("full clear lcd")

    def clearRightLCD(self): # clears the LCD from the 8th column (the right side of the screen)
        #for i in range(2):
        #    self.lcd.cursor_pos = (i,8)
        #    self.lcd.write_string(" "*8)
        self.lcd.cursor_pos = (0, 8)
        self.lcd.write_string("        ")
        self.lcd.cursor_pos = (1, 8)
        self.lcd.write_string("        ")
        print("right lcd cleared")

    def clearTopLeftLCD(self):
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("        ")
        print("top left lcd cleared")

    def clearBottomLeftLCD(self):
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("        ")
        print("bottom left lcd cleared")

    def toggleBacklight(self, boolean):
        self.lcd.backlight_enabled = boolean
        print("LCD Backlight:",str(boolean))

    def splashScreen(self):
        print("splash screen LCD")
        #self.lcd.fullClearLCD()
        
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("SEQUOTRON...")
        
        self.lcd.cursor_pos = (1, 4)
        self.lcd.write_string("...SEQUOTRON")
        
        print("  ###  SEQUOTRON  ###  ")


