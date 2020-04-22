#!/usr/bin/python


"""Velocity Detector

WORK IN PROGRESS

Author : Ryan Printup 
"""


import numpy as np
import matplotlib.pyplot as plt
import signal
import sys
import csv
import filters
from ring_buf import RingBuffer
from filters import moving_average, dc_removal, impulse_noise_removal


# Global run variable
running = False


def signal_handler(signal, frame):
    """ A signal handler function used to safely exit
        the main execution loop
    """

    global running
    running = False


def get_frequencies(samples, sample_rate):
    """ Todo

        Parameters
        ----------
        samples : list
        
    """

    N   = len(samples)
    fft = np.fft.fft(samples)

    return np.fft.fftfreq(N, 1.0 / sample_rate)


    
def run():
    """ This is the main execution function for this script.
        Execution can be interrupted by pressing Ctrl + C
    """

    # Initalize data buffers
    out_data_buf_raw = []
    out_data_buf = [] # Output Data Buffer

    ring_buf = RingBuffer(10)
    fft_ring_buf = RingBuffer(1024)
    ring_buf2 = RingBuffer(20)

    # Main loop
    global running
    running = True

    print("Running... Hit Ctrl + C to terminate")

    with open('../../data/movement_test2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            sample = int(row[0])

            ### Modify from here on ###

            out_data_buf_raw.append(sample)

            ring_buf.append(dc_removal(sample))

            if ring_buf.full():
                ring_buf2.append(impulse_noise_removal(ring_buf.get()))

            if ring_buf2.full():
                out_data_buf.append(moving_average(ring_buf2.get()))
                
    out_data_buf = fft(out_data_buf)



    plt.plot(out_data_buf)
    plt.show()    


def print_usage():
    """ Print script usage to the user """

    print("Usage: velocity-detector.py")


if __name__ == "__main__":
    # Init SIGINT handler for safe termination
    signal.signal(signal.SIGINT, signal_handler)


    # Execute main program
    run()


### End of File ###
