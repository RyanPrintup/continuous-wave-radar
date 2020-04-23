#!/usr/bin/python

""" Implements a basic config file using YAML

Author: Ryan Printup
"""

import yaml
import os.path

cfg_filename = 'config.yaml'

# Default Config
default_cfg = {
    'filtering': {
        'dc_bias_voltage': 1.57,
        'average_bin_size': 10
    },
    'serial': {
        'baud_rate': 9600,
        'port': 'COM1'
    },
    'sampling': {
        'sampling_freq': 10000
    }
}

def get(*argv):
    """ Get a setting from the config file

        Parameters
        ----------
        key(s) : str
            The key (or keys) of the setting
    """
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
