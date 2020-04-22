import yaml
import os.path

cfg_filename = 'config.yaml'

# Default Config
default_cfg = [{
    'filtering': [{
        'dc_bias_voltage': 1.57,
        'average_bin_size': 10
    }],
    'serial': [{
        'baud_rate': 9600,
        'port': 'COM1'
    }],
    'sampling': [{
        'sampling_freq': 10000
    }]
}]

if __name__ == "__main__":
    # Check if config file exists
    if os.path.isfile(cfg_filename):
        # If it does, read config file
        with open(cfg_filename, 'r') as cfg_file:
            cfg = yaml.load(cfg_file, Loader=yaml.FullLoader)
            print(cfg)
    else:
        # else, generate config file from default
        with open(cfg_filename, 'w') as cfg_file:
            yaml.dump(default_cfg, cfg_file)
        

### End of File ###
