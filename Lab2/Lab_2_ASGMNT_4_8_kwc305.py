from math import cos, pi
import pyaudio
import struct
 
import Lab_2_ASGMNT_4_7_kwc305

Fs=8000

T=1
N=T*Fs

a1=-1.8999
a2=0.9977


y1=0.0
y2=0.0



# Lab hw



gain = 100000.0


gain = Lab_2_ASGMNT_4_7_kwc305.gaincheck(gain,10173)


p=pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt8, channels=1,
rate=Fs,
input=False,
output=True,
frames_per_buffer=1)

for n in range(0,N):

	if n == 0:
		x0=1.0
	else:
		x0=0.0
	
# difference equation
	y0=x0-a1*y1-a2*y2

	# delays
	y2=y1
	y1=y0

	out=gain*y0
	str_out = struct.pack('h',out)
	stream.write(str_out,1)
	print n,y0,out 
print("*done*")

stream.stop_stream()
stream.close()
p.terminate()

