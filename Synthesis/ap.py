import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
import sounddevice as sd

# load a guitar signal
samplingFreq, fullGuitarSignal = wave.read('guitar.ff.sulB.B3.wav')
data = np.random.uniform(-1, 1, samplingFreq)
fullGuitarSignal = fullGuitarSignal/2**15 # normalise
sd.play(fullGuitarSignal, samplingFreq)
sd.play(data, samplingFreq)
sd.wait()
