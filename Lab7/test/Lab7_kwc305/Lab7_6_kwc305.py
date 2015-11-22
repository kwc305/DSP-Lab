
import pyaudio
import struct
import wave
import numpy as np
from matplotlib import pyplot as plt
import myfunctions
import  scipy.signal as signal
import cmath
# Open wave file (mono)
wave_file_name = 'author.wav'
# wave_file_name = 'arctic_a0001.wav'
wf = wave.open( wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 
BLOCKSIZE = 2**12
f0 = 0              # 'dock audio'
f = 3
W=0.7
NumBlocks = int(np.floor(LEN/BLOCKSIZE))
print 'Rate =', RATE
print 'Width =', WIDTH
print 'Number of frames =', LEN
print 'Number of channels =', CHANNELS
print 'BLOCKSIZE =', BLOCKSIZE
print 'NumBlocks =', NumBlocks

t =[n for n in range(0, RATE*2)]


filter_order = 2    # 4 order filte

# Initialize angle
theta = 0.0

# Block-to-block angle increment
theta_del = (float(BLOCKSIZE*f0)/RATE - np.floor(BLOCKSIZE*f0/RATE)) * 2.0 * np.pi

output_block = [0 for n in range(0, BLOCKSIZE)]

# N, Wn = signal.buttord([10, 500], [50, 70], 3, 40, True)
fs_Hz = RATE
om = 2.0 * np.pi * float(f)/RATE

def genallpass(f,fs,R):	
	om = 2.0 * np.pi * float(f)/fs
	a1 = -2 * R * np.cos(om)
	a2 = R**2
	a = [1, a1, a2]
	b = list(a)
	b.reverse()
	return a,b
R = 0.9
f1 = 1
#[a,b] = make2ndAllpassNotch(f1,RATE,R)

       

a,b = genallpass(f1,RATE,0.95)
a = np.array(a)
b = np.array(b)
j = cmath.sqrt(-1)
# print f[910:930]
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)

for i in range(0, NumBlocks):
	# Get frames from audio input stream
	input_string = wf.readframes(BLOCKSIZE)       # BLOCKSIZE = number of frames read
	input_tuple = struct.unpack('h' *BLOCKSIZE, input_string)    # Convert
	
	a = a * np.exp(j*np.pi*i)
	b = b * np.exp(j*np.pi*i)
	a = np.array(a)
	b = np.array(b)
	# print i,a,b
	output_block = signal.filtfilt(b,a,input_tuple)
	# output_block = signal.filtfilt(b2,a2,output_block1)
	
	for n in range(0, BLOCKSIZE):
		# output_block[n] = myfunctions.clip16(W*np.exp(j*i*np.pi)*np.real(output_block[n])+input_tuple[n])
		output_block[n] = myfunctions.clip16(W*np.real(output_block[n])+input_tuple[n])
	# print(np.exp(j*i*np.pi))
	# Set angle for next block
	
	output_string = struct.pack('h' *BLOCKSIZE, *output_block)
	# output_string = struct.pack('hh' * BLOCKSIZE*NumBlocks, *input_tuple)
	stream.write(output_string)

plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print '* Done'





