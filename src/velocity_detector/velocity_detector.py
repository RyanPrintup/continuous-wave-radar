#!/usr/bin/python

"""Velocity Detector

WORK IN PROGRESS

Author : Ryan Printup 
"""

import matplotlib.pyplot as plt
import signal
import sys
import csv
from ring_buf import RingBuffer
import filters as flt
import config as cfg

# Global run variable
running = False

def signal_handler(signal, frame):
    """ A signal handler function used to safely exit
        the main execution loop
    """

    global running
    running = False
    
def run():
    """ This is the main execution function for this script.
        Execution can be interrupted by pressing Ctrl + C
    """

    # Initalize data buffers
    out_data_raw = []
    out_data = [] # Output Data Buffer

    ring_buf = RingBuffer(cfg.get('filtering', 'average_bin_size'))

    # Main loop
    global running
    running = True

    print("Running... Hit Ctrl + C to terminate")

    with open('../../data/movement_test2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            sample = int(row[0])

            out_data_raw.append(sample)
            ring_buf.append(flt.remove_dc(sample))

            if ring_buf.full():
                out_data.append(flt.moving_average(ring_buf.get()))

    plt.figure(1)
    plt.plot(out_data_raw)
    
    plt.figure(2)
    plt.plot(out_data)
    
    plt.show()    

if __name__ == "__main__":
    # Init SIGINT handler for safe termination
    signal.signal(signal.SIGINT, signal_handler)

    # Execute main program
    run()

### End of File ###
