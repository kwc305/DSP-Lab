import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import wave
import struct

CHUNKSIZE = 1024 # fixed chunk size
filename = 'author.wav'
wf = wave.open( filename, 'rb')

# Read wave file properties
CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample

# NumBlocks = int( DURATION * RATE / BLOCKSIZE )
# Duration = (1/)

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)


# initialize portaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
				channels=1, 
				rate=RATE, 
				input=True, 
				frames_per_buffer=CHUNKSIZE)


# do this as long as you want fresh samples
data = wf.readframes(LEN)
input_tuple = struct.unpack('h'*LEN,data)
# print len(input_tuple)
output_tuple=[]
for a in range(0,LEN):
	print input_tuple[a]
	output_tuple.append( input_tuple[a] * np.cos(2*np.pi*a))

output_tuple = np.fft.fft(output_tuple)
print output_tuple
# output_string = struct.pack('h'*len(output_tuple),*output_tuple)
# numpydata = np.fromstring(output_string, dtype=np.int16)

# plot data
plt.xlim(-2000,2000)
plt.ylim(0,LEN*100)
plt.plot(output_tuple)
plt.show()

# close stream
stream.stop_stream()
stream.close()
p.terminate()