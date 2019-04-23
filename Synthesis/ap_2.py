import pyaudio
import time
import _thread as t
import wave
import sys

CHUNK = 1024

wf = wave.open("guitar.ff.sulB.B3.wav", 'rb')

p = pyaudio.PyAudio()

def playSound(speed, x):
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=round(wf.getframerate()/speed),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

t.start_new_thread(playSound, (1, 1))
time.sleep(0.1)
t.start_new_thread(playSound, (1, 1))

time.sleep(5)

p.terminate()
