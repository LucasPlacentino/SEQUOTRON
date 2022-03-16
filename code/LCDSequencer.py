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

        self.lcd.cursor_pos = (0, 9) #! need to check
        self.lcd.write_string("..CV#"+str(cvNumber)+":")  # ! need to check

        self.lcd.cursor_pos = (1, cursorPosCV-4)  # ! need to check
        self.lcd.write_string("...."+stringCV)  # ! need to check

    def displayGate(self, gate):

        self.clearRightLCD()

        stringGate = str(int(gate*100))+"%" #? int()
        cursorPosGate = 16 - len(stringGate)

        self.lcd.cursor_pos = (0, 11) #! need to check
        self.lcd.write_string("Gate:") #! need to check

        self.lcd.cursor_pos = (1, cursorPosGate) #! need to check
        self.lcd.write_string(stringGate)  # ! need to check
        
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





#! below were just different libraries tests
"""
#pip install rpi-lcd
from rpi_lcd import LCD
from time import sleep

lcd = LCD()

lcd.text('Hello', 1)
lcd.text('World!', 1, 'right')
lcd.text('Raspberry Pi', 2, 'center')

sleep(5)
lcd.clear()
"""


"""pour justifier du texte à droite (voir librairies utlisée)
autoScroll(True)
rtl(True)
rightToLeft(True)
ou des commandes du genre
"""

""" RPLCD voir (dans lcd.py):
def _set_text_align_mode(self, value):
        if value == 'left':
            self._text_align_mode = c.Alignment.left
        elif value == 'right':
            self._text_align_mode = c.Alignment.right
        else:
            raise ValueError('Text align mode must be either `left` or `right`')
        self.command(c.LCD_ENTRYMODESET | self._text_align_mode | self._display_shift_mode)
        c.usleep(50)

    text_align_mode = property(_get_text_align_mode, _set_text_align_mode,
            doc='The text alignment (``left`` or ``right``).')
"""

""" on dirait que ceci est exactement ce qu'il faut
https://github.com/Depau/python-liquidcrystal
"""

""" test https://learn.adafruit.com/i2c-spi-lcd-backpack/python-circuitpython
import time
import board
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialise the lcd class
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Turn backlight on
lcd.backlight = True
# Print two line message right to left
lcd.text_direction = lcd.RIGHT_TO_LEFT
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
# Return text direction to left to right
lcd.text_direction = lcd.LEFT_TO_RIGHT
"""

""" test https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()

padding = " " * 16
my_long_string = "This is a string that needs to scroll"
padded_string = my_long_string + padding

for i in range (0, len(my_long_string)):
 lcd_text = padded_string[((len(my_long_string)-1)-i):-i]
 mylcd.lcd_display_string(lcd_text,1)
 sleep(0.4)
 mylcd.lcd_display_string(padding[(15+i):i], 1)
"""
