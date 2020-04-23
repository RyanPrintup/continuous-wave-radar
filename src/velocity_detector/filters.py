#!/usr/bin/python

""" Defines Digital Signal Processing (DSP) filter functions

Author: Ryan Printup
"""

import config as cfg
from math import pow

def moving_average(samples):
    """ Computes the moving average from a batch
        of samples

        Parameters
        ----------
        samples : [int]
            A buffer containing the samples
    """
    return sum(samples) / len(samples)

# The following variables are used in the dc_removal() method.
# Since we know the DC bias of our circuit, we can compute the
# digital value and simply remove it from all incoming signals
#
# The variables are defined outside the function to avoid computing
# them everytime the function is called
#
# The following two (2) variables are based on
# the Teensy 4.0 board
analog_reference_voltage = 3.3 # V
adc_sample_resolution = pow(2, 12) - 1 # 12-bit (0-4095)

analog_dc_bias = cfg.get('filtering', 'dc_bias_voltage')
digital_dc_bias = int((adc_sample_resolution / analog_reference_voltage) * analog_dc_bias)

def remove_dc(sample):
    """ Remove the DC bias from a sample
    
        Parameters
        ----------
        sample : int
            The sample to remove the DC bias from
    """
    return sample - digital_dc_bias

""" End of File """
