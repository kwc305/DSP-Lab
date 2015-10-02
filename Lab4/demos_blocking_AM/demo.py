import pyaudio
import wave
import sys

chunk = 1024

def convert(data, sampleSize = 4, channel = 0):
    for i in range(0, len(data), 2*sampleSize):
        for j in range(0, sampleSize):
           data[i + j + sampleSize * channel] = data[i + j + sampleSize * (1 - channel)]

if len(sys.argv) < 2:
    print "Plays a wave file.\n\n" +\
          "Usage: %s filename.wav" % sys.argv[0]
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

# open stream
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# read data
data = wf.readframes(chunk)
convert(data)

# play stream
while data != '':
    stream.write(data)
    data = wf.readframes(chunk)
    convert(data)

stream.close()
p.terminate()