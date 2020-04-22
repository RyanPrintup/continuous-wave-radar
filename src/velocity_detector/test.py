import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Sampling Parameters
    sampling_freq = 1000 # Hz
    sampling_period = 1.0 /  sampling_freq # s

    # Signal Parameters
    t = np.arange(0, 10, sampling_period)
    amplitude = 5
    freq = 20
    y = amplitude * np.sin(2 * np.pi * freq * t) + amplitude * np.sin(2 * np.pi * 300 * t)

    # FFT
    fft = np.fft.fft(y)
    T = t[1] - t[0]
    f = np.linspace(0, 1 / T, len(y))

    # Plot
    plt.bar(f[:len(y) // 2], np.abs(fft)[:len(y) // 2] * 1 / len(y), width=1.5)
    plt.show()
