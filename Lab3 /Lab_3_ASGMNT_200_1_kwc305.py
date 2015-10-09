import pyaudio
import wave
import struct
import math
from myfunctions import clip16

wavfile = "04 04. Grandma (Wai Po).mp3"
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

# set parameter of delay system
gain = 1
gain_delay = 0.8
delay_sec = 0.2
delay_samples = int( math.floor( Fs * delay_sec))

print('The delay of {0:.3f} seconds is {1:d} samples.'.format(delay_sec, delay_samples))

buffer = [ 0 for i in range(delay_samples) ]

p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = Fs,
                input       = False,
                output      = True )




# Get first frame (sample)
input_string = wf.readframes(1)


k =0
print ("*** playing ***")


while input_string != '' :
	# Convert string to number
	
	input_value = struct.unpack('h', input_string)[0]
	# print input_value
	# print '*******************'

	# compute the output value
	output_value = gain * input_value + gain_delay * buffer[k]
	output_value = clip16(output_value)

	# update buffer
	buffer[k] = input_value
	k = k + 1
	if k >= delay_samples:
		k = 0

	# convert output value to binary string
	output_string = struct.pack('h', output_value)

	# write output value to audio stream
	stream.write(output_string)

	# get next frame(sample)

	input_string = wf.readframes(1)

print "sssssssss"

# while buffer[k] != '' :
	# Convert string to number
	
	input_value = struct.unpack('h', input_string)[0]
	# print input_value
	# print '*******************'

	# compute the output value
	output_value = gain * input_value + gain_delay * buffer[k]
	output_value = clip16(output_value)
	
	# update buffer
	buffer[k] = input_value
	k = k + 1
	if k >= delay_samples:
		k = 0

	# convert output value to binary string
	output_string = struct.pack('h', output_value)

	# write output value to audio stream
	stream.write(output_string)

	# get next frame(sample)

	input_string = wf.readframes(1)

print ("**** Done ****")
stream.stop_stream()
stream.close()
p.terminate()












