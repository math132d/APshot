import numpy as np
import math as m
import time as t
import random
import _thread
import pyaudio
import serial

#Init pyaudio
pa = pyaudio.PyAudio()

SAMPLERATE = 44100 #Samples per second
CHUNK = SAMPLERATE * 2 #How many samples to generate a pluck over

BUFFERLEN = SAMPLERATE * 3

buffer = np.zeros(BUFFERLEN)
resetBuffer = np.r_[np.zeros(1024), np.ones(BUFFERLEN-1024)] #Used to reset the first 1024 samples in the buffer

noiseburst = np.r_[np.random.randn(200),np.zeros(CHUNK-200)] #Used as the input in karplusStrong

def karplusStrongChunk(frequency, volume):
    #Function for generating karplusStrong samples with a lenth of CHUNK
    #Frequency is essentially the pitch

    combParameter = 0.99 #Value that determines the plucks decay. Must be close to, but less then 1
    pitchPeriod = float(SAMPLERATE/frequency)
    combDelay = int(m.floor(pitchPeriod-0.5)) #Integer Delay required for the comb-filter to achieve the desired pitch

    #apParameter determines the fractional delay required to achieve the desired pitch
    #Used in the All-Pass filter
    d = pitchPeriod-combDelay-0.5
    apParameter = (1-d)/(1+d)

    #Setting up input and output vars
    #Output is lenth of CHUNK samples filled with zeros
    output = np.zeros(CHUNK)
    input = noiseburst * (m.pow(10, volume/20))

    #Delayed values for the combFilter and LowPassFilter.
    #Set to the previous sample later in the code
    combPrev = 0
    lpPrev = 0

    #Applying karplusStrong for every sample in the output: length = CHUNK
    for n in range(CHUNK-1):

        if(combDelay > n):
            comb = input[n] #If the delay would cause array to 'underflow' just use the input at 'n'
        else:
            comb = input[n] + combParameter*output[n-combDelay] #Differential function for combFilter

        lowpass = 0.5*(comb + combPrev) #Differential function for LowPassFilter
        combPrev = comb

        output[n] = apParameter*(lowpass-output[n-1])+lpPrev #Differential function for AllPassFilter
        lpPrev = lowpass

    return output


def addPluckAtTime(freq, volume, time):
    #Function for adding a pluck sound to the buffer
    #freq determines the pitch
    #time is a delay added before the sound is inserted into buffer in samples

    global buffer
    s_t = t.time() #Starttime for measuring performance
    spacerSamples = time
    input = karplusStrongChunk(freq, volume) #Generate the pluck using karplusStrong

    #Padding input with zeros before adding to the buffer. Must be same length
    input = np.r_[np.zeros(spacerSamples), input, np.zeros(BUFFERLEN-input.size-spacerSamples)]
    buffer = np.add(input, buffer)

    e_t = t.time() #Endtime for measuring performance
    print((e_t-s_t)*1000) #Prints time operation took
    return

def callback(in_data, frame_count, time_info, status):
    #Callback used by pyaudio when ready for the next chunk for playback
    #Returns 'frame_count' samples of data from the buffer to be played back
    global buffer

    #Gets first 'frame_count' samples from the array (frame_count should be 1024 samples)
    data = (buffer[0:frame_count]*0.05).astype(np.float32).tostring()

    #Resets the first 1024 samples of the buffer (Since they were already read)
    buffer = np.multiply(buffer, resetBuffer)
    #Roll empty samples to the back of the buffer (Leaving the next chunk to be read)
    buffer = np.roll(buffer, -frame_count)
    #return the data for playback, paContinue indicated there is more data to be read
    return (data, pyaudio.paContinue)

#Opens pyaudio stream for playback
stream = pa.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate = SAMPLERATE,
                    output=True, #Output for playback
                    stream_callback=callback #Which callback function to use
                )

#Start the stream => Start reading and playing from buffer
stream.start_stream()

#Holds the main thread active while sound is playing
#Polling for serial input from Arduino
while stream.is_active:
    _thread.start_new_thread(addPluckAtTime, (440, -20, 0))

#Terminate program (Probably will never be reached atm. Oops)
stream.stop_stream()
stream.close()

p.terminate()
