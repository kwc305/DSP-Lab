# Lab6_kwc305
"""
Using Pyaudio, record sound from the audio device and plot,
for 8 seconds, and display it live in a Window.
Usage example: python pyrecplotanimation.py
Gerald Schuller, October 2014 
Modified: Ying-Ta Lin, October 2015
"""

import pyaudio
import struct
import wave
import math
import cmath
import numpy as np
from matplotlib import pyplot as plt

# Open wave file (mono)
wave_file_name = 'author.wav'
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
BLOCKSIZE = 1024
f0 = 400              # 'dock audio'

# Number of blocks in wave file
NumBlocks = int(math.floor(LEN/BLOCKSIZE))
# NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
# print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
plt.figure(1)
plt.ylim(-10000, 10000)        # set y-axis limits

plt.xlim(0, BLOCKSIZE)         # set x-axis limits
plt.xlabel('Time (n)')
t = range(0, BLOCKSIZE)

I = cmath.sqrt(-1)
filter_order = 7    # 7 order filter

# a = a_lpf * s
# b = b_lpf * s

a = np.array([1.0000,1.2762*I,-2.6471,2.2785*I,2.1026,1.1252*I,-0.4876,0.1136*I])
b = np.array([0.0423,0.1193*I,-0.2395,0.3208*I,0.3208,0.2395*I,-0.1193,-0.0423*I])

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
                input = True,
                output = True)

for i in range(0, BLOCKSIZE):
    input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)    # Convert

    # Go through data
    for n in range(0, BLOCKSIZE):

        X[7] = input_tuple[n]
        Yvalue = a[1] * Y[6] + a[2] * Y[5] + a[3] * Y[4] + a[4] * Y[3] + a[5] * Y[2] + a[6] * Y[1] + a[7] * Y[0]
        Y[7] = b[0] * X[7] + b[1] * X[6] + b[2] * X[5] + b[3] * X[4] + b[4] * X[3] + b[5] * X[2] + b[6] * X[1] + b[7] * X[0]- Yvalue
        
        output_block[n] = np.real(8.0 * Y[7] * cmath.exp(I * 2 *math.pi*n*f0/RATE))
        # shift array
        shift_array(Y,1)
        shift_array(X,1)

    line.set_ydata(output_block)                               # Update y-data of plot
    plt.draw()
    # Convert values to binary string
    output_string = struct.pack('h' * BLOCKSIZE, *output_block)
    stream.write(output_string)
plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
