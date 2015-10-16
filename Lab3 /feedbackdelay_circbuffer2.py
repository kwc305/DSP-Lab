# feedbackdelay_circbuffer2.py
# Reads a specified wave file (mono) and plays it with a delay with feedback.
# This implementation uses a circular buffer with
# two buffer indices.

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

wavfile = "author.wav"
print("Play the wave file %s." % wavfile)

# Open the wave file
wf = wave.open( wavfile, 'rb')

# Read the wave file properties
num_channels = wf.getnchannels()        # Number of channels
Fs = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()        # Signal length
width = wf.getsampwidth()               # Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % Fs)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)

# Set parameters of delay system
Gfb = 0.5           # feed-back gain
Gdp = 0.8           # direct-path gain
Gff = 2.2           # feed-forward gain
# Gff = 0.0         # feed-forward gain (set to zero for no effect)

buffer_MAX =  2**10 # set the length of buffer
#buffer_MAX =  801

delay_sec = 0.05 # 50 milliseconds
delay_samples = int( math.floor( Fs * delay_sec ) ) 

print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))

buffer = [ 0.0 for i in range(buffer_MAX) ]   

p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = Fs,
                input       = False,
                output      = True )

# Get first frame (sample)
input_string = wf.readframes(1)

# Delay line (buffer) index
kr = 0  # read 
kw = delay_samples  # write

print ("**** Playing ****")

while input_string != '':

    # Convert string to number
    input_value = struct.unpack('h', input_string)[0]

    # Compute output value
    output_value = Gdp * input_value + Gff * buffer[kr];

    # Update buffer
    buffer[kw] = input_value + Gfb * buffer[kr]

    # Increment buffer indices    
    kr += 1
    if kr == buffer_MAX:
        # We have reached the end of the buffer. Circle back to front.
        kr = 0

    kw += 1
    if kw == buffer_MAX:
        # We have reached the end of the buffer. Circle back to front.
        kw = 0

    # Clip output value to 16 bits and convert to binary string
    output_string = struct.pack('h', clip16(output_value))

    # Write output value to audio stream
    stream.write(output_string)

    # Get next frame (sample)
    input_string = wf.readframes(1)     

print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate() 

