from math import cos 
from math import pi 
import pyaudio
import struct
import numpy
import Lab_2_ASGMNT_4_7_kwc305

# 16 bit/sample

# Fs : Sampling frequency (samples/second)
Fs = 8000
# Fs = 16000   
# Fs = 32000

T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Pole location
f1 = 400
om1 = 2.0*pi * float(f1)/Fs

Ta1 = 0.5
Ta2 = 0.8

r1 = 0.01**(1/(Ta1*Fs))      # Try other values, 0.998, 0.9995, 1.0
r2 = 0.01**(1/(Ta2*Fs)) 
r1 = float(r1)
r2 = float(r2)    # Ensure r is a float
print r1
print r2

# Qustion: how to set r to obtain desired time constant?

# Difference equation coefficients

# a[0] = 0
# a[1] = -2*r1*cos(om1)
# a[2] = r1**2
a = [1, -2*r1*cos(om1), r1**2]
# b = [3]
# b[0] = 0
# b[1] = -2*r2*cos(om1)
# b[2] = r2**2
b = [1, -2*r2*cos(om1), r2**2]
print a
print b 



# Initialization
y1 = 0.0
y2 = 0.0
y21 = 0.0
y22 = 0.0
gain = 10.0

gain = Lab_2_ASGMNT_4_7_kwc305.gaincheck(gain, 32767)

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 1, 
                rate = Fs,
                input = False, 
                output = True, 
                frames_per_buffer = 1)

for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation
    y0 = x0 - a[1] * y1 - a[2] * y2 
    
    

    y00 = y0 - b[1] * y21 - b[2] * y22

    # Delays
    y2 = y1
    y1 = y0
    y22 = y21
    y21 = y00

    # Output
    out = gain * y00
    str_out = struct.pack('h', out)     # 'h' for 16 bits
    stream.write(str_out, 1)

print("* done *")

stream.stop_stream()
stream.close()
p.terminate()
