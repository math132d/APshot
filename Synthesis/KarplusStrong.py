import numpy as np
import math as m
import sounddevice as sd

SAMPLERATE = 44100 #Samples per second
CHUNK = SAMPLERATE * 4

def karplusStrongChunk(frequency):

    combParameter = 0.9
    pitchPeriod = SAMPLERATE/frequency
    combDelay = m.floor(pitchPeriod - 0.5)

    d = pitchPeriod-combDelay-0.5
    apParameter = (1-d)/(1+d)

    output = np.zeros(CHUNK)
    input = np.r_[np.random.randn(200),np.zeros(CHUNK-200)]

    combPrev = 0
    lpPrev = 0

    for n in np.arange(CHUNK):

        if(combDelay < n):
            comb = input[n]
        else:
            comb = input[n] + combParameter*output[n-combDelay]

        lowpass = 0.5*comb + 0.5*combPrev
        combPrev = comb

        output[n] = apParameter*(lowpass + lpPrev - output[n-1])
        lpPrev = lowpass

    return output

outputSignal = karplusStrongChunk(200)

sd.play(outputSignal, SAMPLERATE)
sd.wait()
