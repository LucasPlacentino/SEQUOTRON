#!/usr/bin/python

"""
Python Library for MCP4922 DAC using Raspberry Pi 3 Model B+
2 Channels, 12 Bit
Currently only supports Hardware SPI
Requires: RPi.GPIO & spidev libraries

Wiring:

MCP4922    =======>   Raspberry Pi

CS         ------->   GPIO08 Physical Pin 24 (SPI0 CE0) => Can be changed
SDI        ------->   GPIO10 Physical Pin 19 (SPI0 MOSI) => cannot be changed in hardware SPI MODE
SCK        ------->   GPIO11 Physical Pin 23 (SPI0 SCLK) => cannot be changed in hardware SPI MODE

MIT License

Copyright (c) 2017 mrwunderbar666

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import RPi.GPIO as GPIO
import spidev


class MCP4922(object):
    """ Class for the Microchip MCP4922 digital to analog converter
    """
    spi = spidev.SpiDev()

    def __init__(self,
                 spibus=None,
                 spidevice=None,
                 cs=None
                 ):
        """ Initialize MCP4922 device with hardware SPI
            Chipselect default value is BCM Pin 8 (Physical Pin: 24)
            Select the bus and device number. Default values are:
            Bus = 0 ; Device = 1
            If you're not sure, just leave it default
        """
        mode = GPIO.getmode()
        if mode == GPIO.BOARD:
            default_cs = 24
        elif mode == GPIO.BCM:
            default_cs = 8
        else:
            raise ValueError(
                "You haven't selected a GPIO Mode? Use: e.g. GPIO.setmode(GPIO.BCM)")

        if cs is None:
            self.cs = default_cs
        else:
            self.cs = cs

        if spibus is None:
            self.spibus = 0
        else:
            self.spibus = spibus

        if spidevice is None:
            self.spidevice = 1
        else:
            self.spidevice = spidevice

        GPIO.setup(self.cs, GPIO.OUT)
        GPIO.output(self.cs, 1)

        #? self.spi.max_speed_hz = 1953000 #! ?

        #* As soon as MCP4922 object is created spidev bus and device are opened
        #* otherwise causes memory leak and creates Errno 24
        self.spi.open(self.spibus, self.spidevice) # ! comment ?

    def setVoltage(self, channel, value):
        """
        Regular setVoltage Function
        Select your channel 0 or 1
        Select Voltage value 0 to 4095
        """
        if channel == 0:
            output = 0x3000
        elif channel == 1:
            output = 0xb000
        else:
            raise ValueError(
                'MCP4922 Says: Wrong Channel Selected! Chose either 0 or 1!')
        if value > 4095:
            value = 4095
        if value < 0:
            value = 0
        #self.spi.open(self.spibus, self.spidevice) # ! uncomment ?
        output |= value
        #* print("hex output :",output)
        buf0 = (output >> 8) & 0xff
        #* print("buf0 :", buf0)
        buf1 = output & 0xff
        #* print("buf1 :", buf1)
        GPIO.output(self.cs, 0)
        #* print("cs 0")
        self.spi.writebytes([buf0, buf1])
        #* print("writebytes :", [buf0, buf1])
        GPIO.output(self.cs, 1)
        #* print("cs 1")
        #self.spi.close() # ! uncomment ? # ! modified, author forgot the parentheses ()
        return

    def setVoltage_gain(self, channel, value):
        """
        The MCP4922 has the ability to output the double of the reference Voltage
        Reference Voltage is measured by the MCP4922 at pin 13 (VrefA) for Channel A and pin 11 (VrefB) for Channel B
        Note that the output voltage cannot exceed the supply voltage from pin 1 (VDD)
        """
        if channel == 0:
            output = 0x1000
        elif channel == 1:
            output = 0x9000
        else:
            raise ValueError(
                'MCP4922 Says: Wrong Channel Selected! Chose either 0 or 1!')
        if value > 4095:
            value = 4095
        if value < 0:
            value = 0
        #self.spi.open(self.spibus, self.spidevice) # ! uncomment ?
        output |= value
        buf0 = (output >> 8) & 0xff
        buf1 = output & 0xff
        GPIO.output(self.cs, 0)
        self.spi.writebytes([buf0, buf1])
        GPIO.output(self.cs, 1)
        #self.spi.close() # ! uncomment ? # ! modified, author forgot the parentheses ()
        return

    def setVoltage_buffered(self, channel, value):
        """
        Using the buffer feature of the MCP4922,
        refer to the datasheet for details
        """
        if channel == 0:
            output = 0x7000
        elif channel == 1:
            output = 0xF000
        else:
            raise ValueError(
                'MCP4922 Says: Wrong Channel Selected! Chose either 0 or 1!')
        if value > 4095:
            value = 4095
        if value < 0:
            value = 0
        #self.spi.open(self.spibus, self.spidevice) # ! uncomment ?
        output |= value
        buf0 = (output >> 8) & 0xff
        buf1 = output & 0xff
        GPIO.output(self.cs, 0)
        self.spi.writebytes([buf0, buf1])
        GPIO.output(self.cs, 1)
        #self.spi.close() # ! uncomment ? # ! modified, author forgot the parentheses ()
        return

    def shutdown(self, channel):
        """
        Completely shutdown selected channel for power saving
        Sets the output of selected channel to 0 and 500K Ohms.
        Read Datasheet (SHDN) for details
        """
        if channel == 0:
            output = 0x2000
        elif channel == 1:
            output = 0xA000
        else:
            raise ValueError(
                'MCP4922 Says: Wrong Channel Selected! Chose either 0 or 1!')
        #self.spi.open(self.spibus, self.spidevice) # ! uncomment ?
        buf0 = (output >> 8) & 0xff
        buf1 = output & 0xff
        GPIO.output(self.cs, 0)
        self.spi.writebytes([buf0, buf1])
        GPIO.output(self.cs, 1)
        #self.spi.close() # ! uncomment ? # ! modified, author forgot the parentheses ()
        return

    def close(self):
        """
        Closes the device
        """
        self.spi.close() # ! modified, author forgot the parentheses ()
        return

    def open(self):
        """
        Manually Open the device
        """
        self.spi.open(self.spibus, self.spidevice)
        return
