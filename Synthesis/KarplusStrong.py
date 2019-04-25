import numpy as np
import math as m
import time
import sounddevice as sd

SAMPLERATE = 44100 #Samples per second
CHUNK = SAMPLERATE * 3

def karplusStrongChunk(frequency):

    combParameter = 0.99
    pitchPeriod = float(SAMPLERATE/frequency)
    combDelay = m.floor(pitchPeriod-0.5)

    d = pitchPeriod-combDelay-0.5
    apParameter = (1-d)/(1+d)

    output = np.zeros(CHUNK)
    input = np.r_[np.random.randn(200),np.zeros(CHUNK-200)]

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

startTime = time.time()

outputSignal = karplusStrongChunk(440)

endTime = time.time()
print((endTime-startTime)*1000)

sd.play(outputSignal, SAMPLERATE)
sd.wait()
