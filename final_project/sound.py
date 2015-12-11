
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


pygame.init()

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

def main(input_tuple,RATE, Type, OUT, BLOCK, n, kr):
	
	stop = False
	while stop == False:

		if Type == 'q':
			sys.exit(1)

		elif Type == 'l': # lowpass
			output_value = lowpassfilter(input_tuple,RATE)
			output_string = struct.pack('h'*OUT, *output_value)
			if pygame.event.get(pygame.KEYDOWN) :
				stop == True
				
		elif Type == 'h': # highpass 
			output_value = highpassfilter(input_tuple,RATE)
			output_string = struct.pack('h'*OUT, *output_value)
			if pygame.event.get(pygame.KEYDOWN) :
				stop == True
				
		elif Type == 'b': # bandpass
			output_value = bandstopfilter(input_tuple,RATE)
			output_string = struct.pack('h'*OUT, *output_value)
			if pygame.event.get(pygame.KEYDOWN) :
				stop == True
				
		elif Type == 'v': # vibrato
			output_value = vibrato(input_tuple,RATE,BLOCK,n,kr)
			output_string = struct.pack('h'*OUT, *output_value)
			
			if pygame.event.get(pygame.KEYDOWN) :
				stop == True
				
		elif Type == 'n': # normal
			output_string = struct.pack('h'*OUT, *input_tuple)				
			if pygame.event.get(pygame.KEYDOWN) :
				stop == True
				
		return output_string
		print "log"
			

if __name__ == '__main__':

	main()
