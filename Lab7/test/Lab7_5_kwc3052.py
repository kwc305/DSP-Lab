
import pyaudio
import struct
import wave
import math
import numpy as np
from matplotlib import pyplot as plt
import myfunctions
import  scipy.signal as signal




RATE = 10000


b = np.array([5, -4, 3,-2,1])
a = np.array([1,-2,3, -4, 5])

# compute the frequency response
w, h = signal.freqz(b,a,RATE)
plt.xlabel('Normalized Frequency-notch 1(n)')
plt.ylabel('dB')
plt.ylim(-5, 5)        # set y-axis limits
plt.xlim(0, 5) 
plt.plot(w, (h))


plt.show()





print '* Done'
















