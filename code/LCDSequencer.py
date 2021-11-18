# activer I2C
# installer smbus
#peut etre besoin de pigpio (en plus de gpiozero)
# et

# CODE PLUS BAS

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


class LCDSequencer: # must initiate in main file: lcd = LCDSequencer()
    """
        LCD Class
    """
    def __init__(self, tempo):
        self.testvar = 0
        self.tempo = tempo # besoin ?

    def displayTempo(self, tempo):
        self.justify('right')
        self.write(0, "Tempo:\n" + tempo.toString() +"BPM")
        #self.write(0, "Tempo: \n$tempoBPM")

    def displayNote(self, pitch, octave):
        self.justify('left')
        self.write(1, pitch.toString() + octave.toString())

    def displayStep(self, step):
        self.justify('left')
        self.write(0, "Step " + step.toString())
        #self.write("Step $step")
        
        self.displayNote(step.pitch, step.octave)

    def displayOutput(self, output):
        self.justify('right')
        self.write(0, "Output" + output.toString() + ":\n" + output.value.toString())
        
    def test(self):
        print("test")
