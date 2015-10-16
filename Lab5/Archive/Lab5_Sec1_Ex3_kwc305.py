# play_randomly_plots.py
"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
It sounds like pings from a Sonar or from a Geiger Counter.
Gerald Schuller, March 2015 
Modified - Ivan Selesnick, October 2015
"""

import pyaudio
import struct
import random
from math import sin, cos, pi
from matplotlib import pyplot as plt
from myfunctions import clip16
# import numpy as np

BLOCKSIZE = 1024    # Number of frames per block
WIDTH = 2           # Bytes per sample
CHANNELS = 2
# 
RATE = 8000         # Sampling rate in Hz

# Parameters
T = 20       # Total play time (seconds)
Ta = 0.2    # Decay time (seconds)
f1 = random.randint(500,50000)    # Frequency (Hz)
# 
Ta1 = 0.9
f11 = random.randint(500,50000)
# Pole radius and angle
# despeed0 = random.uniform(0,1)
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
# 
om1 = 2.0 * pi * float(f1)/RATE

# Filter coefficients (second-order IIR)
a1 = -2*r*cos(om1)
a2 = r**2
b0 = sin(om1)
# 

# despeed1 = random.uniform(0,1)
r1 = 0.01**(1.0/(Ta1*RATE))       # 0.01 for 1 percent amplitude
# 
om11 = 2.0 * pi * float(f11)/RATE

# Filter coefficients (second-order IIR)
a11 = -2*r1*cos(om11)
a21 = r1**2
b01 = sin(om11)

NumBlocks = T * RATE / BLOCKSIZE

y = [0 for i in range(BLOCKSIZE)]
y1 = [0 for i in range(BLOCKSIZE)]
z = [0 for i in range(BLOCKSIZE*2)]

plt.ion()           # Turn on interactive mode so plot gets updated
fig = plt.figure(1)
line, = plt.plot(y,'blue')
line1, = plt.plot(y1,'yellow')
plt.ylim(-32000, 32000)
plt.xlim(0, BLOCKSIZE)
plt.xlabel('Time (n)')
plt.show()



# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

print 'Playing for {0:f} seconds ...'.format(T),

THRESHOLD = 2.5 / RATE          # For a rate of 2.5 impulses per second

# 
# Loop through blocks
for i in range(0, NumBlocks):

    o = random.uniform(0,1)

    # Do difference equation for block
    for n in range(BLOCKSIZE):

        rand_val = random.random()
        rand_val1 = random.random()
        
        if rand_val < THRESHOLD:
            x = 15000
        else:
            x = 0

        if rand_val1 < THRESHOLD:
            x1 = 15000
        else:
            x1 = 0
        
        y[n] = b0 * x - a1 * y[n-1] - a2 * y[n-2]  
        y1[n] = b01 * x1 - a11 * y1[n-1] - a21 * y1[n-2]  
        
        y[n] = clip16(y[n])
        y1[n] = clip16(y1[n])
        # print n
        z[2*n] = y[n]
        z[(2*n)+1] = y1[n]
        
        # print y
              # What happens when n = 0?
              # In Python negative indices cycle to end, so it works..

        

    line.set_ydata(y)
    line1.set_ydata(y1)
    plt.title('Block {0:d}'.format(i))
    plt.draw()

    # y = np.clip(y, -32000, 32000)     # Clipping using numpy if available

    # Convert numeric list to binary string
    data = struct.pack('hh' * BLOCKSIZE, *z);

    # Write binary string to audio output stream
    stream.write(data, BLOCKSIZE)

print 'Done.'

stream.stop_stream()
stream.close()
p.terminate()
