#!/usr/bin/python

""" Defines Digital Signal Processing (DSP) filter functions

Author: Ryan Printup
"""


import config as cfg
from scipy.signal import butter, lfilter


def moving_average(data):
    """ Computes the moving average from a batch
        of samples

        Parameters
        ----------
        data : [int]
            A buffer containing the samples

        Return: int - Computed moving average
    """
    return sum(data) / len(data)


fs = cfg.get('sampling', 'freq')
nyq = 0.5 * fs
cutoff = cfg.get('filtering', 'lowpass_cutoff') / nyq 
order = cfg.get('filtering', 'lowpass_order')
b, a = butter(order, cutoff, btype='low', analog=False)

def butter_lowpass_filter(data):
    """ Apply a Butterworth Lowpass filter to a batch of samples

        Parameters
        ----------
        data : [int]
            The samples to apply the filter to
        
        Return: [int] - The filtered data
    """
    return lfilter(b, a, data)


# The following variables are used in the dc_removal() method.
# Since we know the DC bias of our circuit, we can compute the
# digital value and simply remove it from all incoming signals.
#
# The variables are defined outside the function to avoid computing
# them everytime the function is called.
#
# The following two (2) variables are based on
# the Teensy 4.0 board.
analog_ref_volt = 3.3 # V
adc_sample_res = pow(2, 12) - 1 # 12-bit (0-4095)

analog_dc_bias = cfg.get('sampling', 'dc_bias_volt')
digital_dc_bias = int((adc_sample_res / analog_ref_volt) * analog_dc_bias)

def remove_dc(data):
    """ Remove the DC bias from a sample
    
        Parameters
        ----------
        data : int
            The sample to remove the DC bias from

        Return: int - Sample without DC bias
    """
    return data - digital_dc_bias


def variance_filter(sample, sample_prev):
    """ Ignores small amplitude changes in the signal
        to attempt to remove white noise

        Parameters
        ----------
        sample : int
        sample_prev : int
    """

    if abs(sample - sample_prev) < 5:
        sample = sample_prev
    
    return sample


""" End of File """
