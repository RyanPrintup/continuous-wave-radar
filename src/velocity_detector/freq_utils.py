#!/usr/bin/python

""" Implement frequency helper functions

Author: Ryan Printup
"""

# Vendors
import numpy as np

# Custom
import config as cfg


# The following variables are used in the perform_fft() method.
# The variables are defined outside the function to avoid computing
# them everytime the function is called.
#
# NOTE: In order to perform a FFT, we need to know the sampling frequency
# of our data. Since we are downsampling by applying a moving average filter,
# the sampling frequency set in the config is not the same sampling frequency
# of the data going into the FFT. We need to account for this by dividing the
# sample frequency by the average bin size
adc_fs       = cfg.get('sampling', 'freq')
avg_bin_size = cfg.get('filtering', 'avg_bin_size')

fs = adc_fs / avg_bin_size # Hz
T = 1.0 / fs               # s

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
    fft = fft / N

    # Compute magnitude and account
    # for power lost in negative frequencies
    fft = 2.0 * np.abs(fft)

    # Return only positive spectrum
    return freqs[mask], fft[mask]


# The following variables are used in the get_dominant_freq() method.
# The variables are defined outside the function to avoid computing
# them everytime the function is called.
mag_threshold  = cfg.get('filtering', 'fft_mag_threshold')
freq_threshold = cfg.get('filtering', 'fft_freq_threshold')

def get_dominant_freq(freqs, mags):
    """ Return the dominant frequency from a FFT spectrum

        Parameters
        ----------
        freqs : [int]
            The frequency bins from the FFT
        mags : [int]
            The magnitudes from the FFT

        Return: int - Dominant frequency
    """
    max_mag   = 0 # The current max magnitude
    max_mag_i = 0 # The index of the max magnitude

    i = 0
    for mag in mags:
        if mag > max_mag and mag > mag_threshold:
            if freqs[i] > freq_threshold:
                max_mag  = mag
                max_mag_i = i

        i += 1

    if max_mag == 0:
        return 0, 0 # Hz
    else:
        return freqs[max_mag_i], max_mag


# The following variables are used in the calc_speed_from_freq()
# method. The variables are defined outside the function to avoid
# computing them everytime the function is called.
radar_freq = cfg.get('radar', 'freq') # Hz
c = 3 * pow(10, 8) # Speed of light (m/s)

def calc_speed_from_freq(freq):
    """ Calculate speed from doppler frequency

        Parameters
        ----------
        freq : int
            The doppler frequency

        Return: int - Speed in m/s

    """
    return (freq * c) / (2 * radar_freq)

### End of File ###