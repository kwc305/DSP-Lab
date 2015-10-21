# Lab6_Sec3_kwc305.py

"""
Using Pyaudio, get audio input and plot real-time FFT of blocks.
Ivan Selesnick, October 2015
Based on program by Gerald Schuller
"""

import pyaudio
import struct
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys
import wave

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 16000      	# Sampling rate (samples/second)
BLOCKSIZE = 1024
DURATION = 10       # Duration in seconds

NumBlocks = int( DURATION * RATE / BLOCKSIZE )
print NumBlocks
print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
print 'Running for ', DURATION, 'seconds...'

output_wf = wave.open('kwc305_bath.wav', 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Initialize plot window:
plt.figure(1)
plt.ylim(0, 100*np.log10(RATE))
plt.ylabel('dB')

# # Time axis in units of milliseconds:
plt.xlim(0, RATE)         # set x-axis limits
plt.xlabel('Frequency (Hz)')
# plt.xscale('log')
f = [n*float(RATE/BLOCKSIZE) for n in range(BLOCKSIZE)]

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(f)                         # x-data of plot (frequency)

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = False)


i = 0
while (True):

    for i in range(0, NumBlocks):
        input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
        input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert
        freq = np.fft.fft(input_tuple)
        freq = np.log10(freq)*20
        # print freq
        # print "@"
        # print type(freq)
        line.set_ydata(abs(freq))                               # Update y-data of plot
        # if i == NumBlocks/2:
       
        if freq.max() >= 130.0:
            print "Bigger than 130 dB"
            pp  = PdfPages('Bath.pdf')
            plt.savefig(pp, format='pdf')
            pp.close()
            output_tuple = struct.pack('h'*BLOCKSIZE,*freq)
            output_wf.writeframes(output_tuple)
            # do thing let it close
            sys.exit(0)

        plt.draw()

# plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
