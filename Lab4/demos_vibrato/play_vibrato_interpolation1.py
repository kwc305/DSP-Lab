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
from myfunctions import clip16

# wavfile = 'author.wav'
# wavfile = 'decay_cosine_mono.wav'
# print 'Play the wave file: {0:s}.'.format(wavfile)

# Open wave file
# wf = wave.open( wavfile, 'rb')

# Read wave file properties
BLOCKSIZE = 64  # Number of frames per block

WIDTH = 2       # Number of bytes per sample
CHANNELS = 2    # mono
RATE = 50000    # Sampling rate (samples/second)
# RECORD_SECONDS = 10
buffer_MAX =  1024  
p = pyaudio.PyAudio()

# num_blocks = int(RATE / buffer_MAX * RECORD_SECONDS)


# Vibrato parameters
f0 = 5
f1 = 5
W = 0.0
W1 =0.5
# W = 0 # for no effct


# Create a buffer (delay line) for past values
#                         # Buffer length
buffer1 = [0.0 for i in range(buffer_MAX)]   # Initialize to zero
buffer2 = [0.0 for i in range(buffer_MAX)]   # Initialize to zero

# Buffer (delay line) indices
kr = 0  # read index
kr1 = 0
kw = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
kw = buffer_MAX/2
kw1 = int(0.5 * buffer_MAX)  # write index (initialize to middle of buffer)
kw1 = buffer_MAX/2

# print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))
print 'The buffer is {0:d} samples long.'.format(buffer_MAX)

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format      = p.get_format_from_width(WIDTH),
                channels    = CHANNELS,
                rate        = RATE,
                input       = True,
                output      = True )

output_all = ''            # output signal in all (string)

print ('* Playing...')

# Loop through wave file 
for n in range(0, buffer_MAX):

    input_tuple1 = []
    input_tuple2 = []
    # output_block1 = [0 for i in range(0, buffer_MAX)]
    # output_block2 = [0 for i in range(0, buffer_MAX)]

    # Get sample from recorder
    input_string = stream.read(buffer_MAX)       

    # Convert string to number
    # input_value = struct.unpack('h', input_string)[0]
    input_tuple = struct.unpack('hh' * buffer_MAX, input_string)
    # print len(input_tuple)
    
    # Get previous and next buffer values (since kr is fractional)
   
    # print kr_next , kr_next1
    
    # Update buffer (pure delay)
    # buffer1[kw] = input_value
    for a in range(0, buffer_MAX):
        buffer1[a] = input_tuple[2*a]
        buffer2[a] = input_tuple[(2*a)+1]

    # do the computation
    # Compute output value using interpolation
    for a in range(0, buffer_MAX/2):
        

        kr_prev = int(math.floor(kr))               
        kr_next = kr_prev + 1
        frac = kr - kr_prev    # 0 <= frac < 1
        if kr_next >= buffer_MAX:
            kr_next = kr_next - buffer_MAX

        kr_prev1 = int(math.floor(kr1))               
        kr_next1 = kr_prev1 + 1
        frac1 = kr1 - kr_prev1    # 0 <= frac < 1
        if kr_next1 >= buffer_MAX:
            kr_next1 = kr_next1 - buffer_MAX

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
        kr1 = kr1 + 1 + W1 * math.sin( 2 * math.pi * f1 * n / RATE )
        # Note: kr is fractional (not integer!)        
        # Ensure that 0 <= kr < buffer_MAX
        if kr >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr = 0

        # Increment write index    
        kw = kw + 1
        if kw == buffer_MAX:
            # End of buffer. Circle back to front.
            kw = 0

        if kr1 >= buffer_MAX:
            # End of buffer. Circle back to front.
            kr1 = 0

        # Increment write index    
        kw1 = kw1 + 1
        if kw1 == buffer_MAX:
        
            # End of buffer. Circle back to front.
            kw1 = 0
        # add to new buffer
        output_value1 = []
        output_value2 = []
        buffer1[a] = ( (1-frac) * buffer1[kr_prev] + frac * buffer1[kr_next])
        buffer2[a] =( (1-frac1) * buffer2[kr_prev1] + frac1 * buffer2[kr_next1])
        
   # print frac, frac1
    result = []
    # print "1",buffer1
    # print "***********"
    # print "2",buffer2
    # print "***********"
    for a in range(0, len(buffer2)):
        result.append(buffer1[a])
        result.append(buffer2[a])


    output_string = struct.pack('hh'*buffer_MAX, *result)

    # Write output to audio stream
    stream.write(output_string)

    output_all = output_all + output_string     # append new to total
    # print output_all

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()

