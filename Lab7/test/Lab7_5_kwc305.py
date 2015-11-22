
import pyaudio
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import  scipy.signal as signal




RATE = 1000


# b = np.array([5, -4, 3])
# a = np.array([3, -4, 5])

r = 0.95
offset = 0.01
b1 = [1 + offset , -2*math.cos(math.pi/2),1 - offset]
a1 = [1 - offset, -2 * math.cos(math.pi/2), 1 + offset]

r1 = 0.85

b2 = [1 + offset , -2*math.cos(math.pi/4),1 - offset]
a2 = [1- offset, -2 * math.cos(math.pi/4), 1 + offset]

bconv = np.convolve(b1,b2)
aconv = np.convolve(a1,a2)

# compute the frequency response
w, h = signal.freqz(bconv,aconv,RATE)
plt.xlabel('Normalized Frequency-notch ')
plt.ylabel('dB')
plt.ylim(-5, 5)        # set y-axis limits
plt.xlim(0, 5) 
plt.plot(w, (h))

pp  = PdfPages('two notch.pdf')
plt.savefig(pp, format='pdf')
pp.close()
plt.show()



print '* pdf saved'
print '* Done'
















