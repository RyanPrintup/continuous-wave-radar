#!/usr/bin/python

""" Defines Digital Signal Processing (DSP) filter functions

Author: Ryan Printup
"""


# Standard
from statistics import mean
from math import pow

# Custom
import config as cfg


def impulse_removal(data):
    """ Detects impulsive spikes and adjusts them to be of
        similar value to surronding signal

        Parameters
        ----------
        data : [int]
            A buffer containing N amount of recent samples

        Return: int - The adjusted data point
     """
    N = len(data)
    u = mean(data)

    # Number of samples above and below the mean
    marks = {
        "pos": 0,
        "neg": 0
    }

    # Sum of the differences between positive samples
    # and the mean
    diff = 0

    for sample in data:
        if sample > u:
            marks['pos'] += 1
            diff += sample - u
        elif sample < u:
            marks['neg'] += 1

    return u + (marks['pos'] - marks['neg']) * diff / (N * N)


# The following variables are used in the remove_dc() method.
# Since we know the DC bias of our circuit, we can compute the
# digital value and simply remove it from all incoming signals.
#
# NOTE: This methodology assumes the DC bias remains constant
# for the entirety of sampling. Any fluctuations in the DC bias
# point can skew the output. There are algorithms that detect
# the DC bias on the fly. This may be worth looking into in the
# future.
#
# The variables are defined outside the function to avoid computing
# them everytime the function is called.
analog_ref_volt = cfg.get('sampling', 'analog_ref_volt') # V
bit_res         = cfg.get('sampling', 'bit_res')         # bits
dc_bias_volt    = cfg.get('sampling', 'dc_bias_volt')    # V

max_adc_val     = pow(2, bit_res) - 1

# Compute the digital DC bias value 
digital_dc_bias = int((max_adc_val / analog_ref_volt) * dc_bias_volt)

def remove_dc(data):
    """ Remove the DC bias from a sample
    
        Parameters
        ----------
        data : int
            The sample to remove the DC bias from

        Return: int - Sample without DC bias
    """
    return data - digital_dc_bias


""" End of File """
