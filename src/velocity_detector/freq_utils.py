""" Implement frequency helper functions

Author: Ryan Printup
"""

import numpy as np
import config as cfg


fs = cfg.get('sampling', 'freq') / 10 # Hz
T = 1.0 / fs # s

def perform_fft(data):
    """ Perform a FFT on a batch of samples

        Parameters
        ----------
        data : [list]
            The samples to compute the FFT with

        Return
        ------
        freqs : [list]
            The positive frequency bins
        mags : [list]
            The FFT magnitudes
    """
    N = len(data)

    # Generate frequency bin
    freqs = np.fft.fftfreq(N, T)

    # Generate a mask to ignore negative frequencies
    mask = freqs > 0

    # Perform FFT
    fft = np.fft.fft(data)

    # Normalize FFT
    fft = fft / 2

    # Compute magnitude and account
    # for power lost in negative frequencies
    fft = 2.0 * np.abs(fft)

    return freqs[mask], fft[mask]


def get_dominant_freq(freqs, mags):
    """ Return the dominant frequency from a FFT

        Parameters
        ----------
        freqs : [int]
            The frequency bins from the FFT
        mags : [int]
            The magnitudes from the FFT

        Return: int - Dominant frequency
    """
    max_mag   = 0
    max_mag_i = 0

    i = 0

    for mag in mags:
        if mag > max_mag and freqs[i] > 5:
            max_mag = mag
            max_mag_i = i

        i += 1

    return freqs[max_mag_i]

### End of File ###