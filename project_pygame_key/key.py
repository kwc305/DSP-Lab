
import pyaudio,sys
import wave
import struct
import math
import numpy as np
import pygame
import random

def main():
	wavfile = 'leanon.wav'
	wf = wave.open( wavfile, 'rb')

	# Read wave file properties
	CHANNELS = wf.getnchannels()        # Number of channels
	RATE = wf.getframerate()            # Sampling rate (frames/second)
	LEN  = wf.getnframes()              # Signal length
	WIDTH = wf.getsampwidth()           # Number of bytes per sample
	BLOCK = 3072
	OUT = WIDTH * BLOCK
	print('The file has %d channel(s).'         % CHANNELS)
	print('The file has %d frames/second.'      % RATE)
	print('The file has %d frames.'             % LEN)
	print('The file has %d bytes per sample.'   % WIDTH)

	p = pyaudio.PyAudio()
	stream = p.open(format      = pyaudio.paInt16,
	                channels    = 2,
	                rate        = RATE,
	                input       = False,
	                output      = True )


	for n in range(0, LEN):
	    # print n 
	    # Get sample from wave file
	    input_string = wf.readframes(BLOCK)

	    # Convert string to number
	    input_tuple = struct.unpack('h'*OUT, input_string)
	    # print input_value 
	    X = np.fft.fft(input_tuple)
	    X = np.log10(X) * 20
	    value = int(np.max(abs(X)))
	    if value>=154:
	       print value

	    output_string = struct.pack('h'*OUT, *input_tuple)
	    stream.write(output_string)

	stream.stop_stream()
	stream.close()
	p.terminate()

	print 'done'


if __name__ == '__main__':


	
	main()
