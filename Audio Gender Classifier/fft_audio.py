import numpy as np 
import array
from scipy.io import wavfile as wavv
import pydub
import matplotlib.pyplot as plt
from numpy import fft as fft

sound = pydub.AudioSegment.from_mp3("sadarkanaku.mp3")
sound.export("sound.wav", format="wav")
au_rate, au_data = wavv.read("sound.wav")
raw_data = sound.raw_data
sample_rate = sound.frame_rate
sample_size = sound.sample_width
channels = sound.channels

channel1 = au_data[:,0]
time = np.arange(0, float(au_data.shape[0]), 1)/sample_rate

fourier1 = fft.fft(channel1)
plt.plot(time, fourier1)
plt.show()