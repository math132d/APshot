import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import time

pitch = 440 # Hz

def karplusStrongSyntheziser(inputSignal, combDelay, combParameter, apParameter, nData):
    samplingIndices = np.arange(nData)
    outputSignal = np.zeros(nData)
    lpFilterState = np.zeros(1)
    apFilterState = np.zeros(2)
    for n in samplingIndices:
        # compute lp-filter input
        if n < combDelay:
            lpInput = inputSignal[n]
        else:
            lpInput = inputSignal[n]+combParameter*outputSignal[n-combDelay] #w(n) from slides w/ allpass
        # compute ap-filter input
        apInput = 0.5*lpInput+0.5*lpFilterState #v(n) from slides w/ allpass
        lpFilterState = lpInput
        # compute filter output
        outputSignal[n] = apParameter*(apInput-apFilterState[1])+apFilterState[0] #y(n)?
        apFilterState[0] = apInput
        apFilterState[1] = outputSignal[n]
    return outputSignal, samplingIndices

# play back the signal
while(pitch < 2000):

    # setup
    samplingFreq = 44100 # Hz
    filterCoefficient = 0.94
    pitchPeriod = samplingFreq/pitch
    simulationTime = 3 #s
    nData = np.int(simulationTime*samplingFreq)
    #inputSignal = np.r_[1,np.zeros(nData-1)] # an impulse
    nNoiseSamples = 200
    inputSignal = np.r_[np.random.randn(nNoiseSamples),np.zeros(nData-nNoiseSamples)] # a short noise burst


    # compute Karplus-Strong filter parameters
    combDelay = np.int(np.floor(pitchPeriod-0.5))
    fractionalDelay = pitchPeriod-combDelay-0.5
    apParameter = (1-fractionalDelay)/(1+fractionalDelay)

    # run the algorithm

    startTime = time.time()

    outputSignal, samplingIndices = \
        karplusStrongSyntheziser(inputSignal, combDelay, filterCoefficient, apParameter, nData)

    endTime = time.time()
    print((endTime-startTime)*1000)

    sd.play(outputSignal, samplingFreq)
    sd.wait()

    pitch += pitch*(1/12)
