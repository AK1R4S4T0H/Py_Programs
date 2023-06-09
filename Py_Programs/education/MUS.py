import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

sr = 44100
freq = 500
length = 1.0

t = np.arange(0,length,1.0/sr)
signal = np.sin(np.pi * 2 *freq* t)

signal*= 32767
signal = np.int16(signal)
wavfile.write("file.wav",sr,signal)