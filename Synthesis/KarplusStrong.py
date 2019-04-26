import numpy as np
import math as m
import time as t
import random
import _thread
import pyaudio
import serial

ser = serial.Serial("COM4", 9600, timeout=0.1)

pa = pyaudio.PyAudio()

SAMPLERATE = 44100 #Samples per second
CHUNK = SAMPLERATE * 2 #How many samples to generate a pluck over

BUFFERLEN = SAMPLERATE * 3

buffer = np.zeros(BUFFERLEN)
resetBuffer = np.r_[np.zeros(1024), np.ones(BUFFERLEN-1024)] #Used to reset the first 1024 samples in the buffer

noiseburst = np.r_[np.random.randn(200),np.zeros(CHUNK-200)] #Used as the input in karplusStrong

def karplusStrongChunk(frequency):

    combParameter = 0.98
    pitchPeriod = float(SAMPLERATE/frequency)
    combDelay = int(m.floor(pitchPeriod-0.5))

    d = pitchPeriod-combDelay-0.5
    apParameter = (1-d)/(1+d)

    output = np.zeros(CHUNK)
    input = noiseburst

    combPrev = 0
    lpPrev = 0

    for n in range(CHUNK):

        if(combDelay > n):
            comb = input[n]
        else:
            comb = input[n] + combParameter*output[n-combDelay]

        lowpass = 0.5*(comb + combPrev)
        combPrev = comb

        output[n] = apParameter*(lowpass-output[n-1])+lpPrev
        lpPrev = lowpass

    return output


def addPluckAtTime(freq, time):
    global buffer
    s_t = t.time()
    spacerSamples = time
    input = karplusStrongChunk(freq)

    input = np.r_[np.zeros(spacerSamples), input, np.zeros(BUFFERLEN-input.size-spacerSamples)]
    buffer = np.add(input, buffer)
    e_t = t.time()
    print((e_t-s_t)*1000)
    return

def callback(in_data, frame_count, time_info, status):
    global buffer
    data = (buffer[0:frame_count]*0.05).astype(np.float32).tostring()
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

a = _thread.start_new_thread(addPluckAtTime, (440, 0))
b = _thread.start_new_thread(addPluckAtTime, (440, 1024))
c = _thread.start_new_thread(addPluckAtTime, (440, 2048))
d = _thread.start_new_thread(addPluckAtTime, (440, 4096))

while stream.is_active:
    data = ser.readline().decode()

    if len(data) > 0:
        _thread.start_new_thread(addPluckAtTime, (440, 1024))
        print("woop")

stream.stop_stream()
stream.close()

p.terminate()
