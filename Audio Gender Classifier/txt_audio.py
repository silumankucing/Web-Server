import numpy as np
from scipy.io import wavfile as wav
from scipy.fftpack import fft

rate, data = wav.read('sound.wav')
np.savetxt("output.csv", np.abs(fft(data)))