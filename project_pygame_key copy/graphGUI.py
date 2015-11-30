
#Import pygame modules and Buttons.py(it must be in same dir)
import pygame.font, pygame.event, pygame.draw, string, Buttons
from pygame.locals import *
import pyaudio,sys
import wave
import struct
import math
import numpy as np
import pygame
import random
import time
import multiprocessing
import scipy.signal as signal
import myfunctions
import sound

#Initialize pygame
pygame.init()

class Button_Example:
    def __init__(self,Type):
        self.main_func(Type)
    
    #Create a display
    def display(self):
        self.screen = pygame.display.set_mode((650,370),0,32)
        pygame.display.set_caption("Buttons.py - example")

    #Update the display and show the button
    def update_display(self):
        self.screen.fill((30,144,255))
        length = 80
        height = 80
        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.Button1.create_button(self.screen, (107,142,35), 20,  135, length,    height,    0,        "Example1", (255,255,255))
        self.Button2.create_button(self.screen, (107,142,35), 120, 135, length,    height,    0,        "Example2", (255,255,255))
        self.Button3.create_button(self.screen, (107,142,35), 220, 135, length,    height,    0,        "Example3", (255,255,255))
        self.Button4.create_button(self.screen, (107,142,35), 320, 135, length,    height,    0,        "Example4", (255,255,255))
        self.Button5.create_button(self.screen, (107,142,35), 420, 135, length,    height,    0,        "Example5", (255,255,255))
        pygame.display.flip()

    def display_box(self,screen, message):
        fontobject=pygame.font.SysFont('Arial', 50)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (107, 142, 35)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        pygame.display.flip()
        time.sleep(3)


    #Run the loop
    def main_func(self,Type):
        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        self.Button3 = Buttons.Button()
        self.Button4 = Buttons.Button()
        self.Button5 = Buttons.Button()

        wavfile = 'leanon.wav'
        wf = wave.open( wavfile, 'rb')
        print Type
        # Read wave file properties
        CHANNELS = wf.getnchannels()        # Number of channels
        RATE = wf.getframerate()            # Sampling rate (frames/second)
        LEN  = wf.getnframes()              # Signal length
        WIDTH = wf.getsampwidth()           # Number of bytes per sample
        BLOCK = 2048
        OUT = WIDTH * BLOCK
        kr = 0 #vibrato's read index
        print('The file has %d channel(s).'         % CHANNELS)
        print('The file has %d frames/second.'      % RATE)
        print('The file has %d frames.'             % LEN)
        print('The file has %d bytes per sample.'   % WIDTH)

        p = pyaudio.PyAudio()
        stream = p.open(format      = pyaudio.paInt16,
                        channels    = 2,
                        rate        = RATE,
                        input       = False,
                        output      = True )

        print Type
        self.display()
        while True:
            
            # send to sound.py, process the sound
            
            input_string = wf.readframes(BLOCK)
            input_tuple = struct.unpack('h'*OUT, input_string)
            # call sound function to process effect
            output_string =  sound.main(input_tuple, RATE, Type, OUT)
            stream.write(output_string)

            # update with display
            self.update_display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    window_size = (650,370)
                    surf = pygame.display.set_mode(window_size)
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!1"    
                        self.display_box(surf, "Example 1")
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!2"
                        self.display_box(surf, "Example 2")
                    elif self.Button3.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!3"
                        self.display_box(surf, "Example 3")
                    elif self.Button4.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!4"
                        self.display_box(surf, "Example 4")
                    elif self.Button5.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!5"
                        self.display_box(surf, "Example 5")
        stream.stop_stream()
        stream.close()
        p.terminate()

    print 'done'
                    

if __name__ == '__main__':
    Type = 'n'
    obj = Button_Example(Type)
