# kwc305 Kang-Wei Chang
# this program is now loading the wav file and then do the fourier transform.
# after the transform, set it to the db scale, shows on the matplotlib.
# idea: to do the equalier, with different input, comes with different effect.

import pyaudio,sys
import wave
import struct
import math
import numpy as np
import pygame
import random

global x_len
global y_len

x_len = 800
y_len = 700

x_posi = random.randint(1,x_len)
y_posi = random.randint(1,y_len)


# program start
def main():
    pygame.init()
    # set up the window
    global DISPLAYSURF 
    DISPLAYSURF = pygame.display.set_mode((x_len, y_len), 0, 32)
    pygame.display.set_caption('Drawing')
    wavfile = 'leanon1.wav'
    soundDB(wavfile)



def soundDB(wavfile):
    # from myfunctions import clip16
    # plt.ion()
    # wavfile = 'decay_cosine_mono.wav'
    print 'Play the wave file: {0:s}.'.format(wavfile)

    # Open wave file
    wf = wave.open( wavfile, 'rb')

    # Read wave file properties
    CHANNELS = wf.getnchannels()        # Number of channels
    RATE = wf.getframerate()            # Sampling rate (frames/second)
    LEN  = wf.getnframes()              # Signal length
    WIDTH = wf.getsampwidth()           # Number of bytes per sample
    BLOCK = 3072
    OUT = WIDTH * BLOCK
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


    for n in range(0, LEN):
        # print n 
        # Get sample from wave file
        input_string = wf.readframes(BLOCK)

        # Convert string to number
        input_tuple = struct.unpack('h'*OUT, input_string)
        # print input_value 
        X = np.fft.fft(input_tuple)
        X = np.log10(X) * 20
        value = int(np.max(abs(X)))
        if value>=154:
            output_value(value)

        output_string = struct.pack('h'*OUT, *input_tuple)
        stream.write(output_string)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print 'done'

def output_value(value):
    value = value
    drawdot(value)


def drawdot(value):
    # print input1
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)
    GREEN = (  0, 255,   0)
    BLUE  = (  0,   0, 255)
    # pygame.draw.polygon(DISPLAYSURF, GREEN, ((value, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    
    x_posi = random.randint(1,x_len)
    y_posi = random.randint(1,y_len)
    direction ='down'
    rock_x = x_posi
    rock_y = 10
    rock_img = pygame.image.load('rock.png')
    stop = False
    while stop==False:
        DISPLAYSURF.fill(BLACK)
        if direction=='down':
            rock_y+=50
            if rock_y>=y_len:
                stop=True
        DISPLAYSURF.blit(rock_img, (rock_x, rock_y))
        pygame.display.update()
    # for fall in range(0,y_len):
    #     pygame.draw.circle(DISPLAYSURF, BLUE, (x_posi, fall), 20, 0)


if __name__ == '__main__':
    main()

 
    
















