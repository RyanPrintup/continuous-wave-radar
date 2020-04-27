#!/usr/bin/python

""" Implements a basic config file using YAML

The config file will be generated from defaults if it 
is not found in the directory.

Author: Ryan Printup
"""


import yaml
import os.path


cfg_filename = 'config.yaml'

# Default Config
default_cfg = {
    'filtering': {
        'average_bin_size': 10,
        'lowpass_cutoff': 2000,
        'lowpass_order': 5,
        'fft_bin_size': 1000
    },
    'serial': {
        'baud_rate': 9600,
        'port': 'COM1'
    },
    'sampling': {
        'dc_bias_volt': 1.65,
        'freq': 10000
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
    # think it's critical to care
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
