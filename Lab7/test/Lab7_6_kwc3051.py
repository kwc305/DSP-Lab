# play_vibrato_interpolation.py
# Reads a specified wave file (mono) and plays it with a vibrato effect
# (sinusoidal time-varying delay).
# This implementation:
#   uses a circular buffer with two buffer indices,
#   uses linear interpolation,
#   saves output as a wave file

import pyaudio
import wave
import struct
import math
import cmath
from myfunctions import clip16
import scipy.signal as signal
import numpy as np

wavfile = 'author.wav'
# wavfile = 'decay_cosine_mono.wav'
print 'Play the wave file: {0:s}.'.format(wavfile)

# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties
CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample
BLOCKSIZE = 512
print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato parameters
f0 = 3
Q = 2
W0 = 1.0
W=2
I = cmath.sqrt(-1)
# Create a buffer (delay line) for past values

# Buffer (delay line) indices
kr0 = 0
kw0 = BLOCKSIZE/2
buffer0 = [0.0 for i in range(BLOCKSIZE)]   
output_block = [0.0 for n in range(0,BLOCKSIZE)]
theta0 = 0.0
theta_del0 = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi
# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
# print 'The buffer is {0:d} samples long.'.format(buffer_MAX)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )

output_all = ''            # output signal in all (string)
I = np.sqrt(-1)
print ('* Playing...')
b = [r**2,-2*r*np.cos(RATE*)]
a = []
# Loop through wave file 
for n in range(0, LEN):
    # print n
        # Get sample from wave file
    input_string = wf.readframes(BLOCKSIZE)
    input_value = struct.unpack('h' * BLOCKSIZE, input_string)
        # Convert string to number
    output_block = signal.filtfilt(b,a,input_value)
    output_block = np.real(W*math.exp(I*cmath.pi*n*Q)*output_block)
    
    for n in range(0,BLOCKSIZE):
        output_block[n] = clip16(output_block[n]+input_value[n])
       
    output_string = struct.pack('h'*BLOCKSIZE, *output_block)

    # Write output to audio stream
    stream.write(output_string)

    output_all = output_all + output_string     # append new to total

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()

print('* Done')

