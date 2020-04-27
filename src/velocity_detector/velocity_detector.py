#!/usr/bin/python

"""Velocity Detector

WORK IN PROGRESS

Author : Ryan Printup 
"""


import matplotlib.pyplot as plt
import numpy as np

import signal
import sys
import serial
from math import pow

from ring_buf import RingBuffer
import filters as flt
import config as cfg
import freq_utils
import time



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
    out_data = []

    ring_buf_avg = RingBuffer(cfg.get('filtering', 'average_bin_size'))
    ring_buf_fft = [None] * cfg.get('filtering', 'fft_bin_size')
    ring_buf_fft_i = 0

    fig = plt.figure()
    plt.ylim([0, 200])
    fig.show()
    artist, = plt.plot(0)

    # Connect to serial port
    ser = serial.Serial(cfg.get('serial', 'port'), cfg.get('serial', 'baud_rate'))
    if (ser.is_open == False):
        ser.open()

    # Main loop
    global running
    running = True

    print("Running... Hit Ctrl + C to terminate")

    while running:
        # Read a packet of data from serial stream. Remove trailing
        # whitespace, new line character, and byte literal. Split data
        # by spaces.
        sample = int(ser.readline().strip().decode('utf-8').split())
        
        # Check if buffer is populated
        if sample:
            ring_buf_avg.append(flt.remove_dc(sample))

            if ring_buf_avg.full():
                out = flt.moving_average(ring_buf_avg.get())
                out_data.append(out)
                ring_buf_fft[ring_buf_fft_i] = out
                ring_buf_fft_i += 1

                if ring_buf_fft_i == len(ring_buf_fft):
                    ring_buf_fft_i = 0

                    freqs, mags = freq_utils.perform_fft(ring_buf_fft)

                    artist.remove()
                    artist, = plt.plot(freqs, mags, 'r')
                    fig.canvas.draw()

    # Clean up code
    ser.close()


if __name__ == "__main__":
    # Init SIGINT handler for safe termination
    signal.signal(signal.SIGINT, signal_handler)

    # Execute main program
    run()


### End of File ###
