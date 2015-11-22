

import wave
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import struct
import pyaudio

wavfile = '10_100.wav'
wf = wave.open(wavfile,'rb')

CHANNELS = wf.getnchannels()        # Number of channels
RATE = wf.getframerate()            # Sampling rate (frames/second)
LEN  = wf.getnframes()              # Signal length
WIDTH = wf.getsampwidth()           # Number of bytes per sample
BLOCKSIZE = 512
Nfft = 16000

print('Play the wave file: {0:s} \n with properties:'.format(wavfile))
print('  %d channel(s)'         % CHANNELS)
print('  %d frames/second'      % RATE)
print('  %d frames'             % LEN)
print('  %d bytes per sample'   % WIDTH)

fs_Hz = RATE
# 60 Hz Notch for fs = 250 Hz
# bb = np.array([ 0.96508099, -0.24246832,  1.94539149, -0.24246832,  0.96508099])
# aa = np.array([ 1.        , -0.24677826,  1.94417178, -0.23815838,  0.93138168])

# create the 60 Hz filter
bp_stop_Hz = np.array([59.0, 61.0])
bb, aa = signal.butter(2,bp_stop_Hz/(fs_Hz / 2.0), 'bandstop')
# print bb , aa 
# create the 50 Hz filter
bp2_stop_Hz = np.array([89, 91.0])
bb2, aa2 = signal.butter(2,bp2_stop_Hz/(fs_Hz / 2.0), 'bandstop')

ww, HH = signal.freqz(bb,aa,1000)
ww2, HH2 = signal.freqz(bb2,aa2,1000)
f = ww * fs_Hz / (2*np.pi)             # convert from rad/sample to Hz

p = pyaudio.PyAudio()
stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )
print '* playing..'

x_res = [n for n in range(0,LEN)]
x_fft_res = [n for n in range(0,Nfft)]



input_string = wf.readframes(LEN)
input_value = struct.unpack('h'*LEN, input_string)

output_value1 = signal.filtfilt(bb, aa, input_value)
output_value = signal.filtfilt(bb2,aa2,output_value1)

input_fft = np.fft.fft(input_value,Nfft)
output_fft = np.fft.fft(input_value,Nfft)


output_string = struct.pack('h'*LEN,*output_value)
stream.write(output_string)




# fig3 = plt.figure(1)
# plt.subplot(2,1,1)
# plt.plot(f,np.abs(HH))

# plt.subplot(2,1,2)
# plt.xlim([10,10000])
# plt.ylim([10,200])
# output_notch = signal.filtfilt(bb, aa, output_fft)
# plt.plot(x_fft_res,20*np.log10(np.abs(output_notch)))
# print output_notch
# plt.show()