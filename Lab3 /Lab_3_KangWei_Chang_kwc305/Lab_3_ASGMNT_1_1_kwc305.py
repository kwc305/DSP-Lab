# play_wav_stereo.py

import pyaudio
import wave
import struct
import math
import sys




def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return int(x)

def stereochannel(input_string):
	input_string = input_string
	while input_string != '':
		# Convert string to numbers
		input_tuple = struct.unpack('hh', input_string)  # produces a two-element tuple

		# Compute output values
		output_value0 = clip16(gain * input_tuple[0])
		output_value1 = clip16(gain * input_tuple[1])

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

def monochannel(input_string):
	input_string = input_string
	while input_string != '':

		# Convert string to number
		input_value = struct.unpack('h', input_string)[0]
		# ... equivalently:
		# input_tuple = struct.unpack('h', input_string)  # One-element tuple
		# input_value = input_tuple[0]                    # Number
   	
		# Compute output value
		output_value = clip16(gain * input_value)    # Number

		# Convert output value to binary string
		output_string = struct.pack('h', output_value)  

		# Write output value to audio stream
		stream.write(output_string)                     

		# Get next frame
		input_string = wf.readframes(1)

	print("**** Done ****")

	stream.stop_stream()
	stream.close()
	p.terminate()
gain = 0.5

# wavfile = "cat01.wav"
# wavfile = 'sin01_mono.wav'
wavfile = sys.argv[1]

print("Play the wave file %s." % wavfile)

wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
num_channels = wf.getnchannels()       	# Number of channels
Fs = wf.getframerate()                  # Sampling rate (frames/second)
signal_length  = wf.getnframes()       	# Signal length
width = wf.getsampwidth()       		# Number of bytes per sample

# print("The file has %d channel(s)."            % num_channels)
# print("The frame rate is %d frames/second."    % Fs)
# print("The file has %d frames."                % signal_length)
# print("There are %d bytes per sample."         % width)

p = pyaudio.PyAudio()

stream = p.open(format      = pyaudio.paInt16,
                channels    = num_channels,
                rate        = Fs,
                input       = False,
                output      = True )

input_string = wf.readframes(1)          # Read first frame



if num_channels == 1:
	monochannel(input_string)
else:
	stereochannel(input_string)


