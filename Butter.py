import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
order = 6
fs = 50       # sample rate, Hz
cutoff = 2.25  # desired cutoff frequency of the filter, Hz

# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
allData = np.loadtxt(open('data.csv', 'rb'), delimiter=",")
t = allData[:,0]
plt.plot(t, allData[:,12]+0.01, 'b-', label='data')
data = allData[:,12]

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

z_accel = y
y_accel = butter_lowpass_filter(allData[:,11], cutoff, fs, order)
x_accel = butter_lowpass_filter(allData[:,10], cutoff, fs, order)
newData = allData
newData[:,10] = x_accel-0.1
newData[:,11] = y_accel+0.033
newData[:,12] = z_accel+0.045

np.savetxt('newData.csv', newData, delimiter=',')

plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()