#!/usr/bin/python

""" Implements a basic config file using YAML

The config file will be generated from defaults if it 
is not found in the directory. If config file does exist,
it will be read.

This is a simple script and does not handle any error checking. 

Author: Ryan Printup
"""


# Standards
import yaml
import os.path
from math import pow


cfg_filename = 'config.yaml'

# Default Config
default_cfg = {
    'filtering': {
        'impulse_bin_size': 50,
        'avg_bin_size': 10,
        'fft_bin_size': 1000,
        'fft_mag_threshold': 0.9,
        'fft_freq_threshold': 6
    },
    'serial': {
        'baud_rate': 115200,
        'port': 'COM10'
    },
    'sampling': {
        'dc_bias_volt': 1.65,
        'analog_ref_volt': 3.3,
        'bit_res': 12,
        'freq': 10000
    },
    'radar': {
        'freq': int(2 * pow(10, 9))
    }
}


def get(*argv):
    """ Get a setting from the config file

        Parameters
        ----------
        key(s) : str
            The key(s) of the setting

        Return: any - Config setting
    """
    # Inefficient to duplicate the config variable
    # everytime this method is called, but I don't
    # think it's critical enough to care
    setting = cfg

    for arg in argv:
        setting = setting[arg]

    return setting


# Check if config file exists
if os.path.isfile(cfg_filename):
    # If it does, read config file
    with open(cfg_filename, 'r') as cfg_file:
        cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
else:
    # else, generate config file from default
    with open(cfg_filename, 'w') as cfg_file:
        yaml.dump(default_cfg, cfg_file)
        cfg = default_cfg


### End of File ###
