from math import cos, pi
import pyaudio
import struct
import numpy
import Lab_2_ASGMNT_4_7_kwc305
# 16 bit/sample

# Fs : Sampling frequency (samples/second)
Fs = 8000
# Try Fs = 16000 and 32000


T = 3       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Difference equation coefficients
a1 = -3.7998
a2 = 5.6048
a3 = -3.7911
a4 = 0.9954

 
# Initialization
y1 = 0.0
y2 = 0.0
y3 = 0.0
y4 = 0.0

gain = 10000
gain = Lab_2_ASGMNT_4_7_kwc305.gaincheck(gain,170)


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
    y0 = x0 - a1 * y1 - a2 * y2 - a3 * y3 - a4 * y4
    # delay
    y4 = y3
    y3 = y2
    y2 = y1
    y1 = y0
    
    # Difference equation
    # Output
    out = gain * y0
    print n,'y0:',y0,'out:',out,y1,y2,y3,y4
    str_out = struct.pack('i', out)     # 'h' for 16 bits
    stream.write(str_out, 1)
print("* done *")

stream.stop_stream()
stream.close()
p.terminate()
