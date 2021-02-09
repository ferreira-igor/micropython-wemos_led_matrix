
# Project: Wemos LED Matrix
# Author: Igor Ferreira
# Description: An implementation of the framebuf library to use with the Wemos' Matrix LED Shield.
# Shield page: https://www.wemos.cc/en/latest/d1_mini_shield/matrix_led.html
# Arduino library: https://github.com/wemos/WEMOS_Matrix_LED_Shield_Arduino_Library
# Source: https://github.com/h1pn0z/micropython-wifi_manager/


from machine import Pin
from framebuf import FrameBuffer, MONO_HLSB


class Matrix(FrameBuffer):
    
    ON = 1
    OFF = 0

    def __init__(self, dataPin, clockPin):
        
        self.dataPin = Pin(dataPin, Pin.OUT)
        self.clockPin = Pin(clockPin, Pin.OUT)
        
        self.framebuffer = bytearray(8)
        super().__init__(self.framebuffer, 8, 8, MONO_HLSB)
        
        self.intensity = 7
        
        self.dataPin.on()
        self.clockPin.on()

    def setIntensity(self, intensity):
        if intensity > 7:
            self.intensity = 7
            print("Invalid brightness value! Using most approximate value.")
        elif intensity < 0:
            self.intensity = 0
            print("Invalid brightness value! Using most approximate value.")
        else:
            self.intensity = intensity

    def send(self, data, bits):
        for pixel in range(0, bits):
            self.clockPin.off()
            if data >> pixel & 1:
                self.dataPin.on()
            else:
                self.dataPin.off()
            self.clockPin.on()

    def sendCommand(self, cmd):
        self.dataPin.off()
        self.send(cmd, 8)
        self.dataPin.on()

    def sendData(self):
        self.sendCommand(0x44)
        self.dataPin.off()
        self.send(0xC0, 8)
        for data in self.framebuffer:
            self.send(data, 8)
        self.dataPin.on()

    def display(self):
        self.sendData()
        self.dataPin.off()
        self.clockPin.off()
        self.clockPin.on()
        self.dataPin.on()
        self.sendCommand(0x88|self.intensity)
