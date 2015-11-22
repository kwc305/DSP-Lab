# Lab6_kwc305
"""
Using Pyaudio, record sound from the audio device and plot,
for 8 seconds, and display it live in a Window.
Usage example: python pyrecplotanimation.py
Gerald Schuller, October 2014 
"""

import pyaudio
import struct
import wave
import math
import cmath
import numpy as np
from matplotlib import pyplot as plt
import myfunctions

# Open wave file (mono)
wave_file_name = 'Sine_Wave_60Hz_30s.wav'
# wave_file_name = 'sin01_mono.wav'
# wave_file_name = 'sin01_stereo.wav'
wf = wave.open( wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 

print 'Rate =', RATE
print 'Width =', WIDTH
print 'Number of frames =', LEN
print 'Number of channels =', CHANNELS

def shift_array(l, n):
    return l[n:] + l[:n]

plt.ion()           # Turn on interactive mode so plot gets updated
BLOCKSIZE = 512
f0 = 0              # 'dock audio'

# Number of blocks in wave file
NumBlocks = int(math.floor(LEN/BLOCKSIZE))
# NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
# print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
plt.figure(1)
plt.ylim(-100, 180)        # set y-axis limits

plt.xlim(0, 1000)         # set x-axis limits
plt.xlabel('Time (n)')
# t = range(0, BLOCKSIZE)
t = range(0, RATE)

I = cmath.sqrt(-1)
filter_order = 4    # 4 order filter

# a = a_lpf * s
# b = b_lpf * s

a = np.array([ 1.0000000,  0.90507892,  0.59790786,  0.29073679,  0.19581571])
b = np.array([ 0.39133577,  0.59790786,  1.01105202,  0.59790786,  0.39133577])

# # Time axis in units of milliseconds:

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t)                         # x-data of plot (time)

# Create block (initialize to zero)
output_block = [0 for n in range(0, BLOCKSIZE)]
Y = [ 0 for i in range(0, filter_order+1) ] 
X = [ 0 for i in range(0, filter_order+1) ] 

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

for i in range(0, BLOCKSIZE):

    input_string = wf.readframes(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)    # Convert

    # Go through data
    for n in range(0, BLOCKSIZE):

        X[4] = input_tuple[n]
        Yvalue = a[1] * Y[3] + a[2] * Y[2] + a[3] * Y[1] + a[4] * Y[0]
        Y[4] = b[0] * X[4] + b[1] * X[3] + b[2] * X[2] + b[3] * X[1] + b[4] * X[0] - Yvalue
        
        output_block[n] = np.real(4.0 * Y[4] * cmath.exp(I * 2 *math.pi*n*f0/RATE))
        # shift array
        shift_array(Y,1)
        shift_array(X,1)


    # line.set_ydata(output_block)                               # Update y-data of plot
    # plt.draw()
    output_block_fft = np.fft.fft(output_block,RATE)
    print len(output_block_fft),BLOCKSIZE
    line.set_ydata(np.log10(output_block_fft)*20)
    plt.draw()
    for n in range(0,BLOCKSIZE):
        output_block[n] = myfunctions.clip16(output_block[n])
    # Convert values to binary string
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)
    stream.write(output_string)
plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
