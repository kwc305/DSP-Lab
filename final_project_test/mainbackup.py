
import pyaudio,sys
import wave
import struct
import math
import numpy as np
import pygame
import random
import scipy.signal as signal
import myfunctions



arg1 =  sys.argv[1]
if  arg1!='lowpass' and arg1!='highpass' and arg1!='bandstop' and arg1 != 'vibrato' :
	print "Usage: python key.py filtertype ex: lowpass/highpass/bandpass"
	sys.exit(0)


def highpassfilter(input_tuple,RATE):
	# high pass
	fs_Hz = RATE
	b1, a1 = signal.butter(4,0.8, 'high')
	output_value1 = signal.filtfilt(b1,a1,input_tuple)
	return output_value

def lowpassfilter(input_tuple,RATE):
	# lowpass
	fs_Hz = RATE
	b1, a1 = signal.butter(4,0.05, 'low')
	output_value = signal.filtfilt(b1,a1,input_tuple)
	return output_value

def bandstopfilter(input_tuple,RATE):
	fs_Hz = RATE
	bp_stop_Hz = np.array([500.0, 5000.0])
	b1, a1 = signal.butter(2,bp_stop_Hz/(fs_Hz / 2.0), 'bandstop')
	output_value = signal.filtfilt(b1,a1,input_tuple)
	return output_value

def vibrato(input_tuple,RATE,BLOCK,n,kr):
	BLOCK = BLOCK*2
	W = 0.6
	W1 = 0.0
	kw = BLOCK/2
	f0 = 2
	frac = 0
	# print len(input_tuple)
	buffer1 = [0.0 for n in range(0,BLOCK)]
	output_value = [0.0 for n in range(0,BLOCK)]
	for i in range(0,BLOCK):
		output_sample = ((1-frac) * buffer1[int(kr) - 1] + frac * buffer1[int(kr)]) / 2
		buffer1[kw] = input_tuple[i]
		kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * i  /RATE)
		frac =  W * math.sin( 2 * math.pi * f0 * i/RATE)
		if kr >= BLOCK:
			kr = 0
		# print kr
		kw = kw + 1
		if kw == BLOCK:
			kw = 0
		output_value[i] = myfunctions.clip16(W1*input_tuple[i] + output_sample)
		# print output_value
	return output_value

def main():
	wavfile = 'leanon.wav'
	wf = wave.open( wavfile, 'rb')

	# Read wave file properties
	CHANNELS = wf.getnchannels()        # Number of channels
	RATE = wf.getframerate()            # Sampling rate (frames/second)
	LEN  = wf.getnframes()              # Signal length
	WIDTH = wf.getsampwidth()           # Number of bytes per sample
	BLOCK = 4096
	if arg1 == "vibrato":
		BLOCK = 512
	OUT = WIDTH * BLOCK
	kr = 0 #vibrato's read index
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
	    if arg1 == "lowpass":
		    output_value = lowpassfilter(input_tuple,RATE)
	    elif arg1 == "highpass":
	    	output_value = highpassfilter(input_tuple,RATE)
	    elif arg1 == "bandstop":
	    	output_value = bandstopfilter(input_tuple,RATE)
	    elif arg1 == "vibrato":
	    	output_value = vibrato(input_tuple,RATE,BLOCK,n,kr)

	    for n in range(0,len(output_value)):   
	    	output_value[n] = myfunctions.clip16(output_value[n])
	    output_string = struct.pack('h'*OUT, *output_value)
	    stream.write(output_string)

	stream.stop_stream()
	stream.close()
	p.terminate()

	print 'done'


if __name__ == '__main__':


	
	main()
