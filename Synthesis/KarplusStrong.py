import numpy as np
import math as m
import time
import random
import pyaudio

pa = pyaudio.PyAudio()

SAMPLERATE = 44100 #Samples per second
CHUNK = SAMPLERATE * 2

BUFFERLEN = SAMPLERATE * 2

buffer = np.zeros(BUFFERLEN)
resetBuffer = np.r_[np.zeros(1024), np.ones(BUFFERLEN-1024)]

noiseburst = np.r_[np.random.randn(200),np.zeros(CHUNK-200)]

def karplusStrongChunk(frequency):

    combParameter = 0.98
    pitchPeriod = float(SAMPLERATE/frequency)
    combDelay = m.floor(pitchPeriod-0.5)

    d = pitchPeriod-combDelay-0.5
    apParameter = (1-d)/(1+d)

    output = np.zeros(CHUNK)
    input = noiseburst

    combPrev = 0
    lpPrev = 0

    for n in np.arange(CHUNK):

        if(combDelay > n):
            comb = input[n]
        else:
            comb = input[n] + combParameter*output[n-combDelay]

        lowpass = 0.5*comb + 0.5*combPrev
        combPrev = comb

        output[n] = apParameter*(lowpass-output[n-1])+lpPrev
        lpPrev = lowpass

    return output

def addSoundAtTime(input, time):
    global buffer

    spacerSamples = round((float(time)/1000) * SAMPLERATE)

    input = np.r_[np.zeros(spacerSamples), input, np.zeros(BUFFERLEN-input.size-spacerSamples)]
    buffer = np.add(input, buffer)

def callback(in_data, frame_count, time_info, status):
    global buffer
    #print(frame_count)
    data = (buffer[0:frame_count]).astype(np.float32).tostring()
    #print(buffer.size, resetBuffer.size)
    buffer = np.multiply(buffer, resetBuffer)
    buffer = np.roll(buffer, -frame_count)
    return (data, pyaudio.paContinue)

stream = pa.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate = SAMPLERATE,
                    output=True,
                    stream_callback=callback
                )

stream.start_stream()

while stream.is_active:
    addSoundAtTime(karplusStrongChunk(random.randint(100, 700)), 0)

stream.stop_stream()
stream.close()

p.terminate()
