# import source


import pyaudio
import struct
import wave
import math




def feedback_modulated_delay(data, modwave, dry, wet):
  ''' Use LFO "modwave" as a delay modulator (with feedback)
  '''
  out = data
  for i in xrange(len(data)):
    index = int(i - modwave[i])
    if index >= 0 and index < len(data):
      out[i] = out[i] * dry + out[index] * wet
  return out


def chorus(data, freq, dry=0.5, wet=0.5, depth=1.0, delay=25.0, rate=44100):
  ''' Chorus effect
      http://en.wikipedia.org/wiki/Chorus_effect
  '''
  length = float(len(data)) / rate
  mil = float(rate) / 1000
  delay *= mil
  depth *= mil
  modwave = (source.sine(freq, length) / 2 + 0.5) * depth + delay
  return modulated_delay(data, modwave, dry, wet)


def flanger(data, freq, dry=0.5, wet=0.5, depth=20.0, delay=1.0, rate=44100):
  ''' Flanger effect
      http://en.wikipedia.org/wiki/Flanging
  '''
  length = float(len(data)) / rate
  mil = float(rate) / 1000
  delay *= mil
  depth *= mil
  modwave = (math.sin(freq/ length) / 2 + 0.5) * depth + delay
  return feedback_modulated_delay(data, modwave, dry, wet)


def tremolo(data, freq, dry=0.5, wet=0.5, rate=44100):
  ''' Tremolo effect
      http://en.wikipedia.org/wiki/Tremolo
  '''
  length = float(len(data)) / rate
  modwave = (source.sine(freq, length) / 2 + 0.5)
  return (data * dry) + ((data * modwave) * wet)




def modulated_delay(data, modwave, dry, wet):
  ''' Use LFO "modwave" as a delay modulator (no feedback)
  '''
  out = data.copy()
  for i in xrange(len(data)):
    index = int(i - modwave[i])
    if index >= 0 and index < len(data):
      out[i] = data[i] * dry + data[index] * wet
  return out



# Open wave file (mono)
wave_file_name = 'author.wav'
# wave_file_name = 'sin01_mono.wav'
# wave_file_name = 'sin01_stereo.wav'
wf = wave.open( wave_file_name, 'rb')
RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes() 
CHANNELS = wf.getnchannels() 
# TODO: More effects. Distortion, echo, delay, reverb, phaser, pitch shift?
# TODO: Better generalize chorus/flanger (they share a lot of code)

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = 1,
                rate = RATE,
                input = False,
                output = True,
                stream_callback = flanger(wave_file_name,RATE))


stream.stop_stream()
stream.close()
p.terminate()