import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
import sounddevice as sd

def allpass(input, delay, b):
    sampleLength = input.size

    tmpSignal = np.zeros(sampleLength)

    for n in np.arange(sampleLength):

        if n < delay:
            outputDelay = input[n]
        else:
            outputDelay = tmpSignal[n-delay]

        inputDelay = input[n-delay]
        tmpSignal[n] = b*input[n] + inputDelay - b*outputDelay

    return tmpSignal, sampleLength

samplingFreq, fullGuitarSignal = wave.read('/Users/laura/Documents/GitHub/APshot/Synthesis/guitar.ff.sulB.B3.wav')

impulse = np.r_[np.array([1]), np.zeros(100000)]

impulseResponse, sampleLength = allpass(impulse, 500, 0.7)
fullGuitarResponse, _ = allpass(fullGuitarSignal, 500, 0.7)

sd.play(fullGuitarResponse, samplingFreq)

plt.figure(figsize=(5, 3))
plt.plot(np.arange(sampleLength)/44100, impulseResponse)
plt.show()
