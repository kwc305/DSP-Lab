import pyaudio
WIDTH=2
p = pyaudio.PyAudio()
format_pyaudio_int = pyaudio.paInt16 
NUM_CHANNEL_INT = 1
FS = 16000
LENGTH_BUFFER_INT = 2
stream = p.open(format=format_pyaudio_int, channels=NUM_CHANNEL_INT,
rate=FS,
input=False,
output=True,
frames_per_buffer=LENGTH_BUFFER_INT)
# print pyaudio.paInt16
print pyaudio.paInt8
print pyaudio.get_format_from_width(1, unsigned=False)
# print pyaudio.get_format_from_width(WIDTH)
