# play_wav_stereo.py

import pyaudio
import wave
import struct
import math

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)

gain = 0.9
gain1 = 0.8
# wavfile = "cat01.wav"
# wavfile = 'sin01_mono.wav'
wavfile = 'sin01_stereo.wav'

print("Play the wave file %s." % wavfile)

wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()       	# Number of channels
Fs = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

print("The file has %d channel(s)."            % num_channels)
print("The frame rate is %d frames/second."    % Fs)
print("The file has %d frames."                % signal_length)
print("There are %d bytes per sample."         % width)

# ----------------------------------

# Set parameters of delay system
Gfb = 0.8       # feed-back gain
g0 = 0.9        # direct-path gain
g11 =  1.0       # a feed-forward gain
               # a feed-forward gain
g21 = 1.0
# g22 = 0.8
# Set g0 = Gdp, g1 = 0, g2 = Gff to recover system in feedbackdelay_circbuffer.py
#  (Check..)

delay1_sec = 0.4
delay2_sec = 0.5   # delay2_sec > delay1_sec

delay1 = int( math.floor( Fs * delay1_sec ) )    # Delay in samples
delay2 = int( math.floor( Fs * delay2_sec ) ) 

# Create a delay line (buffer) to store past values. Initialize to zero.

buffer_length1 = delay1
buffer_length2 = delay2      # minimal-length buffer
buffer1 = [ 0 for i in range(buffer_length1) ]  
buffer2 = [ 0 for j in range(buffer_length2) ]   

print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay1_sec, delay1))
print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay2_sec, delay2))
print('My buffer is of length {0:d}'.format(buffer_length1))

# ----------------------------------

p = pyaudio.PyAudio()

stream = p.open(format      = pyaudio.paInt16,
                channels    = num_channels,
                rate        = Fs,
                input       = False,
                output      = True )

input_string = wf.readframes(1)          # Read first frame



k = 0
m1 = 2
m11 = 0
m2 = 2
m22 =0

print ("****  playing  ****")
while input_string != '':

    # Convert string to numbers
    input_tuple = struct.unpack('hh', input_string)  # produces a two-element tuple


    buffer1[k] = gain * input_tuple[0] 
    buffer2[k] = gain1 * input_tuple[1] 

    # Compute output values
    output_value0 = clip16(gain * input_tuple[0] + g11 * buffer2[m2-1])
    output_value1 = clip16(gain1 * input_tuple[1] + g21 * buffer1[m1-1] )

    

    k = k + 1
    m1 = m1 + 1
    m2 = m2 + 1
    if k == buffer_length1:
        k = 0
    if m1 >= buffer_length1:
        m1 = 0
    if m2 >= buffer_length2:
        m2 = 0

    # Convert output value to binary string
    output_string = struct.pack('hh', output_value0, output_value1)

    # Write output value to audio stream
    stream.write(output_string)

    # Get next frame
    input_string = wf.readframes(1)

print("**** Done ****")

stream.stop_stream()
stream.close()
p.terminate()






