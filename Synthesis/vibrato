import numpy as np

# vibrato with the time-varying delay
def vibrato(inputSignal, maxDelay, modFreq, offset = 0):
    nData = np.size(inputSignal)
    outputSignal = np.zeros(nData)
    tmpSignal = np.zeros(nData)

    for n in np.arrange(nData):
        # Calculate Delay
        delay = offset + (maxDelay/2)*(1-np.cos(modFreq*n))

        # Calculate filter output
        if n < delay:
            outputSignal[n] = 0
        else:
            intDelay = np.int(np.floor(delay)) # np.floor returns largest integer
            tmpSignal[n] = inputSignal[n - intDelay]
            fractionalDelay = delay-intDelay
            apParameter = (1-fractionalDelay)/(1+fractionalDelay)
            outputSignal[n] = apParameter*tmpSignal[n]+tmpSignal[n-1]-apParameter*outputSignal[n-1]
        return outputSignal
