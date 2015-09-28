from math import cos 
from math import pi 
import pyaudio
import struct
import numpy
import gain_range

# 16 bit/sample

# Fs : Sampling frequency (samples/second)
Fs = 8000
# Fs = 16000   
# Fs = 32000

T = 2       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Pole location
f1 = 400
om1 = 2.0*pi * float(f1)/Fs

Ta1 = 0.5
Ta2 = 0.9

r1 = 0.01**(1/(Ta1*Fs))      # Try other values, 0.998, 0.9995, 1.0
r1 = float(r1)

r2 = 0.01**(1/(Ta2*Fs)) 
r2 = float(r2)    # Ensure r is a float

# Qustion: how to set r to obtain desired time constant?

# Difference equation coefficients

array1 = [1, -2*r1*cos(om1), r1**2]
array2 = [1, -2*r2*cos(om1), r2**2]



# Initialization
y11 = 0.0
y12 = 0.0
y21 = 0.0
y22 = 0.0
gain = 5.0

gain = gain_range.gain_range(gain)

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
    y00 = x0 - array1[1] * y11 - array1[2] * y12 
    
    

    y10 = y00 - array2[1] * y21 - array2[2] * y22

    # Delays
    y12 = y11
    y11 = y00
    y22 = y21
    y21 = y10

    # Output
    out = gain * y10
    str_out = struct.pack('i', out)     # 'h' for 16 bits
    stream.write(str_out, 1)

print("* done *")

stream.stop_stream()
stream.close()
p.terminate()
