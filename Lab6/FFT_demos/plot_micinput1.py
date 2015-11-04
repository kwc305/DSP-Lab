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
from matplotlib import pyplot as plt
import wave
import time
import numpy as np

filename = 'author.wav'


plt.ion()           # Turn on interactive mode so plot gets updated

# WIDTH = 2           # bytes per sample
# CHANNELS = 1        # mono
# RATE = 16000        # Sampling rate (samples/second)
BLOCKSIZE = 1024
DURATION = 10  		# Duration in seconds



#print ('BLOCKSIZE =', BLOCKSIZE
# print 'NumBlocks =', NumBlocks
#print ('Running for '), DURATION, ('seconds...'

wf = wave.open( filename, 'rb')

# Read wave file properties
CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

NumBlocks = int( DURATION * RATE / BLOCKSIZE )
# Duration = (1/)

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)


# Initialize plot window:
plt.figure(1)
plt.ylim(0.0, 10000)        # set y-axis limits

plt.xlim(0, LEN)         # set x-axis limits
plt.xlabel('Time (n)')
t = range(0, BLOCKSIZE)

# # Time axis in units of milliseconds:
# plt.xlim(0, 1000.0*BLOCKSIZE/RATE)         # set x-axis limits
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
                output = False)



for i in range(0, int(LEN/BLOCKSIZE)):
	
	# print i
	# input_string = stream.read(BLOCKSIZE)                     # Read audio input stream
	input_string = wf.readframes(BLOCKSIZE)
	# print len(input_string)
	input_tuple = struct.unpack('h'*BLOCKSIZE, input_string)  # Convert
	input_tuple= input_tuple * np.cos(2*np.pi*RATE)
	line.set_ydata(input_tuple)                               # Update y-data of plot
	plt.draw()
	time.sleep(1)
# plt.close()

stream.stop_stream()
stream.close()
p.terminate()

# print '* Done'
