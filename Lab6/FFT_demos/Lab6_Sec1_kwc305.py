# plot_micinput_spectrum.py

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

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 16000      	# Sampling rate (samples/second)
BLOCKSIZE = 1024
DURATION = 10       # Duration in seconds

NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks
print 'Running for ', DURATION, 'seconds...'

# Initialize plot window:
plt.figure(1)
plt.ylim(0, 100*np.log10(RATE))
plt.ylabel('dB')

# plt.xlim(0, 1000*np.log10(RATE))         # set x-axis limits
# plt.xlabel('Frequency (k)')
# f = np.linspace(0, BLOCKSIZE-1, BLOCKSIZE)

# # Time axis in units of milliseconds:
plt.xlim(1, np.log10(RATE/2))
# plt.xscale('log')
# plt.xticks([1,200,500])
plt.xlabel('Log (Hz)')

f = [np.log10(n*float(RATE/BLOCKSIZE)) for n in range(BLOCKSIZE)]

line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(f)                         # x-data of plot (frequency)
# plt.xscale('log')
# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = False)




for i in range(0, NumBlocks):
    input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert
    
    X = np.fft.fft(input_tuple)
    X = np.log10(X)*20
    print X[i]
    line.set_ydata(np.abs(X))                               # Update y-data of plot
    if i == NumBlocks/2:
        pp  = PdfPages('spectrum.pdf')
        plt.savefig(pp, format='pdf')
        pp.close()
    plt.draw()
plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'
