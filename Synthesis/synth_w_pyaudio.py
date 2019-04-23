import numpy as np
import math
import pyaudio

p = pyaudio.PyAudio()

samplingFreq = 44100
length = 5 #seconds

sampleLength = samplingFreq*length
rotLength = 2*math.pi * np.divide(np.arange(sampleLength), 440)

stream = p.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate = samplingFreq,
                    output=True
                )

noise = np.random.uniform(1, -1, samplingFreq*5)
sin = np.sin(rotLength) * 0.01

stream.write(sin.astype(np.float32).tostring())
stream.close()
