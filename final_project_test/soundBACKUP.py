
import pyaudio,sys
import wave
import struct
import math
import numpy as np
import pygame
import random
import time
import scipy.signal as signal
import myfunctions




def highpassfilter(input_tuple,RATE):
	# high pass
	fs_Hz = RATE
	b1, a1 = signal.butter(4,0.8, 'high')
	output_value = signal.filtfilt(b1,a1,input_tuple)
	for n in range(0,len(output_value)):
		output_value[n] = myfunctions.clip16(output_value[n])
	return output_value

def lowpassfilter(input_tuple,RATE):
	# lowpass
	fs_Hz = RATE
	b1, a1 = signal.butter(4,0.05, 'low')
	output_value = signal.filtfilt(b1,a1,input_tuple)
	for n in range(0,len(output_value)):
		output_value[n] = myfunctions.clip16(output_value[n])
	return output_value

def bandstopfilter(input_tuple,RATE):
	fs_Hz = RATE
	bp_stop_Hz = np.array([200.0, 1000.0])
	b1, a1 = signal.butter(4,bp_stop_Hz/(fs_Hz / 2.0), 'bandstop')
	output_value = signal.filtfilt(b1,a1,input_tuple)
	for n in range(0,len(output_value)):
		output_value[n] = myfunctions.clip16(output_value[n])
	return output_value

def vibrato(input_tuple,RATE,BLOCK,n,kr):
	BLOCK = BLOCK*2
	W = 0.6
	W1 = 0.0
	kw = BLOCK/2
	f0 = 0.1
	frac = 0
	# print len(input_tuple)
	buffer1 = [0.0 for n in range(0,BLOCK)]
	output_value = [0.0 for n in range(0,BLOCK)]
	for i in range(0,BLOCK):
		output_sample = ((1-frac) * buffer1[int(kr) - 1] + frac * buffer1[int(kr)]) / 2
		buffer1[kw] = input_tuple[i]
		kr = kr + 1 
		# + W * math.sin( 2 * math.pi * f0 * n  /RATE)
		frac =  W * math.sin( 2 * math.pi * f0 * n/RATE)
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
	BLOCK = 1024
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
	pygame.init()
	
	
	while True:
		for event in pygame.event.get(pygame.KEYDOWN):
			print (event.key)
			if (event.key == 113):
				sys.exit(1)

			elif (event.key == 108): # press l
				print 'do the sound signal with low pass'
				while True:
					input_string = wf.readframes(BLOCK)
					input_tuple = struct.unpack('h'*OUT, input_string)
					output_value = lowpassfilter(input_tuple,RATE)
					output_string = struct.pack('h'*OUT, *output_value)
					stream.write(output_string)
					if pygame.event.get(pygame.KEYDOWN) :
						print 'stop'
						break

			elif (event.key == 104): # press h 
				print 'do the sound signal with high pass'
				while True:
					input_string = wf.readframes(BLOCK)
					input_tuple = struct.unpack('h'*OUT, input_string)
					output_value = highpassfilter(input_tuple,RATE)
					output_string = struct.pack('h'*OUT, *output_value)
					stream.write(output_string)
					if pygame.event.get(pygame.KEYDOWN) :
						print 'stop'
						break

			elif (event.key == 98): # press b
				print 'do the sound signal with vibrato'
				while True:
					input_string = wf.readframes(BLOCK)
					input_tuple = struct.unpack('h'*OUT, input_string)
					output_value = bandstopfilter(input_tuple,RATE)
					output_string = struct.pack('h'*OUT, *output_value)
					stream.write(output_string)
					if pygame.event.get(pygame.KEYDOWN) :
						print 'stop'
						break

			elif (event.key == 118): # press v
				print 'do the sound signal with vibrato'
				n = 0
				while True:
					n += 1
					input_string = wf.readframes(BLOCK)
					input_tuple = struct.unpack('h'*OUT, input_string)
					output_value = vibrato(input_tuple,RATE,BLOCK,n,kr)
					output_string = struct.pack('h'*OUT, *output_value)
					stream.write(output_string)
					if pygame.event.get(pygame.KEYDOWN) :
						print 'stop'
						break

			elif (event.key == 110): # press n
				print "do the sound signal with normal"
				while True:
					input_string = wf.readframes(BLOCK)
					stream.write(input_string)
					if pygame.event.get(pygame.KEYDOWN) :
						print 'stop'
						break
					
	stream.stop_stream()
	stream.close()
	p.terminate()

	print 'done'


if __name__ == '__main__':


	
	main()
