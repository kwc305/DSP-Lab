# recplayAM_mono.py
# Record audio and play it with amplitude modulation. 
# This implementation:
#   uses blocking, 
#   corrects for block-to-block angle mismatch,
#   assumes mono channel
"""
Read a signal from a wave file, do amplitude modulation, play to output
Original: pyrecplay_modulation.py by Gerald Schuller, Octtober 2013
Modified to read a wave file - Ivan Selesnick, September 2015
"""

import pyaudio
import struct
import math

# f0 = 0      # Normal audio
f0 = 400    # 'Duck' audio
f1 = 900
BLOCKSIZE = 64  # Number of frames per block

WIDTH = 2       # Number of bytes per sample
CHANNELS = 2    # mono
RATE = 32000    # Sampling rate (samples/second)
RECORD_SECONDS = 10

p = pyaudio.PyAudio()

number_of_devices = p.get_device_count()
print('There are {0:d} devices'.format(number_of_devices))

property_list = ['defaultSampleRate', 'maxInputChannels', 'maxOutputChannels']
for i in range(0, number_of_devices):
    print('Device {0:d} has:'.format(i))
    for s in property_list:
        print ' ', s, '=', p.get_device_info_by_index(i)[s]

stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)

output_block1 = [0 for i in range(0, BLOCKSIZE)]
output_block2 = [0 for i in range(0, BLOCKSIZE)]
# input_tuple1 = [0 for i in range(0, BLOCKSIZE)]
# input_tuple2 = [0 for i in range(0, BLOCKSIZE)]
result = [0 for i in range(0, BLOCKSIZE*2)]
# Initialize angle
theta = 0.0
theta1 =0.0
# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f0)/RATE - math.floor(BLOCKSIZE*f0/RATE)) * 2.0 * math.pi
theta_del1 = (float(BLOCKSIZE*f1)/RATE - math.floor(BLOCKSIZE*f1/RATE)) * 2.0 * math.pi

# Number of blocks to run for
num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

print('* Recording for {0:.3f} seconds'.format(RECORD_SECONDS))
b=0
# Start loop
for i in range(0, num_blocks):
    b+=1
    print b
    input_tuple1 = []
    input_tuple2 = []
    output_block1 = [0 for i in range(0, BLOCKSIZE)]
    output_block2 = [0 for i in range(0, BLOCKSIZE)]

    # Get frames from audio input stream
    input_string = stream.read(BLOCKSIZE)       # BLOCKSIZE = number of frames read

    # Convert binary string to tuple of numbers
    input_tuple = struct.unpack('hh' * BLOCKSIZE, input_string)
    
    # print input_tuple
    
    # add for loop for put tuple
    for a in range(0, BLOCKSIZE):
        input_tuple1.append( input_tuple[2*a])
        input_tuple2.append( input_tuple[2*a+1])
    # print input_tuple1
    # print input_tuple2
    # input_tuple2 = struct.unpack('h' * (BLOCKSIZE), input_string[1])   
    # Go through block
    for n in range(0, BLOCKSIZE):
        # No processing:
        # samples[n] = input_tuple[n]  
        # OR
        # Amplitude modulation:
        
        output_block1[n] = input_tuple1[n] * math.cos(2*math.pi*n*f0/RATE + theta)
        output_block2[n] = input_tuple2[n] * math.sin(2*math.pi*n*f1/RATE + theta)
    # Set angle for next block
    theta = theta + theta_del
    theta1 = theta1 + theta_del1
    
    # append block2 to block1
    print output_block1
    print "**************"
    print output_block2 
    result = []
    for a in range(0,len(output_block2)):
        result.append(output_block1[a])
        result.append(output_block2[a])
    # print output_block1
    # Convert values to binary string
    # print result
    output_string = struct.pack('hh' * BLOCKSIZE, *result)

    # Write binary string to audio output stream
    stream.write(output_string)

print('* Done')

stream.stop_stream()
stream.close()
p.terminate()
