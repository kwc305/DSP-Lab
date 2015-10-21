# plot_micinput_ver.py
"""
Using Pyaudio, record sound from the audio device and plot,
for 8 seconds, and display it live in a Window.
Usage example: python pyrecplotanimation.py
Gerald Schuller, October 2014 
Modified: Ivan Selesnick, September 2015
"""

import pyaudio
import struct
import numpy as np
from matplotlib import pyplot as plt
import myfunctions

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 16000        # Sampling rate (samples/second)
BLOCKSIZE = 1024
DURATION = 10  		# Duration in seconds

NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
plt.figure(1)
plt.ylim(0, 300)        # set y-axis limits

plt.xlim(0, BLOCKSIZE)         # set x-axis limits
plt.xlabel('Freq (Hz)')
plt.ylabel('dB')
Size = BLOCKSIZE/2+1
print Size
t = range(0, Size)

# # Time axis in units of milliseconds:
# plt.xlabel('Time (msec)')
# t = [n*1000/float(RATE) for n in range(BLOCKSIZE)]

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(t)                         # x-data of plot (time)
 
# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)


for a in range(0,NumBlocks):
    input_string = stream.read(BLOCKSIZE)
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)
    input_tuple =input_tuple * np.cos(2*np.pi*RATE*a)
    input_freq =np.fft.rfft(input_tuple)
    xx = 0-1j
    input_freq = input_freq * np.exp(xx*a)
    # print len(input_freq)
    output_tuple = np.fft.ifft(input_freq)
    # for i in range(0,len(output_tuple)):
    #     output_tuple[i] = myfunctions.clip16(output_tuple[i])

    output_result = 20 * np.log10 (output_tuple)
    output_string = struct.pack('h'*len(output_result),*output_tuple)
    stream.write(output_string)
    line.set_ydata(output_result)
    plt.draw()

y0 = 0

for n in range(0,NumBlocks):

    if n == 0:
        x0=7.0
    else:
        x0=0.0

    y0 = x0 -a1*y1-a2*y2






stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
