
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
        self.screen = pygame.display.set_mode((640,580),0,32)
        pygame.display.set_caption("Buttons.py - example")

    #Update the display and show the button
    def update_display(self,score):
        self.screen.fill((255,255,255))
        length = 80
        height = 80
        YELLOW = (255,255,0)
        RED = (255,0,0)
        GREEN = (0,255,40)
        FONT1 = pygame.font.SysFont('Ariel',114)
        FONT2 = pygame.font.SysFont('Cochin',21)
        SURFACEFONT = FONT1.render("%d" % score,True,(20,20,100)) #True is for anti-aliasing, looks better when true 
        Title = FONT2.render("GUESSING GAME : \n THE TRULY PROFESSIONAL DJ",True,(100,10,10))
        SURFACER=SURFACEFONT.get_rect() #meaning SURFACER will gain rectangular values
        SURFACER.center=(300,300)
        self.screen.blit(SURFACEFONT,(275,290)) # score position
        self.screen.blit(Title,(50,50)) 
        #Param(self.screen, (107,142,35), 220, 135, length,    height,    0,        "BandStop", (255,255,255))
        self.Button1.create_button(self.screen, (110,110,200), 120, 235, length,    height,    0,        "Normal", (0,0,0)) #normal
        self.Button2.create_button(self.screen, (107,202,100), 220, 135, length,    height,    0,        "LowPass", (0,0,0)) #l
        self.Button3.create_button(self.screen, (200,190,135), 320, 135, length,    height,    0,        "BandStop", (0,0,0)) #b
        self.Button4.create_button(self.screen, (200,142,35), 420, 235, length,    height,    0,        "HighPass", (0,0,0)) #h
        self.Button5.create_button(self.screen, (235,100,105), 420, 335, length,    height,    0,        "Vibrato", (0,0,0)) #v

        pygame.display.flip()

    def update_display_first(self):
        self.screen.fill((255,255,255))
        length = 80
        height = 80
        YELLOW = (255,255,0)
        RED = (255,0,0)
        GREEN = (0,255,40)
        FONT1 = pygame.font.SysFont('Ariel',114)
        FONT2 = pygame.font.SysFont('Cochin',21)
        SURFACEFONT = FONT1.render("Hiii",True,(20,20,100)) #True is for anti-aliasing, looks better when true 
        Title = FONT2.render("GUESSING GAME : \n THE TRULY PROFESSIONAL DJ",True,(100,10,10))
        SURFACER=SURFACEFONT.get_rect() #meaning SURFACER will gain rectangular values
        SURFACER.center=(300,300)
        self.screen.blit(SURFACEFONT,(275,290)) # score position
        self.screen.blit(Title,(50,50)) 
        #Param(self.screen, (107,142,35), 220, 135, length,    height,    0,        "BandStop", (255,255,255))
        self.Button1.create_button(self.screen, (110,110,200), 120, 235, length,    height,    0,        "lean-on", (0,0,0)) #normal
        self.Button2.create_button(self.screen, (107,202,100), 220, 135, length,    height,    0,        "shakeitoff", (0,0,0)) #l
        

        pygame.display.flip()



    def display_box(self,screen, message, message2): # youo're right message box
        self.screen.fill((255,255,255))
        fontobject=pygame.font.SysFont('Cochin', 90)                                #Bingo font
        fontobject2=pygame.font.SysFont('Cochin', 40)                              
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (100, 20, 20)),              #Bingo color
                ((screen.get_width() / 2) - 170, (screen.get_height() / 2) - 130))   #position
            screen.blit(fontobject2.render(message2, 1, (0, 0, 35)),              #your score color
                ((screen.get_width() / 2) - 140, (screen.get_height() / 2) - 10))   #position

        pygame.display.flip()
        time.sleep(1)


    #Run the loop
    def main_func(self,Type):
        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        self.Button3 = Buttons.Button()
        self.Button4 = Buttons.Button()
        self.Button5 = Buttons.Button()
        self.display()

        # get the info of song_name
        firstop = False
        while firstop == False:
            self.update_display_first()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        print "song choosed"
                        firstop = True
                        wavfile = 'leanon.wav'
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        print "song choosed"
                        firstop = True
                        wavfile = 'shakeitoff.wav'

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

        Type = 'n'
        n = 0
        effect_list = ['n', 'l', 'b', 'h', 'v']

        score = 0
        count = 0
        while True:
            
            # send to sound.py, process the sound
            n+=1
            input_string = wf.readframes(BLOCK)
            input_tuple = struct.unpack('h'*OUT, input_string)
            # call sound function to process effect
            output_string =  sound.main(input_tuple, RATE, Type, OUT, BLOCK, n ,kr)
            stream.write(output_string)

            # update with display
            self.update_display(score)
            for event in pygame.event.get():
                # print Type
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    window_size = (640,580)
                    count+=1
                    surf = pygame.display.set_mode(window_size)
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        if Type == 'n':
                            score +=10

                            self.display_box(surf, "BINGO!", "Your Score: %d" %score)
                            
                        else:
                            self.display_box(surf, "Sorry", "You are Wrong! :(")
                            
                        Type = random.choice(effect_list)   
                        
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        if Type == 'l':
                            score +=10
                            self.display_box(surf, "BINGO!", "Your Score: %d" %score)
                        else:
                            self.display_box(surf, "Sorry", "You are Wrong! :(")
                        Type = random.choice(effect_list)
                    
                    elif self.Button3.pressed(pygame.mouse.get_pos()):
                        if Type == 'b':
                            score +=10
                            self.display_box(surf, "BINGO!", "Your Score: %d" %score)
                        else:
                            self.display_box(surf,"Sorry", "You are Wrong! :(")
                        Type = random.choice(effect_list)   
                        
                    elif self.Button4.pressed(pygame.mouse.get_pos()):
                        if Type == 'h':
                            score +=10
                            self.display_box(surf, "BINGO!", "Your Score: %d" %score)
                        else:
                            self.display_box(surf,"Sorry", "You are Wrong! :(")
                        Type = random.choice(effect_list)   
                        
                    elif self.Button5.pressed(pygame.mouse.get_pos()):
                        if Type == 'v':
                            score +=10
                            self.display_box(surf, "BINGO!", "Your Score: %d" %score)
                        else:
                            self.display_box(surf, "Sorry", "You are Wrong! :(")
                        Type = random.choice(effect_list)

            if count>= 10:
                print "Your score: ", score
                break
        stream.stop_stream()
        stream.close()
        p.terminate()

    print 'done'
                    

if __name__ == '__main__':
    Type = 'n'
    obj = Button_Example(Type)
